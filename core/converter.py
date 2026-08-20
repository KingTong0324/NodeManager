# core/converter.py
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

    def convert_line_to_nodes(self, line, inherited=None):
        """
        把单行解析为一个或多个 Node 实例（支持行内多个 ip:port）。
        inherited: 可选的 dict，包含从 block 级继承的 asn/tls/isp 等（如果需要）
        """
        nodes = []
        if inherited is None:
            inherited = {}

        # 优先尝试 node_info 从行内提取（会覆盖 inherited）
        node_info = parse_node_info(line) or {}
        tls = node_info.get("tls", inherited.get("tls", False))
        asn = node_info.get("asn", inherited.get("asn", ""))
        isp = node_info.get("isp", inherited.get("isp", ""))

        ip_list = parse_ips(line)
        if not ip_list:
            # fallback to single ip parse
            ip_single = parse_ip(line)
            if ip_single:
                ip_list = [ip_single]

        # 行级的 location/latency/speed
        location = parse_location(line) or {}
        latency = parse_latency(line) or {}
        speed = parse_speed(line) or {}

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

        return nodes

    def convert_line_block(self, block):
        """
        保留原来的 block-level（带标签、多行描述）解析逻辑：
        当 block 中包含标签关键字（如 IP地址、端口、下载速度 等）时，
        我们把整个 block 视作一个节点描述，然后从 block 中提取 ip 列表并把 block-level 的 location/latency/speed 应用到每个 ip。
        """
        nodes = []

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
        # fallback: prefer node_info.ip/node_info.port if parse_node_info extracted them (supports split-line labels)
        if not ip_list:
            if node_info.get("ip") and node_info.get("port"):
                ip_list = [{"ip": node_info.get("ip"), "port": node_info.get("port")}]
            else:
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

        return nodes

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

        修复要点：
        - 如果一个 block 包含多行但没有标签关键词（如“IP地址”等），则把 block 当作多条独立的单行记录来逐行解析，
          避免把 block 级别的 speed/location 错误地应用到 block 内所有 IP。
        - 如果 block 是带标签的多行描述（常见于详细信息块），保留原 block-level 的解析逻辑。
        """
        nodes = []

        if not text or not text.strip():
            return []

        blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]

        label_keywords = ["IP地址", "端口", "IP原生位置", "网络延迟", "下载速度"]

        for block in blocks:
            # 如果 block 包含多行并且没有 label 关键词，则把它拆成多行逐行解析（避免 block-level 复用）
            if "\n" in block and not any(k in block for k in label_keywords):
                # 逐行处理；每行作为单独记录解析
                for line in block.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    line_nodes = self.convert_line_to_nodes(line)
                    nodes.extend(line_nodes)
            else:
                # 否则保留原来的行为（对带标签或单行 block 进行 block-level 处理）
                # 如果是单行但没有标签，convert_line_to_nodes 也能正确处理（保留兼容性）
                if "\n" in block:
                    # 带标签的多行描述
                    nodes.extend(self.convert_line_block(block))
                else:
                    # 单行，按行解析（支持一行多个 ip）
                    nodes.extend(self.convert_line_to_nodes(block))

        return self.assign_number(nodes)

    def output(self, text, format_name="default"):
        nodes = self.convert(text)
        return "\n".join(
            node.output_line(format_name)
            for node in nodes
        )
