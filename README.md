# 🧠 AI Soul Counselor
A personalized AI companion which is built with FastAPI, Langchain, ChromaDB, and JWT authentication. Each user has a unique AI soul that remembers conversations, stores long-term memory, and responds based on a customizable personality profile.

🚀 Overview
AI Soul Counselor creates a personalized AI Soul for every user

Each user gets
Their Own Long-term memory
Secure JWT authentication
A private vector database for storing conversations
RAG-powered responses with retrieval from user-specific memory
Fully modular FastAPI backend with scalable architeure

⭐ Key Features
Personal AI Soul(Per User Personality Engine)
Each user has configureable settings stored in DB:
-Tone(gentle,casual,formal,funny)
-Empathy level
-Reasoning depth
-Creativity Level
-Memory Aggressiveness
-Boundaries

These features are injected into every LLM prompt

🔒 JWT Authentication and Protected Routes

Users must authenticate through:
POST /auth/login
POST /auth/registar

Protected Routes:
/chat
/history
/soul/settings

No token means no access
Swagger authentication enabled

🧠 RAG with Per-User Vector Databases
- Each user gets their own persistant Chroma database:
DATA_DIR/<user_id>/chroma_db

When a message is sent:
-It is embedded 
-Stored in the user's vector DB
-Retrieved for context in future conversations
Overall this gives each user a unique evolving memory

💬 AI Chat with memory
-Chat messages are saved in a SQL database
-Vector search retrieves revelant memories
-AI responds using both memory + settings

🧱 Backend
- FastAPI modualar architecture
- SQLALchemy ORM
- Seperate routers for auth, chat, history and personality settings
- Custom OpenAPI schema
- CORS enabled
- Scalability built in

⚙️ Tech Stack
Backend Side
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn

AI/ML
- Langchain
- OpenAI
- ChromaDB
- Vector Storage + Embeddings

Security
- JWT(OAuth2 Bearer)
- Password Hashing
- Protected routes

Database
- SQlite(dev)

📁 Project Structure
- auth_dependency.py
- auth.py
- chains.py
- database.py
- main.auth.py
- main.py
- models.py
- o.models.py
- protected_routes.py
- routes_chat.py
- routes_history.py
- routes_soul.py
- schemas.py
- utilites.py
- vector_store.py

🔑 API Endpoints
🔒 Authentication
Method              Route                  Description
Post                /auth/registar         Registar a new user
Post                /auth/login            Login and get JWT token

💬 Chat
Method              Route                  Description
Post                /chat                  Send message to AI Soul

🗺️ History
Method              Route                  Description
Get                /history                Get User Chat Memory
Post               /history                Add history 
Delete             /history                Clear history

Soul Settings       Route                  Description
Get                /soul/settings          Get personality settings
Put                /soul/settings          Update personality settings

🧪Testing(Swagger UI)
Run: uvicorn main:app --reload
Open: http//localhost:8000/docs

Once Authorized you paste your token and have full access to all endpoints.

☀️How the System Works
1) User registars/login
-> JWT generated

2) User sends a message
-> Saved in DB
-> Embedded & stored in user vector DB
-> Prompt built using
- personality settings
- recent chat history
- vector-retrieved memories

3) AI Soul Responds
- Response saved
- Memory updated
- Returned to user

Skills Demonstrated

This project demonstrates real-world engineering skills in

Backend Engineering
- REST API architecture
- Modular Routing
- OAuth2/JWT
- Dependency 
- Database design
- ORM Modeling

AI Engineering
- RAG pipelines
- prompt engineering
- Retrieval chains
- Vector search
- Memory encoding
- Per-user AI models

Security
- JWT Auth
- protected user data
- password hashing

Project Architecture
- Personalized AI
- User isolation
- Scaleable design

🚀 Deployment Ready
- AWS EC2
- Docker
- render
- Railway

Frontend can be
- React
- Node.js
- HTML/JS































