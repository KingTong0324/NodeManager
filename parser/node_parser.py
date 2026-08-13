import re

FIELD_ALIASES = {
    "ip": [
        "IP地址",
        "IP",
        "Address",
        "IP Address"
    ],
    "port": [
        "端口",
        "Port"
    ],
    "tls": [
        "TLS",
        "SSL"
    ],
    "asn": [
        "ASN编号",
        "ASN",
        "AS"
    ],
    "isp": [
        "运营商",
        "ISP",
        "Provider",
        "Organization"
    ],
    "location": [
        "IP原生位置",
        "原生位置",
        "Location",
        "Country",
        "Region"
    ],
    "ping": [
        "网络延迟",
        "延迟",
        "Latency",
        "Ping",
        "RTT"
    ],
    "speed": [
        "下载速度",
        "速度",
        "Download",
        "Speed"
    ]
}

def find_field_value(text, aliases):
    pattern = "|".join(
        re.escape(item)
        for item in aliases
    )

    match = re.search(
        rf"(?:{pattern})\s*[:：=]\s*([^\n]+)",
        text,
        re.I
    )

    if match:
        return match.group(1).strip()

    return ""

def parse_node_info(text):
    result = {
        "ip": "",
        "port": "",
        "name": "",
        "country": "",
        "tls": False,
        "asn": "",
        "isp": "",
        "location": "",
        "ping": 0,
        "speed": ""
    }

    if not text:
        return result

    node_match = re.search(
        r"([0-9a-fA-F:.]+):(\d+)(?:#([^\s]+))?",
        text
    )

    if node_match:
        result["ip"] = node_match.group(1)
        result["port"] = node_match.group(2)
        if node_match.group(3):
            result["name"] = node_match.group(3)

            country_match = re.search(
                r"([A-Z]{2})",
                result["name"]
            )
            if country_match:
                result["country"] = country_match.group(1)

    ip = find_field_value(
        text,
        FIELD_ALIASES["ip"]
    )

    if ip:
        ip_match = re.search(
            r"[0-9a-fA-F:.]+",
            ip
        )
        if ip_match:
            result["ip"] = ip_match.group(0)

    port = find_field_value(
        text,
        FIELD_ALIASES["port"]
    )

    if port:
        port_match = re.search(
            r"\d+",
            port
        )
        if port_match:
            result["port"] = port_match.group(0)

    tls = find_field_value(
        text,
        FIELD_ALIASES["tls"]
    )
    if tls:
        result["tls"] = tls.lower() in [
            "true",
            "yes",
            "enabled",
            "on",
            "1"
        ]

    result["asn"] = find_field_value(
        text,
        FIELD_ALIASES["asn"]
    )
    if not result["asn"]:
        asn_match = re.search(
            r"(AS\d+\s+[^\n]+)",
            text,
            re.I
        )

        if asn_match:
            result["asn"] = asn_match.group(1).strip()

    result["isp"] = find_field_value(
        text,
        FIELD_ALIASES["isp"]
    )
    result["location"] = find_field_value(
        text,
        FIELD_ALIASES["location"]
    )

    result["location"] = re.sub(
        r"^[^\w\u4e00-\u9fa5]+",
        "",
        result["location"]
    ).strip()

    result["location"] = re.sub(
        r"^[\s│└─]+",
        "",
        result["location"]
    ).strip()
    ping = find_field_value(
        text,
        FIELD_ALIASES["ping"]
    )
    if ping:
        ping_match = re.search(
            r"\d+",
            ping
        )
        if ping_match:
            result["ping"] = int(
                ping_match.group(0)
            )
    speed = find_field_value(
        text,
        FIELD_ALIASES["speed"]
    )
    if speed:
        speed_match = re.search(
            r"[0-9.]+\s*[A-Za-z/]+",
            speed
        )
        if speed_match:
            result["speed"] = (
                speed_match.group(0)
                .replace(" ", "")
            )

    return result