from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta
from app.detection.loader import load_rules

class DetectionEngine:
    def __init__(self, rules_path: str):
        self.rules = load_rules(rules_path)
        self.history = defaultdict(deque)

    def evaluate(self, event: dict) -> list[dict]:
        matches = []
        now = datetime.now(timezone.utc)
        key = event.get("source_ip") or event.get("username") or "global"
        self.history[key].append((now, event))
        self._trim(key, now)

        for rule in self.rules:
            if self._match(rule, event, self.history[key]):
                matches.append(rule)
        return matches

    def _trim(self, key, now):
        cutoff = now - timedelta(minutes=15)
        q = self.history[key]
        while q and q[0][0] < cutoff:
            q.popleft()

    def _match(self, rule, event, history) -> bool:
        cond = rule.get("condition", {})
        if cond.get("event_type") and event.get("event_type") != cond["event_type"]:
            return False
        for field, expected in cond.get("equals", {}).items():
            if event.get(field) != expected:
                return False
        text = (event.get("message") or "").lower()
        for needle in cond.get("contains_any", []):
            if needle.lower() in text:
                break
        elif cond.get("contains_any"):
            return False

        threshold = cond.get("count")
        if threshold:
            window = cond.get("window_minutes", 5)
            now = datetime.now(timezone.utc)
            recent = [e for ts, e in history if now - ts <= timedelta(minutes=window)]
            if cond.get("event_type"):
                recent = [e for e in recent if e.get("event_type") == cond["event_type"]]
            if len(recent) < threshold:
                return False

        return True
