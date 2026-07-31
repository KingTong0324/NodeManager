from collections import defaultdict
import os
import json
import re

from parser import (
    parse_ip,
    parse_speed,
    parse_latency,
    parse_location
)

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



    def __init__(self, auto_fill_default_airport=False):

        # 新增可配置开关：是否在只有 country 时自动补默认机房
        # 默认根据调用者传入（此处默认 False，表示不自动补默认机房）
        self.auto_fill_default_airport = auto_fill_default_airport

        self.counters = defaultdict(int)

        # 从配置/映射中派生的城市->code 映射缓存（延迟加载）
        self._city_map = None

        # 常见日本机场代码后备集合（用于 airport->country 的后备判定）
        self.JP_AIRPORTS = {
            "NRT", "HND", "TYO", "KIX", "ITM", "OSA", "NGO",
            "FUK", "SPK", "OKA", "CTS", "KMQ", "FSZ", "MMB"
        }



    def reset_counter(self):

        self.counters.clear()



    def get_default_airport(self, country, country_name):

        """
        根据国家补默认机房
        """

        return (
            self.DEFAULT_AIRPORT.get(country)
            or
            self.DEFAULT_AIRPORT.get(country_name)
            or
            ""
        )

    def _load_city_map(self):
        """
        延迟加载 NodeManager/config/city.json，并构建从 alias/name -> code 的映射
        """
        if self._city_map is not None:
            return self._city_map

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
        path = os.path.join(base_dir, "config", "city.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                city_data = json.load(f)
        except Exception:
            city_data = {}

        mapping = {}
        for city_name, info in city_data.items():
            code = info.get("code")
            if not code:
                continue
            # map canonical name
            mapping[city_name.lower()] = code
            # map aliases
            for alias in info.get("aliases", []):
                mapping[str(alias).lower()] = code

        self._city_map = mapping
        return mapping


    def convert_line(self, line):

        if not line.strip():
            return None

        node = Node()

        # ======================
        # IP
        # ======================

        ip_data = parse_ip(line) or {}

        node.ip = ip_data.get(
            "ip",
            ""
        )

        node.port = ip_data.get(
            "port",
            ""
        )

        # ======================
        # 地理
        # ======================

        location = parse_location(line) or {}

        # 如果输入含有 "# 后缀"，把后缀按常见分隔符拆成多个 segment，逐段尝试解析并合并有用字段
        m = re.search(r"#\s*([^|\n]+)", line)
        if m:
            raw_token = m.group(1).strip()
            # 先把已有的格式化编号/序号前缀去掉，例如 "03_NRT"、"01-TYO" 等
            raw_token = re.sub(r"^\d+[_\s-]*", "", raw_token)
            # 拆分常见分隔符： '/', '|', ',', ' '（保留连字符与下划线作为内部分隔）
            segments = re.split(r"[\/|,]", raw_token)

            city_map = self._load_city_map()

            for seg in segments:
                seg = seg.strip()
                if not seg:
                    continue
                # 清洗噪声：去掉像 '43ms', '10.8MB/s', ports, IPs 等
                if re.search(r"\d+ms$", seg) or re.search(r"\d+(\.\d+)?(MB/s|MB|M/s)$", seg, re.I):
                    continue
                # 去掉末尾的 :port
                seg = re.sub(r":\d+$", "", seg)
                # 如果看起来是 IP，跳过
                if re.match(r"^\d+\.\d+\.\d+\.\d+$", seg):
                    continue
                # 标准化连字符下划线为中线形式（保留原格式）
                cand = seg
                # 先尝试直接解析该段
                hint = parse_location(cand) or {}
                # 若 parse_location 未解析出 airport 但解析出 city，我们尝试 city->code 补全
                if hint and not hint.get("airport") and hint.get("city"):
                    code = city_map.get(str(hint.get("city")).lower())
                    if code:
                        hint["airport"] = code

                # 另外，如果 parse_location 返回空，我们尝试把该段做为 city alias 检查
                if not hint:
                    code = city_map.get(cand.lower())
                    if code:
                        hint = {"airport": code}

                # 合并 hint 到 location，只在目标字段为空时填充
                if hint:
                    for k in ("country", "country_name", "country_display", "city", "airport", "datacenter"):
                        if not location.get(k) and hint.get(k):
                            location[k] = hint[k]

        node.country = location.get(
            "country",
            ""
        )

        node.country_name = location.get(
            "country_name",
            ""
        )

        node.country_display = location.get(
            "country_display",
            ""
        )

        node.city = location.get(
            "city",
            ""
        )

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
        # 只有在 auto_fill_default_airport 开启时，才自动用国家默认机房补 airport
        if not node.airport and self.auto_fill_default_airport:
            node.airport = self.get_default_airport(
                node.country,
                node.country_name
            )

        # ======================
        # 延迟
        # ======================

        latency = parse_latency(line) or {}

        node.latency = latency.get(
            "latency",
            ""
        )

        node.latency_value = latency.get(
            "value"
        )

        # ======================
        # 速度
        # ======================

        speed = parse_speed(line) or {}

        node.speed = speed.get(
            "speed",
            ""
        )

        node.speed_value = speed.get(
            "value"
        )

        node.speed_unit = speed.get(
            "unit",
            ""
        )

        node.speed_mbps = speed.get(
            "mbps"
        )

        return node


    def assign_number(self,nodes):

        self.reset_counter()

        for node in nodes:

            # 如果是日本节点，按国家统一编号（保证日本连续编号）
            is_japan = (
                (node.country and str(node.country).upper() == "JP")
                or (node.country_name == "日本")
                or ("日本" in (node.country_display or ""))
                or (node.airport and str(node.airport).upper() in self.JP_AIRPORTS)
            )

            if is_japan:
                # 按国家编号（所有日本节点共用一个计数器）
                key = "JP"
            else:
                # 其他国家按机房/机场代码编号，优先使用 airport，再使用 datacenter，最后退回到国家
                key = node.airport or node.datacenter or node.country or "OTHER"

            self.counters[key] += 1

            node.number = (
                f"{self.counters[key]:02d}"
            )

        return nodes

    def convert(self,text):

        nodes=[]

        for line in text.splitlines():

            node=self.convert_line(line)

            if node:

                nodes.append(node)

        return self.assign_number(nodes)

    def output(self,text,format_name="default"):

        nodes=self.convert(text)

        return "\n".join(

            node.output_line(format_name)

            for node in nodes

        )