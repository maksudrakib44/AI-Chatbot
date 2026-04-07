# AI Chatbot API

A production-ready conversational AI chatbot with persistent memory, built with FastAPI and Google's Gemini API.

## Video Demonstration

[INSERT YOUTUBE OR GOOGLE DRIVE LINK HERE]

## Features

- Multi-turn conversation with context memory
- Session isolation (different users don't interfere)
- RESTful API with FastAPI
- Docker containerization
- Thread-safe in-memory storage
- Automatic API documentation (Swagger UI)
- Health checks and error handling
- Session management (create, read, clear, delete)

## Technology Stack

- Framework: FastAPI (Python 3.11)
- AI Model: Google Gemini Pro (Free)
- Memory: In-memory dictionary (thread-safe)
- Container: Docker + Docker Compose

## Prerequisites

- Python 3.11 or higher
- Docker Desktop (optional, for containerized deployment)
- Git
- Google Gemini API key (free)

## Quick Start (5 minutes)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-chatbot-task