from collections import defaultdict
from core.node_database import NodeDatabase
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
            or
            self.DEFAULT_AIRPORT.get(country_name)
            or
            ""
        )

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
        # 过滤无效节点
        if not node.ip or not node.port:
            return None        

        # ======================
        # 地理
        # ======================

        location = parse_location(line) or {}

        # 如果输入是已经格式化/不完整的形式（如 "#03_JP-HND"、"#HND"、"#03_JP"），
        # 从 "#" 后面尝试提取提示并合并到 location 中以补全信息。
        m = re.search(r"#\s*([^|]+)", line)
        if m:
            token = m.group(1).strip()
            # 删除前导序���/下划线，例如 "03_JP-HND" -> "JP-HND"
            token = re.sub(r"^\d+[_\s-]*", "", token)
            # 把 token 传给 parse_location 作为 hint（parse_location 能识别国家/机场别名）
            hint = parse_location(token) or {}

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

        if not node.country_name:
            node.country_name="其他"

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

        if not node.airport:

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

        # 先清空计数器
        self.reset_counter()

        # 按节点库国家顺序排序
        country_order = NodeDatabase().country_order()

        nodes.sort(
            key=lambda node: (
                country_order.get(
                    node.country_name,
                    99
                ),
                node.airport or "",
                node.ip or ""
            )
        )

        for node in nodes:

            is_japan = (
                (node.country and str(node.country).upper() == "JP")
                or (node.country_name == "日本")
                or ("日本" in (node.country_display or ""))
                or (node.airport and str(node.airport).upper() in {"NRT","HND","TYO","KIX","ITM","OSA","NGO","FUK","SPK","OKA","CTS","KMQ","FSZ","MMB"})
            )

            if is_japan:
                key = "JP"
            else:
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
