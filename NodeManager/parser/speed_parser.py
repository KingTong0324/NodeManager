import re


def parse_speed(text):
    """
    下载速度解析器

    支持:

    MB/s
    MBps
    Mbps
    Mb/s
    Mbit/s
    KB/s
    KBps
    Kbps
    Kb/s
    GB/s
    Gbps

    返回:

    {
        "speed": "10.82MB/s",
        "value": 10.82,
        "unit": "MB/s",
        "mbps": 86.56
    }

    无匹配:

    {
        "speed":"",
        "value":None,
        "unit":"",
        "mbps":None
    }
    """


    result = {
        "speed": "",
        "value": None,
        "unit": "",
        "mbps": None
    }


    if not text:
        return result


    source = text.replace(" ", "")



    # 匹配速度单位
    pattern = (
        r'(\d+(?:\.\d+)?)'
        r'(Gbps|GB/s|GBps|'
        r'Mbps|MB/s|MBps|Mbit/s|Mb/s|'
        r'Kbps|KB/s|KBps|Kb/s|'
        r'Gb/s)'
    )


    match = re.search(
        pattern,
        source,
        re.IGNORECASE
    )


    if not match:
        return result



    value = float(
        match.group(1)
    )


    unit_raw = match.group(2)



    unit = normalize_unit(unit_raw)



    result["value"] = value
    result["unit"] = unit
    result["speed"] = f"{value}{unit}"

    result["mbps"] = convert_to_mbps(
        value,
        unit
    )


    return result



def normalize_unit(unit):

    """
    单位标准化
    """

    u = unit.lower()


    mapping = {

        "gbps": "Gbps",
        "gb/s": "GB/s",
        "gbps": "Gbps",
        "gbps": "Gbps",

        "mbps": "Mbps",
        "mb/s": "MB/s",
        "mbps": "Mbps",
        "mbps": "Mbps",
        "mbit/s": "Mbps",

        "kbps": "Kbps",
        "kb/s": "KB/s",
        "kbps": "Kbps",

    }


    return mapping.get(
        u,
        unit
    )



def convert_to_mbps(value, unit):

    """
    所有速度统一转换 Mbps

    1 Byte = 8 bit

    """

    if unit == "GB/s":
        return round(
            value * 1024 * 8,
            2
        )


    if unit == "MB/s":
        return round(
            value * 8,
            2
        )


    if unit == "KB/s":
        return round(
            value / 128,
            2
        )


    if unit == "Gbps":
        return round(
            value * 1000,
            2
        )


    if unit == "Mbps":
        return round(
            value,
            2
        )


    if unit == "Kbps":
        return round(
            value / 1000,
            2
        )


    return None