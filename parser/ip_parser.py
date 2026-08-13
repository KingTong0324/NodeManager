import re

def parse_ip(text):
    """
    解析IP和端口（向后兼容接口）：返回第一个匹配或 None
    """
    result = {
        "ip": "",
        "port": ""
    }

    # 匹配 [IPv6]:端口
    ipv6_match = re.search(
        r'\[([0-9a-fA-F:]+)\](?::|,|=|\s+)(\d{2,5})',
        text
    )

    if ipv6_match:
        result["ip"] = ipv6_match.group(1)
        result["port"] = ipv6_match.group(2)
        return result

    # 匹配 IPv4
    ip_match = re.search(
        r'(\d{1,3}(?:\.\d{1,3}){3})',
        text
    )

    if ip_match:
        result["ip"] = ip_match.group(1)
        port_match = re.search(
            r'(?:[:|,=\s]+)(\d{2,5})',
            text[ip_match.end():]
        )
        if port_match:
            result["port"] = port_match.group(1)
            return result

    # 匹配 IPv6 + 端口（支持 :: 压缩格式）
    ipv6_match = re.search(
        r'([0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{0,4}){2,}):(\d{2,5})(?=#|[|,\s]|$)',
        text
    )

    if ipv6_match:
        result["ip"] = ipv6_match.group(1)
        result["port"] = ipv6_match.group(2)
        return result

    return None


def parse_ips(text):
    """
    返回行中所有匹配的 (ip, port) 字典列表，例如:
    [{"ip": "2001:db8::1", "port": "443"}, {"ip": "1.2.3.4", "port": "8080"}, ...]
    尽量避免重复匹配同一片段。
    """
    results = []
    used_spans = []

    # 1) 带中括号的 IPv6 [2001:db8::1]:443
    for m in re.finditer(r'\[([0-9a-fA-F:]+)\](?::|,|=|\s+)(\d{2,5})', text):
        span = m.span()
        used_spans.append(span)
        results.append({"ip": m.group(1), "port": m.group(2)})

    # 2) 非中括号的 IPv6:port（较长的带冒号序列，避免匹配日期或时间）
    for m in re.finditer(r'([0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{0,4}){2,}):(\d{2,5})(?=#|[|,\s]|$)', text):
        span = m.span()
        # 跳过已被中括号匹配覆盖的片段
        if any(s <= span[0] < e or s < span[1] <= e for s, e in used_spans):
            continue
        used_spans.append(span)
        results.append({"ip": m.group(1), "port": m.group(2)})

    # 3) IPv4:port（或 IPv4 后跟端口）
    for m in re.finditer(r'(\d{1,3}(?:\.\d{1,3}){3})', text):
        start, end = m.span()
        # 跳过落在已使用 span 内的
        if any(s <= start < e or s < end <= e for s, e in used_spans):
            continue
        # 在 IPv4 后面找端口（允许分隔符 : , = 空格 等）
        tail = text[end:end+20]
        port_m = re.search(r'(?:[:|,=\s]+)(\d{2,5})', tail)
        if port_m:
            results.append({"ip": m.group(1), "port": port_m.group(1)})
            used_spans.append((start, end + port_m.end()))

    return results
