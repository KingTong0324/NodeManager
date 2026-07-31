from collections import defaultdict

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



        # ======================
        # 地理
        # ======================

        location = parse_location(line) or {}



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

        self.reset_counter()



        for node in nodes:

            country = node.country or "OTHER"


            self.counters[country] += 1


            node.number = (
                f"{self.counters[country]:02d}"
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