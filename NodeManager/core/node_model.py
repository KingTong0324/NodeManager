import os
import json


class Node:
    def __init__(self):
        self.ip = ""
        self.port = ""

        # 国家信息
        self.country = ""
        self.country_name = ""
        self.country_display = ""

        # 地理信息
        self.city = ""

        # 机房代码
        self.airport = ""
        self.datacenter = ""

        # 网络信息
        self.latency = ""
        self.latency_value = None

        self.speed = ""
        self.speed_value = None
        self.speed_unit = ""
        self.speed_mbps = None

        # 编号
        self.number = ""


    def to_dict(self):
        return {
            "ip": self.ip,
            "port": self.port,

            "country": self.country,
            "country_name": self.country_name,
            "country_display": self.country_display,

            "city": self.city,

            # 保存机房代码
            "airport": self.airport,
            "datacenter": self.datacenter,

            "latency": self.latency,
            "latency_value": self.latency_value,

            "speed": self.speed,
            "speed_value": self.speed_value,
            "speed_unit": self.speed_unit,
            "speed_mbps": self.speed_mbps,

            "number": self.number
        }


    def from_dict(self, data):

        for key, value in data.items():

            if hasattr(self, key):
                setattr(self, key, value)

        return self



    def display_name(self):

        name = self.country_name

        if self.number:
            name += self.number

        # 优先机场代码
        code = self.airport or self.datacenter

        if code:
            name += f"_{code}"

        return f"{self.country_display} {name}"



    def get_variables(self):

        return {

            "ip": self.ip,
            "port": self.port,

            "country": self.country,
            "country_name": self.country_name,
            "country_display": self.country_display,

            "city": self.city,

            # 输出变量
            "airport": self.airport,
            "datacenter": self.datacenter,

            # 新增兼容变量
            "code": self.airport or self.datacenter,

            "number": self.number,

            "latency": self.latency,
            "latency_value": self.latency_value,

            "speed": self.speed,
            "speed_value": self.speed_value,
            "speed_unit": self.speed_unit,
            "speed_mbps": self.speed_mbps
        }



    def render(self, template):

        variables = self.get_variables()

        try:
            return template.format(**variables)

        except KeyError as e:
            return f"错误变量:{e}"



    def load_format(self, name="default"):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        path = os.path.join(
            base_dir,
            "config",
            "format.json"
        )


        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                formats=json.load(f)


            return formats.get(name,"")


        except Exception:

            return ""



    def output_line(self, format_name="default"):

        template=self.load_format(format_name)


        if not template:

            template = (
                "{ip}:{port}"
                "#{country_display} "
                "{country_name}{number}_{code}"
                "|{speed}"
            )


        return self.render(template)