# Telegram CRM

A web application for managing Telegram bot messages. Operators can receive and reply to messages through a real-time dashboard.

The project also supports AI auto-replies through OpenRouter. When enabled, the system can generate and send responses automatically instead of waiting for a human operator.

## Tech Stack

**Backend:** Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, WebSocket, Alembic, httpx  
**Frontend:** React 18, TypeScript, TailwindCSS, Flowbite, Zustand  
**Infrastructure:** Docker, docker-compose, nginx

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/senozinesensei/tg-crm.git
cd tg-crm
```

### 2. Start the project

```bash
docker-compose up --build
```

### 3. Open your browser

http://localhost:3000

**Login:** admin@admin.com  
**Password:** admin123

## Telegram Bot Setup

1. Create a bot via @BotFather in Telegram
2. Copy the bot token
3. Run ngrok:

```bash
ngrok http 8000
```

4. Go to **Settings** on the website
5. Paste the bot token and click **Save**
6. Paste the ngrok URL into the Webhook URL field
7. Click **Register Webhook**
8. Send a message to your bot in Telegram - it will appear in real-time

## OpenRouter AI Auto-Reply Setup

1. Create an OpenRouter account at https://openrouter.ai
2. Create and copy an OpenRouter API key
3. Go to **Settings** on the website
4. Find the **OpenRouter AI Auto-Reply** section
5. Paste the OpenRouter API key
6. Enter the model name, for example:

```text
openai/gpt-4o-mini
```

7. Edit the system prompt
8. Set how many recent messages should be sent to AI as chat history
9. Enable **AI auto-reply**
10. Click **Save OpenRouter Settings**

When AI auto-reply is enabled, every incoming Telegram message will be sent to OpenRouter with the configured system prompt and recent chat history. The generated AI response will be saved in the database, displayed in the chat in real-time, and sent back to the user through Telegram Bot API.

## Features

- JWT authentication
- Real-time chat via WebSocket
- Auto-create contacts on first message
- Reply to users directly from the dashboard
- Contact list with message history
- Webhook and bot token management
- OpenRouter AI auto-reply
- Editable AI system prompt
- Configurable OpenRouter model
- Configurable AI chat history length
- Enable/disable AI auto-reply without restarting the app

## Project Structure

```text
tg-crm/
|-- backend/          # FastAPI application
|-- frontend/         # React application
|-- scripts/          # Helper scripts
|-- docker-compose.yml
`-- README.md
```

## Requirements

- Docker Desktop
- ngrok (for webhook testing)
- Telegram bot token
- OpenRouter API key (only if AI auto-reply is used)

## Useful Commands

Start the project:

```bash
docker-compose up --build
```

Start in background:

```bash
docker-compose up -d --build
```

Stop the project:

```bash
docker-compose down
```

View backend logs:

```bash
docker-compose logs -f backend
```

Run database migrations:

```bash
docker-compose exec backend alembic upgrade head
```

## Environment Variables

Example `.env`:

```env
POSTGRES_USER=tgcrm
POSTGRES_PASSWORD=tgcrm_secret
POSTGRES_DB=tgcrm
DATABASE_URL=postgresql+asyncpg://tgcrm:tgcrm_secret@db:5432/tgcrm
SECRET_KEY=change-me-to-a-random-64-character-string-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

Do not commit real bot tokens, OpenRouter API keys, or production secrets.
