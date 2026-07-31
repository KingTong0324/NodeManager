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

    "CN":"PEK",
    "JP":"TYO",
    "KR":"SEL",
    "SG":"SIN",
    "HK":"HKG",
    "TW":"TPE",

    "US":"LAX",
    "GB":"LON",
    "DE":"FRA",
    "FR":"PAR",
    "NL":"AMS",

    "CA":"YYZ",
    "AU":"SYD",

    "IN":"DEL",
    "TH":"BKK",
    "MY":"KUL",
    "PH":"MNL",
    "ID":"JKT"

}



# =========================
# 城市反向
# =========================

def build_city_reverse(data):

    result={}

    for city,info in data.items():

        if isinstance(info,dict):

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
# 保留真实机场代码
# NRT -> NRT
# HND -> HND
# TYO -> TYO
# =========================

def build_airport_reverse(data):

    result={}

    for city,info in data.items():

        if not isinstance(info,dict):

            continue


        city_code=str(
            info.get(
                "code",
                ""
            )
        ).upper()


        if city_code:

            result[
                city_code.lower()
            ]={

                "city":city,

                "airport":city_code

            }


        for alias in info.get("aliases", []):
            # 把 alias 映射到 canonical city_code（不要用 alias.upper() 当 code）
            result[str(alias).lower()] = {
                "city": city,
                "airport": city_code
            }


    return result



# =========================
# 机房反向
# =========================

def build_datacenter_reverse(data):

    result={}

    for city,info in data.items():

        if not isinstance(info,dict):

            continue


        code=str(
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

def detect_airport(text):

    source=text.lower()


    for alias,info in airport_reverse.items():

        if len(alias)<3:

            continue


        pattern = (
            r"(?<![a-z])"
            +
            re.escape(alias)
            +
            r"(?![a-z])"
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

    source=text.lower()


    for alias,code in datacenter_reverse.items():

        if len(alias)<3:

            continue


        if alias in source:

            return code


    return ""



# =========================
# 国家检测
# =========================

def detect_country(text):

    source=text.lower()


    for code,info in region_map.items():


        if isinstance(info,dict):

            aliases=list(
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

            aliases=[

                code,

                str(info)

            ]



        for alias in aliases:


            alias=str(alias).lower().strip()


            if not alias:

                continue



            if len(alias)<=2:


                pattern=(

                    r"(?<![a-z])"
                    +
                    re.escape(alias)
                    +
                    r"(?![a-z])"

                )


                match=re.search(
                    pattern,
                    source
                )


            else:

                match=alias in source



            if match:


                return {

                    "country":code,

                    "country_name":
                        info.get("name","")
                        if isinstance(info,dict)
                        else str(info),


                    "country_display":
                        (
                            info.get("flag","")
                            +
                            " "
                            +
                            info.get("name","")
                        )
                        if isinstance(info,dict)
                        else str(info)

                }


    return {}



# =========================
# 主解析
# =========================

def parse_location(text):


    result={

        "country":"",
        "country_name":"",
        "country_display":"",

        "city":"",
        "airport":"",
        "datacenter":""

    }


    if not text:

        return result


    country=detect_country(text)

    if country:

        result.update(country)


    airport=detect_airport(text)

    if airport:

        result["airport"]=airport["airport"]

        result["city"]=airport["city"]


    source=text.lower()


    for alias,city in city_reverse.items():

        if alias in source:

            result["city"]=city

            break


    dc=detect_datacenter(text)

    if dc:

        result["datacenter"]=dc


    if not result["airport"] and result["datacenter"]:

        result["airport"]=result["datacenter"]


    if not result["airport"]:

        country_code=result["country"]

        if country_code in DEFAULT_AIRPORT:

            result["airport"]=DEFAULT_AIRPORT[country_code]


    return result
