import re
from datetime import datetime, timezone

def normalize_linux_auth(line: str) -> dict:
    ip = re.search(r"from\s+(\d+\.\d+\.\d+\.\d+)", line)
    user = re.search(r"for (?:invalid user )?([A-Za-z0-9._-]+)", line)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "linux",
        "event_type": "authentication_failure" if "Failed password" in line else "authentication_success",
        "username": user.group(1) if user else None,
        "source_ip": ip.group(1) if ip else None,
        "message": line,
        "raw": {"parser": "linux_auth"},
    }

def normalize_windows_event(event: dict) -> dict:
    return {
        "timestamp": event.get("timestamp"),
        "source": "windows",
        "event_type": event.get("event_type", "unknown"),
        "username": event.get("username"),
        "source_ip": event.get("source_ip"),
        "hostname": event.get("hostname"),
        "message": event.get("message"),
        "raw": event,
    }

def normalize_apache(line: str) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "apache",
        "event_type": "web_request",
        "message": line,
        "raw": {"parser": "apache"},
    }
