import re


def parse_ip(text):
    """
    解析IP和端口

    返回:
    {
        "ip": "172.64.229.68",
        "port": "443"
    }

    如果没有匹配:
    返回 None
    """

    result = {
        "ip": "",
        "port": ""
    }


    # 匹配 IPv4
    ip_match = re.search(
        r'(\d{1,3}(?:\.\d{1,3}){3})',
        text
    )

    if ip_match:
        result["ip"] = ip_match.group(1)

        # 匹配IP后面的端口
        port_match = re.search(
            r'(?:[:|,=\s]+)(\d{2,5})',
            text[ip_match.end():]
        )

        if port_match:
            result["port"] = port_match.group(1)

            return result


    return None