import re
from collections import defaultdict
from core.node_database import NodeDatabase

from parser import (
    parse_ip,
    parse_speed,
    parse_latency,
    parse_location
)
from parser.node_parser import parse_node_info
from parser.ip_parser import parse_ips
from core.node_model import Node

class NodeConverter:
    # 国家默认机房代码
    DEFAULT_AIRPORT = {
        "KR": "ICN",
        "韩国": "ICN",
        "HK": "HKG",
        "香港": "HKG",
        "JP": "NRT",
        "日本": "NRT",
        "SG": "SIN",
        "新加坡": "SIN",
        "US": "LAX",
        "美国": "LAX",
        "DE": "FRA",
        "德国": "FRA",
        "GB": "LHR",
        "英国": "LHR",
        "TW": "TPE",
        "台湾": "TPE",
        "CN": "PEK",
        "中国": "PEK",
    }

    def __init__(self):
        self.counters = defaultdict(int)

    def reset_counter(self):
        self.counters.clear()

    def get_default_airport(self, country, country_name):
        """
        根据国家补默认机房
        """
        return (
            self.DEFAULT_AIRPORT.get(country)
            or self.DEFAULT_AIRPORT.get(country_name)
            or ""
        )

    def convert_line(self, line):
        if not line.strip():
            return None
        node = Node()
        node_info = parse_node_info(line) or {}
        node.tls = node_info.get("tls", False)
        node.asn = node_info.get("asn", "")
        node.isp = node_info.get("isp", "")
        # ======================
        # IP
        # ======================
        ip_data = parse_ip(line) or {}
        node.ip = ip_data.get("ip", "")
        node.port = ip_data.get("port", "")
        # 过滤无效节点
        if not node.ip or not node.port:
            return None
        # ======================
        # 地理
        # ======================
        location = parse_location(line) or {}
        # 如果输入是已经格式化/不完整的形式（如 "#03_JP-HND"、"#HND"、"#03_JP"），
        # 从 "#" 后面尝试提取提示并合并到 location 中以补全信息。
        m = re.search(r"#\s*([^|]+(?:\|[^|]+)?)", line)
        if m:
            token = m.group(1).strip()
            # 删除前导序号/下划线，例如 "03_JP-HND" -> "JP-HND"
            token = re.sub(r"^\d+[_\s-]*", "", token)
            # 把 token 传给 parse_location 作为 hint（parse_location 能识别国家/机场别名）
            hint = parse_location(token) or {}
            for k in ("country", "country_name", "country_display", "city", "airport", "datacenter"):
                if not location.get(k) and hint.get(k):
                    location[k] = hint[k]
        node.country = location.get("country", "")
        node.country_name = location.get("country_name", "")
        if not node.country_name:
            node.country_name = "其他"
        node.country_display = location.get("country_display", "")
        node.city = location.get("city", "")
        node.native_location = location.get("native_location", "")
        # ======================
        # 机场 / 机房代码
        # ======================
        node.airport = (
            location.get("airport")
            or location.get("code")
            or location.get("airport_code")
            or ""
        )
        node.datacenter = (
            location.get("datacenter")
            or location.get("dc")
            or ""
        )
        # datacenter补airport
        if not node.airport and node.datacenter:
            node.airport = node.datacenter
        # 国家默认补机场
        if not node.airport:
            node.airport = self.get_default_airport(
                node.country,
                node.country_name
            )
        # ======================
        # 延迟
        # ======================
        latency = parse_latency(line) or {}
        node.latency = latency.get("latency", "")
        node.latency_value = latency.get("value")
        # ======================
        # 速度
        # ======================
        speed = parse_speed(line) or {}
        node.speed = speed.get("speed", "")
        node.speed_value = speed.get("value")
        node.speed_unit = speed.get("unit", "")
        node.speed_mbps = speed.get("mbps")
        return node

    def assign_number(self, nodes):
        # 先清空计数器
        self.reset_counter()
        # 按节点库国家顺序排序
        country_order = NodeDatabase().country_order()
        nodes.sort(
            key=lambda node: (
                country_order.get(node.country_name, 99),
                node.airport or "",
                node.ip or ""
            )
        )
        for node in nodes:
            # 统一按国家编号（所有国家采用相同逻辑）
            key = node.country_name or "OTHER"
            self.counters[key] += 1
            node.number = f"{self.counters[key]:02d}"
        return nodes

    def convert(self, text):
        """
        支持两种输入风格：
        - 每个节点单独一行（或一行多个 ip:port）
        - 多行块格式（节点信息以空行分隔）

        本方法优先把输入按空行切分为块（block），每个 block 代表一个节点的完整描述（多行）。
        如果没有空行分隔，则按行处理并支持行内多个 ip/port（兼容早期行为）。
        """
        nodes = []

        if not text or not text.strip():
            return []

        # 先尝试将输入按空行分块 —— 使多行节点信息（带标签）能被整体解析
        blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]

        # 如果只有单一块且块中只有一行，则也支持行内多个 ip 的老行为
        for block in blocks:
            # 如果 block 包含多行或包含标签关键字，按 block 处理
            if "\n" in block or any(k in block for k in ["IP地址", "端口", "IP原生位置", "网络延迟", "下载速度"]):
                node_info = parse_node_info(block) or {}
                tls = node_info.get("tls", False)
                asn = node_info.get("asn", "")
                isp = node_info.get("isp", "")

                location = parse_location(block) or {}
                # 保持原来对 '#' hint 的处理
                m = re.search(r"#\s*([^|]+(?:\|[^|]+)?)", block)
                if m:
                    token = m.group(1).strip()
                    token = re.sub(r"^\d+[_\s-]*", "", token)
                    hint = parse_location(token) or {}
                    for k in ("country", "country_name", "country_display", "city", "airport", "datacenter"):
                        if not location.get(k) and hint.get(k):
                            location[k] = hint[k]

                latency = parse_latency(block) or {}
                speed = parse_speed(block) or {}

                ip_list = parse_ips(block)
                if not ip_list:
                    ip_single = parse_ip(block)
                    if ip_single:
                        ip_list = [ip_single]

                for ip_data in ip_list:
                    node = Node()
                    node.tls = tls
                    node.asn = asn
                    node.isp = isp

                    node.ip = ip_data.get("ip", "")
                    node.port = ip_data.get("port", "")

                    if not node.ip or not node.port:
                        continue

                    node.country = location.get("country", "")
                    node.country_name = location.get("country_name", "")
                    if not node.country_name:
                        node.country_name = "其他"
                    node.country_display = location.get("country_display", "")
                    node.city = location.get("city", "")
                    node.native_location = location.get("native_location", "")

                    node.airport = (
                        location.get("airport")
                        or location.get("code")
                        or location.get("airport_code")
                        or ""
                    )
                    node.datacenter = (
                        location.get("datacenter")
                        or location.get("dc")
                        or ""
                    )
                    if not node.airport and node.datacenter:
                        node.airport = node.datacenter
                    if not node.airport:
                        node.airport = self.get_default_airport(
                            node.country,
                            node.country_name
                        )

                    node.latency = latency.get("latency", "")
                    node.latency_value = latency.get("value")
                    node.speed = speed.get("speed", "")
                    node.speed_value = speed.get("value")
                    node.speed_unit = speed.get("unit", "")
                    node.speed_mbps = speed.get("mbps")

                    nodes.append(node)

            else:
                # block 为单行且没有明显标签 —— 支持行内多个 ip 的行为
                ip_list = parse_ips(block)
                if not ip_list:
                    ip_single = parse_ip(block)
                    if ip_single:
                        ip_list = [ip_single]

                # reuse line-level parsing for location/latency/speed
                node_info = parse_node_info(block) or {}
                tls = node_info.get("tls", False)
                asn = node_info.get("asn", "")
                isp = node_info.get("isp", "")
                location = parse_location(block) or {}
                # hint
                m = re.search(r"#\s*([^|]+(?:\|[^|]+)?)", block)
                if m:
                    token = m.group(1).strip()
                    token = re.sub(r"^\d+[_\s-]*", "", token)
                    hint = parse_location(token) or {}
                    for k in ("country", "country_name", "country_display", "city", "airport", "datacenter"):
                        if not location.get(k) and hint.get(k):
                            location[k] = hint[k]
                latency = parse_latency(block) or {}
                speed = parse_speed(block) or {}

                for ip_data in ip_list:
                    node = Node()
                    node.tls = tls
                    node.asn = asn
                    node.isp = isp

                    node.ip = ip_data.get("ip", "")
                    node.port = ip_data.get("port", "")

                    if not node.ip or not node.port:
                        continue

                    node.country = location.get("country", "")
                    node.country_name = location.get("country_name", "")
                    if not node.country_name:
                        node.country_name = "其他"
                    node.country_display = location.get("country_display", "")
                    node.city = location.get("city", "")
                    node.native_location = location.get("native_location", "")

                    node.airport = (
                        location.get("airport")
                        or location.get("code")
                        or location.get("airport_code")
                        or ""
                    )
                    node.datacenter = (
                        location.get("datacenter")
                        or location.get("dc")
                        or ""
                    )
                    if not node.airport and node.datacenter:
                        node.airport = node.datacenter
                    if not node.airport:
                        node.airport = self.get_default_airport(
                            node.country,
                            node.country_name
                        )

                    node.latency = latency.get("latency", "")
                    node.latency_value = latency.get("value")
                    node.speed = speed.get("speed", "")
                    node.speed_value = speed.get("value")
                    node.speed_unit = speed.get("unit", "")
                    node.speed_mbps = speed.get("mbps")

                    nodes.append(node)

        return self.assign_number(nodes)

    def output(self, text, format_name="default"):
        nodes = self.convert(text)
        return "\n".join(
            node.output_line(format_name)
            for node in nodes
        )
