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
    GBps
    Gbps
    Gb/s

    返回:
    {
        "speed": "10.82MB/s",
        "value": 10.82,
        "unit": "MB/s",
        "mbps": 86.56
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

    pattern = (
        r'(\d+(?:\.\d+)?)'
        r'(GB/s|GBps|Gbps|Gb/s|'
        r'MB/s|MBps|Mbps|Mbit/s|Mb/s|'
        r'KB/s|KBps|Kbps|Kb/s)'
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

    unit = normalize_unit(
        match.group(2)
    )

    display_value = value
    display_unit = unit

    # KB/s 转 MB/s
    if unit == "KB/s" and value >= 1024:
        display_value = round(
            value / 1024,
            2
        )
        display_unit = "MB/s"

    # MB/s 转 GB/s
    elif unit == "MB/s" and value >= 1024:
        display_value = round(
            value / 1024,
            2
        )
        display_unit = "GB/s"

    result["value"] = value
    result["unit"] = unit
    result["speed"] = f"{display_value}{display_unit}"

    result["mbps"] = convert_to_mbps(
        value,
        unit
    )

    return result


def normalize_unit(unit):
    """
    单位标准化
    """

    u = unit.replace(
        " ",
        ""
    ).lower()

    mapping = {
        # Byte
        "gb/s": "GB/s",

        "mb/s": "MB/s",

        "kb/s": "KB/s",

        # bit
        "gbps": "Gbps",
        "gb/s": "GB/s",
        "gb/s": "GB/s",

        "mbps": "Mbps",
        "mbit/s": "Mbps",

        "kbps": "Kbps"
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