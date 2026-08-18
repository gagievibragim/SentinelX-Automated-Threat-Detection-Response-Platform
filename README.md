# SentinelX

**Automated Threat Detection & Response Platform**

SentinelX is a runnable security monitoring platform for ingesting security events, normalizing them, applying YAML detection rules, calculating risk, mapping detections to MITRE ATT&CK, and creating incidents through a FastAPI API.

> This repository is a real software project, not a collection of incident-response writeups. It is designed to run locally with Docker Compose.

## Architecture

```text
Security Events
      |
      v
+-------------+
|  FastAPI    |
|  /events    |
+------+------+
       |
       v
+------------------+
| Normalizer       |
+--------+---------+
         |
         v
+------------------+
| Detection Engine |
| YAML rules       |
+--------+---------+
         |
    +----+----+
    |         |
    v         v
 Scoring   MITRE ATT&CK
    |         |
    +----+----+
         |
         v
+------------------+
| Incident Manager |
+--------+---------+
         |
         v
 PostgreSQL
         |
         v
 Dashboard / API
```

## Features

- FastAPI REST API
- PostgreSQL persistence
- Redis-backed Celery worker
- YAML detection rules
- Detection engine with rule conditions
- Risk scoring
- MITRE ATT&CK technique mapping
- Incident creation
- IOC extraction and storage
- Basic IP enrichment interface
- Security dashboard
- Linux auth, Windows event and Apache log normalization
- Docker Compose deployment
- Automated pytest test suite
- GitHub Actions CI
- Sample attack telemetry
- Health and readiness endpoints

## Detection coverage

Included rules cover:

| Rule | Detection | MITRE |
|---|---|---|
| SSH brute force | Repeated SSH authentication failures | T1110.001 |
| Windows brute force | Repeated Windows logon failures | T1110 |
| PowerShell | Suspicious encoded/hidden PowerShell | T1059.001 |
| Port scan | Repeated connection attempts to many ports | T1046 |
| Privilege escalation | `sudo` / privilege-related events | T1548 |
| Suspicious process | Shell spawned by unusual parent | T1059 |
| Web attack | SQL injection / path traversal indicators | T1190 |
| Suspicious download | Script/binary downloaded from remote URL | T1105 |
| Persistence | Cron / startup modification | T1053 |
| Impossible travel | Distant logins in an unrealistic interval | T1078 |

## Quick start

### Requirements

- Docker Desktop
- Docker Compose
- Git

### Run

```bash
git clone https://github.com/gagievibragim/SentinelX-Automated-Threat-Detection-Response-Platform.git
cd sentinelx
docker compose up --build
```

Open:

- Dashboard: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Generate sample detections

```bash
docker compose exec api python scripts/generate_demo_events.py
```

Then refresh the dashboard.

## API examples

Create an event:

```bash
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "source": "linux",
    "event_type": "authentication_failure",
    "username": "admin",
    "source_ip": "185.123.45.10",
    "message": "Failed password for admin from 185.123.45.10"
  }'
```

List incidents:

```bash
curl http://localhost:8000/api/incidents
```

Get statistics:

```bash
curl http://localhost:8000/api/stats
```

## Project structure

```text
sentinelx/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── api/
│   │   ├── events.py
│   │   ├── incidents.py
│   │   └── stats.py
│   ├── detection/
│   │   ├── engine.py
│   │   ├── loader.py
│   │   └── rules/
│   ├── ingestion/
│   │   ├── normalizer.py
│   │   └── parsers.py
│   ├── enrichment/
│   │   └── ioc.py
│   └── response/
│       └── manager.py
├── dashboard/
├── scripts/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/ci.yml
```

## Security design

SentinelX intentionally does not perform destructive host actions by default. Automated response is represented as an auditable action recommendation. Production deployments should place real containment actions behind authentication, authorization, approvals, and environment-specific integrations.

## Configuration

Copy `.env.example` to `.env` when running outside the default Compose configuration.

Important settings:

```text
DATABASE_URL
REDIS_URL
RULES_PATH
RISK_THRESHOLD
```

## Testing

```bash
pip install -r requirements.txt
pytest -q
```

## CI

GitHub Actions runs:

- Python syntax/import checks
- pytest
- API smoke tests

## License

MIT

Author: Ibragim