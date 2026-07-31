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


    # 匹配 IPv4:端口
    match = re.search(
        r'(\d{1,3}(?:\.\d{1,3}){3}):(\d+)',
        text
    )


    if match:
        result["ip"] = match.group(1)
        result["port"] = match.group(2)

        return result


    return None