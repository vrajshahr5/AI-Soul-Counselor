from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.database import init_db
from app.protected_routes import router as protected_router
from app.routes_chat import router as chat_router
from app.routes_history import router as history_router
from app.routes_soul import router as soul_router



app = FastAPI(
    title="AI Soul Counselor",
    version="0.1.0",
    description="An AI powered counseling platform"
)


app.add_middleware(
CORSMiddleware,
allow_origins =["*"],
allow_credentials = True,
allow_methods=["*"],
allow_headers=["*"],


)

init_db()

app.include_router(soul_router)
app.include_router(auth_router,prefix="/auth")
app.include_router(protected_router, prefix="/protected")
app.include_router(chat_router,prefix="/chat")
app.include_router(history_router,prefix="/history")

@app.get("/")
def root():
    return{"message": "API is running"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    open_schema = get_openapi(
        title = "AI Soul Counselor",
        version = "0.1.0",
        description= "API documentation with JWT auth",
        routes=app.routes,
)
    
    app.openapi_schema = open_schema

    return app.openapi_schema

app.openapi = custom_openapi


























    



