from __future__ import annotations
import os
import json
import argparse
import requests
from datetime import datetime
from pathlib import Path
from typing import List,Dict,Any,Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()

def join_url(*parts: str) -> str:
    clean = []
    for i, p in enumerate(parts):
        if p is None:
            continue
        s=str(p)
        if i ==0:
            clean.append(s.strip("/"))
        else:
            clean.append(s.strip("/"))
    return "/".join(clean)

def login(login_url: str, username: str, password: str) -> str:
    # FastAPI OAuth2PasswordRequest Form expects x-www-form-url-encoded
    data = {
        "username": username,
        "password": password,
        "grant_type": password,
        "scope": "",
        "client_id": "",
        "client_secret" : "",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(login_url, data=data, headers=headers, timeout=30)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise SystemExit(f"Login failed ({r.status_code}): {r.text}") from e
    token = r.json().get("access_token")
    if not token:
        raise SystemExit(f"Login response missing access_token: {r.text}")
    return token

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1,max=8))
def send_chat(
    chat_url: str, 
    token: str,
    *, 
    user_id: Optional[str], 
    text: str, 
    history: Optional[List[Dict[str,Any]]] = None
)-> str:

    """ Send the chat and reply to the server and return the response """
    headers={"Authorization":f"Bearer {token}", "Content-Type": "application/json"}
    payload: Dict[str,Any] ={"message":text}
    if user_id:
        payload["user_id"]=user_id,
    if history:
        payload["history"]=history,
    r = requests.post(chat_url, headers=headers, json=payload, timeout=60)

    r.raise_for_status()
    data=r.json()

    "Response Field name from server"

    response=data.get("response") or data.get("message")
    if not response:
        raise RuntimeError(f"Unexpected response {data}")
    return response

def history_path(user_id:Optional[str],base_dir:str="history")->Path:
    uid=user_id or "default"
    p=Path(base_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p / f"{uid}_chat_history.json"

def load_history(user_id:Optional[str],base_dir:str="history")->List[Dict[str,Any]]:
    p=history_path(user_id,base_dir)
    if not p.exists():
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            data=json.load(f)
            return data if isinstance(data,list) else[]
    except Exception:
        backup=p.with_suffix(".bak")
        try:
            p.replace(backup)
        except Exception:
            pass
        return []
    
def save_history(user_id:Optional[str], history:List[Dict[str,Any]],base_dir: str="history")->None:
    p=history_path(user_id,base_dir)
    backup=p.with_suffix(".tmp")
    try:
        with open(backup, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        p.replace(backup)
    except Exception:
        pass

def append_history(
        user_text: Optional[str],
        history: List[Dict[str,Any]],
        bot_text: str,
        *,
        max_turns: Optional[int],
        user_id: Optional[str]=None,
        base_dir: str="history"
       ) -> None:
    history.append({"user": user_text, "bot": bot_text, "timestamp": datetime.utcnow().isoformat() + "Z"})
    if max_turns and max_turns and len(history) > max_turns:
        history[:] = history[-max_turns:]
        save_history(user_id, history, base_dir=base_dir)

def chat_loop(chat_url:str,token:str,*,user_id:Optional[str],max_turns:Optional[int],reset_history:bool)->None:
    history = history =[] if reset_history else load_history(user_id)
    if history:
        print(f"Loaded {len(history)} previous chat turns from history.\n")

        print("Welcome to the AI Soul Counselor! Type 'exit' to end the chat.")
    while True:
        try:
            user_input=input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat. Goodbye!")
            break
        if not user_input:
            continue
        if user_input.lower()=="exit":
            print("\nExiting chat. Goodbye!")
            break
        try:
            reply=send_chat(chat_url, token, user_id=user_id, text=user_input, history=history)
            print(f"AI Soul: {reply}\n")
            append_history(user_input, history, reply, max_turns=max_turns, user_id=user_id)
            save_history(user_id, history)
        except Exception as e:
            print(f"Error: {e}\n")

    def parse_args() -> argparse.Namespace:
        parser=argparse.ArgumentParser(description="AI Soul Counselor Client")
        parser.add_argument("--base--dir",default=os.getenv("AI_BASE_DIR","http://localhost:8000"))
        parser.add_argument("--auth--prefix",default=os.getenv("AUTH_PREFIX","/auth"))
        parser.add_argument("--chat--prefix",default=os.getenv("CHAT_PREFIX","/chat"))

        parser.add_argument("--username",default=os.getenv("USERNAME"))
        parser.add_argument("--password",default=os.getenv("PASSWORD"))
        parser.add_argument("--user-id",default=os.getenv("USER_ID"))

        parser.add_argument("--reset-history",action="store_true",help="Ignore and reset chat history")
        parser.add_argument("--max-turns",type=int,default=int(os.getenv("MAX_TURNS", "0")),help="Max chat turns to keep in history, 0 for unlimited")
        return parser.parse_args()
    
    def main() -> None:
        args=parse_args()
        if not args.username or not args.password:
            raise SystemExit("Username and password are required.")
        
        login.url=join_url(args.base_url, args.auth_prefix, "login")
        chat_url=join_url(args.base_url, args.chat_prefix, "chat")

        chat_loop(
            chat_url=chat_url,
            token=token,
            user_id=args.user_id,
            max_turns=(args.max_turns or None),
            reset_history=args.reset_history
        )

        if __name__ == "__main__":
            main()

            







        

 

    