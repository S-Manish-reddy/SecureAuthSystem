from fastapi import FastAPI
from sqlalchemy import text

from backend.database.db import engine
from backend.database.db import Base

from backend.models.user_model import User

from backend.routes.auth_routes import router as auth_router
from backend.routes.user_routes import router as user_router
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from backend.security.rate_limiter import limiter

from backend.middleware.security_middleware import SecurityHeadersMiddleware
from backend.routes.admin_routes import router as admin_router
from fastapi.middleware.cors import CORSMiddleware
from backend.models.security_event_model import SecurityEvent
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    title="Secure Authentication System",
    description="Production Style Secure Authentication Platform",
    version="1.0.0"
)
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["GET", "POST"],

    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "127.0.0.1",
        "localhost"
    ]
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)


@app.get("/")
def home():

    return {
        "message": "Secure Authentication System Running"
    }


@app.get("/db-test")
def db_test():

    with engine.connect() as connection:

        connection.execute(text("SELECT 1"))

        return {
            "database_status": "Connected Successfully"
        }