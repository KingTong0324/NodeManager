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
        self.native_location = ""

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
            "native_location": self.native_location,

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

        code = self.airport or self.datacenter

        if code:
            name += f"_{code}"

        return f"{self.country_display} {name}"

    def get_variables(self):

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

        if ":" in self.ip:
            ip_port = f"[{self.ip}]:{self.port}"
        else:
            ip_port = f"{self.ip}:{self.port}"

        return {
            "ip": self.ip,
            "port": self.port,
            "ip_port": ip_port,

            "country": self.country,
            "country_name": self.country_name,
            "country_display": self.country_display,

            "city": self.city,

            "airport": self.airport,
            "datacenter": self.datacenter,

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

                formats = json.load(f)

            return formats.get(name, "")

        except Exception:

            return ""

    def output_line(self, format_name="default"):

        template = self.load_format(format_name)

        if self.country_name == "其他" and not self.airport and not self.city:

            if ":" in self.ip:
                rendered = (
                    f"[{self.ip}]:{self.port}"
                )
            else:
                rendered = (
                    f"{self.ip}:{self.port}"
                )

            if self.speed and str(self.speed).strip():
                rendered += f"|{self.speed}"

            return rendered

        if not template:

            template = (
                "{ip_port}"
                "#{country_display} "
                "{country_name}{number}_{code}"
                "|{speed}"
            )

        rendered = self.render(template)

        rendered = re.sub(r"\|\s*$", "", rendered)
        rendered = re.sub(r"_\s*$", "", rendered)
        rendered = re.sub(r"#\s*$", "", rendered)

        return rendered