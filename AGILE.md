# Agile Development & Sprint Planning

This project was built following Agile/Scrum methodology with 4 iterative sprints.

---

## 📋 Product Backlog & User Stories

| ID | User Story | Effort (Story Points) | Sprint | Status |
|:---|:---|:---:|:---:|:---:|
| **US-1** | As a user, I want to view a 5-day weather forecast for any city so I can plan my week. | 5 pts | Sprint 1 | ✅ Done |
| **US-2** | As a user, I want to save and delete favorite addresses so I can access them quickly. | 3 pts | Sprint 1 | ✅ Done |
| **US-3** | As a developer, I want unit tests with >70% coverage to prevent regressions. | 5 pts | Sprint 2 | ✅ Done |
| **US-4** | As a DevOps engineer, I want Docker containerization for consistent deployment. | 3 pts | Sprint 3 | ✅ Done |
| **US-5** | As a team, we want automated linting (Flake8) and security scanning (Bandit) for code quality. | 2 pts | Sprint 3 | ✅ Done |
| **US-6** | As a DevOps engineer, I want Docker Compose for multi-container orchestration. | 3 pts | Sprint 4 | ✅ Done |

---

## 📊 Kanban Board Layout

| TO DO (0) | IN PROGRESS (0) | IN REVIEW (0) | DONE (6) |
|-----------|-----------------|---------------|----------|
|           |                 |               | [US-1] Weather API |
|           |                 |               | [US-2] Address Mgr |
|           |                 |               | [US-3] Unit Tests |
|           |                 |               | [US-4] Dockerfile |
|           |                 |               | [US-5] Flake8/Bandit|
|           |                 |               | [US-6] Docker Compose|

---

## 🔄 Sprint Retrospectives (Bonus 6a)

### Sprint 1 Retrospective (Core App & API)
- **What went well:** Fast implementation of OpenWeatherMap integration and address CRUD.
- **What could be improved:** Hardcoded port 5000 collided with macOS AirPlay receiver.
- **Action item:** Added environment variable `PORT` to allow dynamic port selection.

### Sprint 2 Retrospective (Testing & Coverage)
- **What went well:** Mocking the OpenWeatherMap API allowed tests to run offline without consuming API quota.
- **What could be improved:** Initial test suite only covered modules (67%), leaving Flask routes uncovered.
- **Action item:** Added Flask `test_client()` integration tests, bringing coverage to 88.37%.

### Sprint 3 Retrospective (Docker & Security)
- **What went well:** Docker container built smoothly using Python slim base image.
- **What could be improved:** Bandit flagged `host="0.0.0.0"` in development mode.
- **Action item:** Modified `app.py` to default to `127.0.0.1` locally, and allow `0.0.0.0` inside containers.

### Sprint 4 Retrospective (Orchestration & Final Polish)
- **What went well:** Docker Compose unified port mapping and API key configuration.
- **What could be improved:** Dependency freeze contained too many transitive dependencies.
- **Action item:** Kept clean `requirements.txt` for production and `requirements_full.txt` for auditing.