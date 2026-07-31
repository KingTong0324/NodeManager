import os
import json
import re


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

        # 延迟加载并缓存 city->code 映射，使用 config/city.json 中的 code/aliases
        # 这样当 airport 为空但 city 可识别时，我们仍能输出标准三字码
        if not hasattr(Node, "_city_map_cache") or Node._city_map_cache is None:
            Node._city_map_cache = {}
            try:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                path = os.path.join(base_dir, "config", "city.json")
                with open(path, "r", encoding="utf-8") as f:
                    city_data = json.load(f)
                for cname, info in city_data.items():
                    code = info.get("code")
                    if not code:
                        continue
                    Node._city_map_cache[cname.lower()] = code
                    for alias in info.get("aliases", []):
                        Node._city_map_cache[str(alias).lower()] = code
            except Exception:
                Node._city_map_cache = {}

        city_key = (self.city or "").lower().strip()
        mapped_code = Node._city_map_cache.get(city_key)

        code_value = (
            (self.airport or self.datacenter)
            or mapped_code
            or (self.city.upper() if self.city else "")
        )

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

            # 兼容变量：code 始终为标准三字码（或 city.upper() 退路）
            "code": code_value,

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

        rendered = self.render(template)

        # 如果 speed 为空，则去掉末尾多余的 '|'（以及尾随空白）
        if not (self.speed and str(self.speed).strip()):
            rendered = re.sub(r"\|\s*$", "", rendered)

        return rendered
