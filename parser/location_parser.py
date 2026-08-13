import os
import json
import re

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CONFIG_DIR = os.path.join(
    BASE_DIR,
    "config"
)

def load_json(filename):
    path = os.path.join(
        CONFIG_DIR,
        filename
    )

    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception:
        return {}

region_map = load_json("region.json")
city_map = load_json("city.json")
airport_map = load_json("airport.json")
datacenter_map = load_json("datacenter.json")

# =========================
# 默认机场
# =========================

DEFAULT_AIRPORT = {
    "CN": "PEK",
    "JP": "TYO",
    "KR": "SEL",
    "SG": "SIN",
    "HK": "HKG",
    "TW": "TPE",
    "US": "LAX",
    "GB": "LON",
    "DE": "FRA",
    "FR": "PAR",
    "NL": "AMS",
    "CA": "YYZ",
    "AU": "SYD",
    "IN": "DEL",
    "TH": "BKK",
    "MY": "KUL",
    "PH": "MNL",
    "ID": "JKT"
}

# =========================
# 城市反向
# =========================

def build_city_reverse(data):
    result = {}

    for city, info in data.items():
        if isinstance(info, dict):
            for alias in info.get(
                "aliases",
                []
            ):
                result[
                    str(alias).lower()
                ] = city
        else:
            result[
                str(info).lower()
            ] = city

    return result


# =========================
# 机场反向
# =========================

def build_airport_reverse(data):
    result = {}

    for code, info in data.items():
        if not isinstance(info, dict):
            continue

        airport_code = str(
            info.get(
                "code",
                code
            )
        ).upper()

        city = info.get(
            "city",
            ""
        )

        country = info.get(
            "country",
            ""
        )

        result[
            airport_code.lower()
        ] = {
            "city": city,
            "airport": airport_code,
            "country": country
        }

        for alias in info.get(
            "aliases",
            []
        ):
            result[
                str(alias).lower()
            ] = {
                "city": city,
                "airport": airport_code,
                "country": country
            }

    return result


# =========================
# 机房反向
# =========================

def build_datacenter_reverse(data):
    result = {}

    for city, info in data.items():
        if not isinstance(info, dict):
            continue

        code = str(
            info.get(
                "code",
                ""
            )
        ).upper()

        if code:
            result[
                code.lower()
            ] = code

        for alias in info.get(
            "aliases",
            []
        ):
            result[
                str(alias).lower()
            ] = code

    return result


city_reverse = build_city_reverse(
    city_map
)

airport_reverse = build_airport_reverse(
    airport_map
)

datacenter_reverse = build_datacenter_reverse(
    datacenter_map
)


# =========================
# 机场检测
# =========================

def detect_airport(text, country_code=""):
    source = text.lower()

    # 优先匹配真实机场代码
    for code, info in airport_map.items():

        if country_code and info.get("country") != country_code:
            continue

        airport_code = str(
            info.get(
                "code",
                code
            )
        ).lower()

        if len(airport_code) < 3:
            continue

        pattern = (
            r"(?<![a-z])"
            + re.escape(airport_code)
            + r"(?![a-z])"
        )

        if re.search(
            pattern,
            source
        ):
            return {
                "city": info.get(
                    "city",
                    ""
                ),
                "airport": airport_code.upper(),
                "country": info.get(
                    "country",
                    ""
                )
            }

    # 再匹配机场别名
    for alias, info in airport_reverse.items():

        if country_code and info.get("country") != country_code:
            continue

        if len(alias) < 3:
            continue

        pattern = (
            r"(?<![a-z])"
            + re.escape(alias)
            + r"(?![a-z])"
        )

        if re.search(
            pattern,
            source
        ):
            return info

    return None

# =========================
# 机房检测
# =========================

def detect_datacenter(text):
    source = text.lower()

    for alias, code in datacenter_reverse.items():
        if len(alias) < 3:
            continue

        if alias in source:
            return code

    return ""

# =========================
# 原生位置检测
# =========================

def detect_native_location(text):
    lines = text.splitlines()

    for index, line in enumerate(lines):
        if "IP原生位置" in line or "原生位置" in line:
            for next_line in lines[index + 1:index + 3]:
                value = re.sub(
                    r"^[^\w\u4e00-\u9fa5]+",
                    "",
                    next_line
                ).strip()

                if value:
                    return value

    return ""

# =========================
# 国家检测
# =========================

def detect_country(text):
    source = text.lower()

    for code, info in region_map.items():
        if isinstance(info, dict):
            aliases = list(
                info.get(
                    "aliases",
                    []
                )
            )

            aliases.append(code)
            aliases.append(
                info.get(
                    "name",
                    ""
                )
            )

        else:
            aliases = [
                code,
                str(info)
            ]

        for alias in aliases:
            alias = str(alias).lower().strip()

            if not alias:
                continue

        if len(alias) <= 2:
            pattern = (
                r"(?<![a-z])"
                +
                re.escape(alias)
                +
                r"(?![a-z])"
            )

            match = re.search(
                pattern,
                source
            )

        else:
            match = re.search(
                r"(?<![a-z])"
                + re.escape(alias)
                + r"(?![a-z])",
                source
            )

        if match:
            return {
                "country": code,
                "country_name":
                    info.get("name", "")
                    if isinstance(info, dict)
                    else str(info),
                "country_display":
                    (
                        info.get("flag", "")
                        +
                        " "
                        +
                        info.get("name", "")
                    )
                    if isinstance(info, dict)
                    else str(info)
            }
    return {}


# =========================
# 主解析
# =========================

def parse_location(text, country_code=""):
    result = {
        "country": "",
        "country_name": "",
        "country_display": "",
        "city": "",
        "airport": "",
        "datacenter": "",
        "native_location": ""
    }

    if not text:
        return result

    text = re.sub(
        r"^[^\w\u4e00-\u9fa5]+",
        "",
        text
    ).strip()

    native_location = detect_native_location(text)

    if native_location:
        result["native_location"] = native_location

    if country_code:
        region = region_map.get(
            country_code,
            {}
        )

        if isinstance(region, dict):
            result["country"] = country_code
            result["country_name"] = region.get(
                "name",
                ""
            )
            result["country_display"] = (
                region.get("flag", "")
                +
                " "
                +
                region.get("name", "")
            )

    else:
        country = detect_country(text)

        if country:
            result.update(country)

    airport = detect_airport(
        text,
        result["country"]
    )

    if airport:
        result["airport"] = airport["airport"]
        result["city"] = airport["city"]

        if not result["country"] and airport.get("country"):
            result["country"] = airport["country"]

            region = region_map.get(
                airport["country"],
                {}
            )

            if isinstance(region, dict):
                result["country_name"] = region.get(
                    "name",
                    ""
                )

                result["country_display"] = (
                    region.get("flag", "")
                    +
                    " "
                    +
                    region.get("name", "")
                )

    source = text.lower()

    for city, info in city_map.items():
        if not isinstance(info, dict):
            continue

        if result["country"] and info.get("country") != result["country"]:
            continue

        for alias in info.get(
            "aliases",
            []
        ):
            if str(alias).lower() in source:
                result["city"] = city
                break

    dc = detect_datacenter(text)

    if dc:
        result["datacenter"] = dc

    if not result["airport"] and result["datacenter"]:
        result["airport"] = result["datacenter"]

    if not result["airport"]:
        country_code = result["country"]

        if country_code in DEFAULT_AIRPORT:
            result["airport"] = DEFAULT_AIRPORT[country_code]

    return result