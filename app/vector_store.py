from __future__ import annotations
import os
from typing import Optional, Iterable
from datetime import date
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document


load_dotenv()

def _get_embeddings() -> OpenAIEmbeddings:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OpenAI API key not found")
    return OpenAIEmbeddings(api_key=api_key)

DATA_DIR = os.getenv("DATA_DIR", "data")

def user_chroma_dir(user_id: str) -> str:
    """Return per-user Chroma persist directory and make sure it exists."""
    path = os.path.join(DATA_DIR, user_id, "chroma_db")
    os.makedirs(path, exist_ok=True)
    return path

def load_vector_store(persist_dir:str)->Optional[Chroma]:
    """Load a Chroma vector store from disk, or return None if missing."""
    if not os.path.exists(persist_dir):
        return None
    return Chroma(persist_directory=persist_dir, embedding_function=_get_embeddings())

def embed_and_store(
        text: str,
        persist_dir: str,
        *,
        user_id: Optional[str]="default",
        chunk_size: int=1000,
        chunk_overlap: int=100,
)-> int:
    """
    Split text and persist to Chroma at persist_dir. Return the number of chunks needed.
    """
    os.makedirs(persist_dir, exist_ok=True)
    
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    
    ts = date.today().isoformat()
    documents: Iterable[Document] = (
        Document(page_content=chunk, metadata={"timestamp": ts, "user_id": user_id}) for chunk in chunks
    )

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=_get_embeddings(),
        persist_directory=persist_dir,
    )
    vectordb.persist()
    return len(chunks)


        



                



