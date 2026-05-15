# Telegram CRM

A web application for managing Telegram bot messages. Operators can receive and reply to messages through a real-time dashboard.

## Tech Stack

**Backend:** Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, WebSocket  
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
3. Run ngrok: `ngrok http 8000`
4. Go to **Settings** on the website
5. Paste the bot token and click **Save**
6. Paste the ngrok URL into the Webhook URL field
7. Click **Register Webhook**
8. Send a message to your bot in Telegram — it will appear in real-time

## Features

- JWT authentication
- Real-time chat via WebSocket
- Auto-create contacts on first message
- Reply to users directly from the dashboard
- Contact list with message history
- Webhook and bot token management

## Project Structure
tg-crm/
├── backend/          # FastAPI application
├── frontend/         # React application
├── docker-compose.yml
└── README.md

## Requirements

- Docker Desktop
- ngrok (for webhook testing
