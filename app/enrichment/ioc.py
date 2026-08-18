import ipaddress
import re

def extract_iocs(text: str) -> list[tuple[str, str]]:
    results = []
    for ip in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text or ""):
        try:
            ipaddress.ip_address(ip)
            results.append(("ip", ip))
        except ValueError:
            pass
    for domain in re.findall(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", text or ""):
        results.append(("domain", domain))
    return list(dict.fromkeys(results))

def reputation(ip: str) -> str:
    # Safe offline default. Replace with a threat-intelligence provider in production.
    if ip.startswith(("10.", "192.168.", "172.16.")):
        return "private"
    return "unknown"
