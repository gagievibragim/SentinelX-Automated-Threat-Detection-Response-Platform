import time
import urllib.request
import json

URL = "http://localhost:8000/api/events"

def send(payload):
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())

for i in range(6):
    send({
        "source": "linux",
        "event_type": "authentication_failure",
        "username": "admin",
        "source_ip": "185.123.45.10",
        "message": f"Failed password for admin from 185.123.45.10 attempt={i+1}",
    })

send({
    "source": "windows",
    "event_type": "process_execution",
    "username": "user1",
    "hostname": "WS-01",
    "message": "powershell.exe -EncodedCommand SQBFAFgA",
})

send({
    "source": "apache",
    "event_type": "web_request",
    "source_ip": "203.0.113.50",
    "message": "GET /index.php?id=1 UNION SELECT username,password FROM users",
})

for port in range(10):
    send({
        "source": "network",
        "event_type": "network_connection",
        "source_ip": "198.51.100.20",
        "message": f"connection attempt port={20+port}",
    })

send({
    "source": "linux",
    "event_type": "file_change",
    "message": "modified /etc/cron.d/backup",
})

print("Sample telemetry sent.")
