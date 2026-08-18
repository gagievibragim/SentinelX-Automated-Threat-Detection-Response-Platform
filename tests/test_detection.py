from pathlib import Path
from app.detection.engine import DetectionEngine

RULES = str(Path(__file__).resolve().parents[1] / "app" / "detection" / "rules")

def test_powershell_detection():
    engine = DetectionEngine(RULES)
    matches = engine.evaluate({
        "source": "windows",
        "event_type": "process_execution",
        "message": "powershell.exe -EncodedCommand AAAA",
        "source_ip": "203.0.113.1",
    })
    assert any(x["id"] == "POWERSHELL-SUSPICIOUS" for x in matches)

def test_web_attack_detection():
    engine = DetectionEngine(RULES)
    matches = engine.evaluate({
        "source": "apache",
        "event_type": "web_request",
        "message": "GET /?id=1 UNION SELECT password FROM users",
        "source_ip": "203.0.113.1",
    })
    assert any(x["id"] == "WEB-ATTACK" for x in matches)

def test_ssh_bruteforce():
    engine = DetectionEngine(RULES)
    for _ in range(5):
        matches = engine.evaluate({
            "source": "linux",
            "event_type": "authentication_failure",
            "username": "root",
            "source_ip": "203.0.113.9",
            "message": "Failed password for root",
        })
    assert any(x["id"] == "SSH-BRUTE-FORCE" for x in matches)
