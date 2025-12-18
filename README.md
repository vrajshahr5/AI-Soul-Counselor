AI Soul Counselor

AI Soul Counselor is a production-grade, backend-first AI system that creates a personalized AI companion for each user, combining Retrieval-Augmented Generation (RAG), long-term memory, and configurable personality profiles.

Each user interacts with a private AI Soul that evolves over time through stored memory and personalized prompt injection.

🚀 Core Capabilities

Per-user AI Souls with long-term memory

Retrieval-Augmented Generation (RAG) using user-specific vector databases

JWT-authenticated API with protected routes

Configurable AI personalities persisted per user

Production-ready FastAPI architecture

Dockerized deployment

🧠 Personalized AI Souls

Each user has a unique AI Soul whose behavior is defined by stored personality settings:

Tone (gentle, casual, formal, humorous)

Empathy level

Reasoning depth

Creativity level

Memory aggressiveness

Behavioral boundaries

These settings are injected into every LLM prompt, ensuring consistent and personalized responses.

🧠 RAG with Per-User Memory Isolation

Each user has a private ChromaDB vector store

Messages are:

Embedded

Stored in the user’s vector database

Retrieved during future conversations for contextual grounding

This guarantees:

No cross-user data leakage

Independent memory evolution per user

Scalable memory architecture

🔐 Security & Authentication

JWT-based authentication (OAuth2 Bearer)

Password hashing

Protected routes enforced at the dependency layer

Swagger UI authentication enabled

Protected endpoints require a valid token.

💬 AI Chat Flow

User authenticates

Message is saved to SQL database

Message is embedded and stored in vector memory

Relevant memories are retrieved

Prompt is built using:

Personality settings

Retrieved memories

User input

LLM generates response

Response is stored and returned

🧱 Backend Architecture

FastAPI with modular routers

SQLAlchemy ORM + Alembic migrations

Clean separation of concerns:

Auth

Chat

History

Soul settings

Custom OpenAPI schema

CORS-enabled

Designed for horizontal scalability

⚙️ Tech Stack
Backend

FastAPI

SQLAlchemy

Alembic

Pydantic

Uvicorn

AI / ML

LangChain

OpenAI

ChromaDB

Vector embeddings & retrieval

Security

JWT (OAuth2 Bearer)

Password hashing

Protected routes

Deployment

Docker

Render

AWS EC2 (compatible)

Railway (compatible)

🧪 API Documentation

Interactive Swagger UI available at:

/docs


After authentication, all protected endpoints can be tested directly.

🎯 Skills Demonstrated

Backend system design

REST API architecture

Secure authentication

Retrieval-Augmented Generation (RAG)

Per-user vector memory systems

Prompt engineering

Scalable AI infrastructure

Production deployment with Docker








