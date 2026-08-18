def recommended_action(severity: str, rule_id: str) -> dict:
    actions = {
        "CRITICAL": "Isolate affected host and begin incident response.",
        "HIGH": "Investigate immediately; consider temporary containment.",
        "MEDIUM": "Review correlated telemetry and validate the detection.",
        "LOW": "Monitor and collect additional context.",
    }
    return {
        "rule_id": rule_id,
        "recommended_action": actions.get(severity, actions["MEDIUM"]),
        "automated_execution": False,
    }
