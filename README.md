# OuterEye API
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white) 
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 
![DeepSeek](https://img.shields.io/badge/DeepSeek-%235786FE.svg?style=for-the-badge&logo=deepseek&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white) 
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) 

An API that uses AI to analyze player actions in Minecraft and influence the state of the server. It is designed to accept requests from a local Minecraft server, which sends notifications about player actions through the API endpoints, and to return instructions to the server based on the analysis of those actions.

![Architecture schema](Schema.jpg)

## Features
- Player action tracking
- Player position and inventory tracking
- AI-powered player behaviour analysis
- AI-generated gameplay responses
- REST API for Minecraft integration
- Docker-based deployment
- Configurable AI prompts

## How it works
First, the Minecraft server detects a player action and sends it to OuterEye through the REST API. OuterEye validates the received data and stores it in PostgreSQL.

When the Minecraft server requests an analysis of the player's actions, OuterEye collects the required context from PostgreSQL and compresses it into a structured, readable, and cost-efficient prompt containing the player's recent history. This prompt is then sent to the AI provider.

The AI analyzes the player's recent activity and returns instructions in JSON format. OuterEye processes the response and sends the instructions back to the Minecraft server.

## Quick start

There are two ways to run OuterEye

Before running OuterEye, make sure you have Docker, an AI API key, and the required prompts.

### Quick full launch 

This option is recommended if you want to start a Minecraft server with OuterEye using a single command and DeepSeek.

At first, clone the GitHub repository:

```bash
git clone https://github.com/saszastanczyk/OuterEyeAPI.git
cd OuterEyeAPI
```

Then open `docker-compose.yaml` and configure the following environment variables:

| Variable                  | Description                               |
|---------------------------|-------------------------------------------|
| `POSTGRES_PASSWORD`       | PostgreSQL password                       |
| `DATABASE_PASSWORD`       | Password from previous variable           |
| `AI_SECRET_KEY`           | DeepSeek API key                          |
| `AI_ANALYSIS_PROMPT`      | Prompt used for player behaviour analysis |
| `AI_PRAY_PROMPT`          | Prompt used for prayer responses          |
| `AI_ANALYSIS_TEMPERATURE` | Temperature for analysis                  |
| `AI_PRAY_TEMPERATURE`     | Temperature for prayer responses          |

After this launch the whole system

```bash
docker compose up
```

The server will be available on `127.0.0.1:7777`. Open Minecraft, add your server to the servers list and enjoy

## Quick core launch

This option is better if you want to use custom Minecraft server with your own plugin

Clone GitHub repository:

```bash
git clone https://github.com/saszastanczyk/OuterEyeAPI.git
cd OuterEyeAPI
```

Open `docker-compose.core.yaml` and configure following environmental variables (just as in [Full Launch](#quick-full-launch-))

| Variable                  | Description                               |
|---------------------------|-------------------------------------------|
| `POSTGRES_PASSWORD`       | PostgreSQL password                       |
| `DATABASE_PASSWORD`       | Password from previous variable           |
| `AI_SECRET_KEY`           | DeepSeek API key                          |
| `AI_ANALYSIS_PROMPT`      | Prompt used for player behaviour analysis |
| `AI_PRAY_PROMPT`          | Prompt used for prayer responses          |
| `AI_ANALYSIS_TEMPERATURE` | Temperature for analysis                  |
| `AI_PRAY_TEMPERATURE`     | Temperature for prayer responses          |

Then launch the configured OuterEyeAPI:

```bash
docker compose -f docker-compose.core.yaml up
```

OuterEyeAPI will be available on `127.0.0.1:8088`

## Project Structure

```text
OuterEye/
├── app/                              # Main FastAPI application
│   ├── routes/                       # HTTP API endpoints
│   │   ├── __init__.py
│   │   ├── actions_notification.py   # Player action notifications
│   │   ├── analysis_requests.py      # Requests for AI analysis
│   │   └── scan_notification.py      # Player state/scan notifications
|   |
│   ├── src/                          # Application core
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   │   ├── notifications.py      # Notification schemas
│   │   │   ├── requests.py           # API request schemas
│   │   │   ├── response_data.py      # API response schemas
│   │   │   └── user_data.py          # User-related schemas
│   │   ├── __init__.py
│   │   ├── auth.py                   # User identification from X-Username header
│   │   ├── database.py               # Database engine and session management
│   │   ├── models.py                 # SQLAlchemy ORM models
│   │   ├── open_ai.py                # LLM/AI integration with openai SDK
│   │   └── services.py               # Application and database services
│   │
│   ├── __init__.py
│   ├── main.py                       # FastAPI application entry point
│   ├── Dockerfile                    # Docker image for the API
│   └── requirements.txt              # Python dependencies
│   
├── database/
│   ├── Dockerfile                     # Database container configuration
│   └── init.sql                       # Initial database schema
│
├── tests/
│   ├── test_actions.py                # Action endpoint tests
│   ├── test_requests.py               # Analysis/request endpoint tests
│   ├── test_scans.py                  # Scan endpoint tests
│   ├── requirements.txt               # Test dependencies
│   └── __init__.py

├── docker-compose.core.yaml           # Docker compose for OuterEye core only
├── docker-compose.yaml                # Docker compose for OuterEye with Minecraft server
├── README.md                          # Project documentation
└── .gitignore                         # Git ignored files
```

## Endpoints

| Method | Path | Description                                                                                 | Request Body                                                                                                                 | Successful response                   |
|---|---|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| `POST` | `/action/meal` | Record a meal action                                                                        | `position: {pos_x, pos_y, pos_z}`, `meal_name: str`                                                                          | `"status":"created"`                  |
| `POST` | `/action/craft` | Record a crafting action                                                                    | `position`, `craft_subject: str`, `craft_amount: int`                                                                        | `"status":"created"`                  |
| `POST` | `/action/kill` | Record a kill action                                                                        | `position`, `kill_type: str`, `kill_tool: str`, `kill_subject: UUID \| null` (optional), `kill_name: str \| null` (optional) | `"status":"created"`                  |
| `POST` | `/action/breed` | Record a breeding action                                                                    | `position`, `father_subject_id: UUID`, `mother_subject_id: UUID`, `child_subject_id: UUID`, `child_type: str`                | `"status":"created"`                  |
| `POST` | `/action/death` | Record a death action                                                                       | `position`, `death_cause: str`                                                                                               | `"status":"created"`                  |
| `POST` | `/action/pray` | Record a prayer and get an AI-generated response                                            | `position`, `pray_text: str`                                                                                                 | `"pray_respond":pray_response`        |
| `POST` | `/scan/position` | Record a position scan                                                                      | `pos_x: int`, `pos_y: int`, `pos_z: int`                                                                                     | `"status":"created"`                  |
| `POST` | `/scan/inventory` | Record an inventory scan                                                                    | `items: [{name: str, amount: int}, ...]`                                                                                     | `"status":"created"`                  |
| `GET` | `/analysis/scenario` | Get an AI-generated analysis of the user's recent actions/scans and instructions for server | — (no body, uses `CurrentUser` from X-Username header)                                                                       | `"analysis_respond":instruction_json` |

All endpoints require the `X-Username` header, which provides the nickname — a missing or invalid header results in `401`/`403`.





