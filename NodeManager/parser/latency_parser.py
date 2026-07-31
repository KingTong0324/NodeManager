import re


def parse_latency(text):
    """
    延迟解析器

    支持格式：

    98ms
    98 ms
    98MS
    ping=98ms
    ping 98ms
    latency:98ms
    delay:98ms
    delay 98 ms
    time=98ms
    RTT 98ms
    rtt:98ms
    98毫秒

    返回:
    {
        "latency": "98ms",
        "value": 98
    }

    无匹配:
    {
        "latency": "",
        "value": None
    }
    """


    result = {
        "latency": "",
        "value": None
    }


    if not text:
        return result



    # 统一小写，方便匹配
    source = text.lower()



    patterns = [

        # 98ms / 98 ms / 98MS
        r'(\d+(?:\.\d+)?)\s*ms',


        # 98毫秒
        r'(\d+(?:\.\d+)?)\s*毫秒',


        # ping=98
        r'ping\s*[=:]?\s*(\d+(?:\.\d+)?)',


        # latency:98
        r'latency\s*[=:]?\s*(\d+(?:\.\d+)?)',


        # delay=98
        r'delay\s*[=:]?\s*(\d+(?:\.\d+)?)',


        # time=98
        r'time\s*[=:]?\s*(\d+(?:\.\d+)?)',


        # RTT 98
        r'rtt\s*[=:]?\s*(\d+(?:\.\d+)?)',

    ]



    for pattern in patterns:

        match = re.search(
            pattern,
            source,
            re.IGNORECASE
        )


        if match:

            value = float(
                match.group(1)
            )


            # 如果是整数，不显示小数
            if value.is_integer():
                value = int(value)


            result["value"] = value

            result["latency"] = f"{value}ms"


            return result



    return result