from __future__ import annotations
import os
import logging
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from app.models import ChatMessage, SoulSettings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage  
from sqlalchemy.orm import Session
from app.database import get_db
from app.vector_store import load_vector_store


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("CHAT_OPEN_AI", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("CHAT_OPEN_AI_TEMPERATURE", "0.3"))
RETRIEVER_K = int(os.getenv("RETRIEVER_MODEL_K", "6"))
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", "6"))
DATA_DIR = os.getenv("DATA_DIR", "data")


CONDENSE_QUESTION_PROMPT = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=(
        "Rewrite the follow-up question into a standalone, self-contained question.\n\n"
        "=== Chat history ===\n{chat_history}\n\n"
        "Follow-up question: {question}\n"
        "Standalone question:"
    ),
)


QA_PROMPT = PromptTemplate(
    input_variables=["context", "question", "personality"],
    template=(
        "{personality}\n"
        "=== Retrieved Context ===\n{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    ),
)



def user_chroma_dir(user_id: str) -> str:
    path = os.path.join(DATA_DIR, user_id, "chroma_db")
    os.makedirs(path, exist_ok=True)
    return path



def load_recent_chat_history(db: Session, user_id: int):
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.timestamp.desc())
        .limit(MAX_CHAT_HISTORY)
        .all()
    )

    rows = list(reversed(rows))  
    messages = []
    for msg in rows:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))

    return messages



def get_conversational_chain(user_id: str):
    persist_dir = user_chroma_dir(user_id)
    vectordb = load_vector_store(persist_dir=persist_dir)
    if not vectordb:
        raise RuntimeError(f"Vector store not found for user_id={user_id}")

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": RETRIEVER_K})

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
    )
    return chain



def get_response(user_input: str, user_id: str) -> str:
    db = next(get_db())

    
    settings = (
        db.query(SoulSettings)
        .filter(SoulSettings.user_id == int(user_id))
        .first()
    )

   
    if not settings:
        settings = SoulSettings(
            user_id=int(user_id),
            tone="gentle",
            empathy_level=5,
            reasoning_depth=7,
            creativity_level=5,
            memory_aggressiveness=5,
            boundaries="Respectful and supportive"
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    
    PERSONALITY = f"""
--- USER'S AI SOUL PERSONALITY ---
Tone: {settings.tone}
Empathy Level: {settings.empathy_level}/10
Reasoning Depth: {settings.reasoning_depth}/10
Creativity: {settings.creativity_level}/10
Memory Aggressiveness: {settings.memory_aggressiveness}/10
Boundaries: {settings.boundaries}

Follow these personality traits STRICTLY when responding.
--------------------------------
"""

    try:
        chain = get_conversational_chain(user_id)
        logger.info("Generating response for user_id=%s", user_id)

        history = load_recent_chat_history(db, int(user_id))

       
        result = chain.invoke({
            "question": user_input,
            "chat_history": history,
            "personality": PERSONALITY
        })

        answer = result.get("answer") or result.get("result") or "I couldn't generate a response."
        return answer

    except Exception as e:
        logger.error(f"Error generating response for user_id={user_id}: {e}")
        return "Sorry, something went wrong while generating a response."






    
       









    
    

    


    

    
    














