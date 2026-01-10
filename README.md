AI Soul Counselor
-
AI Soul Counselor is a production-grade, backend-first AI system that creates a personalized AI companion for each user, combining Retrieval-Augmented Generation (RAG), long-term memory, and configurable personality profiles.Each user interacts with a private AI Soul that evolves over time through stored memory and personalized prompt injection.

Problem Statement
-
Long term context is critical for individuals looking for AI assisted coaching or counseling. This long term ontext relates to recurring concerns and worries, established goals and objectives, and a user's customized preferences. Most chat systems of LLMs operate only on a session basis without any saved information. As a result, those chat systems cannot allow for secure integration of user emotional context from previous chats and therefore hinder progress through consecutive conversations. 

AI Soul Counselor was created to solve this exact problem 
- 
+ Structured long term conversation memory
+ Deterministic personality enforcement
+ Strict per-user data isolation

Core Capabilites 
+ Per-user AI Soul with independent memory evolution
+ Retrieval-Augmented Generation powered by OpenAI embeddings
+ Private ChromaDB vector stores per account
+ JWT-authenticated API with OAuth2 Bearer security
+ Password hasing and protected route enforcement
+ Conversation History in PostSQL Lite
+ Dockerized deployment for cloud platforms
+ FastAPI architecture

RAG with Per-User Memory Isolation
-
All conversations are stored in a relational database and mirrored into ChromaDB as embeddings. Retrieval is only executed with authenticated user scope, which ensures privacy and Independent companions.

Chat Flow
-
1) User authentication
2) Message saved to SQL database
3) Embedding generated and stored
4) Relevant memories retrieved
5) Prompt constructed using:
   + persisted personality settings
   + Retrieved Historical context
   + Current user input
6) LLM generates response
7) Response stored and returned

Backend Archeticture
![IMG_3580](https://github.com/user-attachments/assets/61f5830e-c25d-44e4-9e5d-311f283aa435)


Design Principles
-
+ Modular routers with dependency layer security
+ SQLAchemy ORM and Alembic migrations
+ Service oriented AI integration
+ Extensible OpenAPI schema

Technology Stack
-
Backend
-
+ FastAPI
+ SQLAlchemy
+ Alembic
+ Pydantic
+ Uvicorn

AI/ML
-
+ Langchain
+ OpenAI
+ ChromaDB
+ Vector embeddings & RAG

Security
-
+ OAuth2 Bearer JWT
+ Protected routes
+ Paswword Hashing

Deployment
- 
+ Containerized with Docker
+ Hosted on Render Web Service
+ Enviornment configured with PostgreSQL Lite and ChromaDB
+ Live API accessible at: https://ai-soul-counsler.onrender.com/

API Documentation/Example
-
The FastAPI backend provides an interactive Swagger UI for live endpoint testing at /docs. Authentication is supported directly in Swagger using JWT Bearer tokens.
The publicly deployed API dcoumentation can be accessed at https://ai-soul-counsler.onrender.com/docs, Use this link to explore and test all avaliable endpoints directly from your browser.

Local Development Documentation
-
After Running the server locally, the same documentation is avaliable at: http://127.0.0.1:8000/docs

#### Example cURL Request
```
curl -X 'POST' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <jwt_token>' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Tell me something about my last message"
}'
```

#### Sample Successful Response

```json
{
  "response": "It sounds like you're feeling quite overwhelmed about your exam. It's completely normal to experience stress in situations like this. If you'd like, we can talk about some strategies to help manage that stress or ways to prepare effectively. What do you think?",
  "user_id": 24,
  "metadata": null
}
```
### Response Codes

- `200 OK` – Request processed successfully  
- `401 Unauthorized` – JWT token missing or invalid  
- `422 Validation Error` – Incorrect request format  
- `500 Server Error` – Internal processing issue  

---

Installation Steps
-
Clone the Repository

Open your terminal and run:

git clone https://github.com/vrajshahr5/AI-Soul-Counselor.git
cd AI-Soul-Counselor

### Create and Activate Virtual Environment

Create a virtual environment:

python -m venv venv

Activate it using the command for your operating system:

- macOS / Linux:
  source venv/bin/activate

- Windows Command Prompt:
  venv\Scripts\activate

- Windows PowerShell:
  .\venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Configure Environment Variables

Create a file named `.env` in the project root directory with the following contents:

OPENAI_API_KEY=your_openai_key  
JWT_SECRET_KEY=your_secret_key  
DATABASE_URL=sqlite:///./app.db  
CHROMADB_PATH=./chroma  

Replace `your_openai_key` and `your_secret_key` with your actual credentials.

### Run Alembic Migrations

alembic upgrade head

### Start the Backend Server

uvicorn app.main:app --reload

### Access the API

Once the server is running, open your browser and navigate to:

http://127.0.0.1:8000/docs

The interactive API documentation will be available at this address.

---

## Docker Deployment (Local Simulation)

### Build Docker Image

docker build -t ai-soul-counselor .

### Run Docker Container

docker run -p 8000:8000 --env-file .env ai-soul-counselor

This simulates deployment locally using Docker.

---





