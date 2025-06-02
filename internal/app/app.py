# internal/app/app.py
from fastapi import FastAPI
from internal.http.server.server import router
app = FastAPI(
    title="Student Rating API",
    description="API для управления рейтингами студентов",
    version="1.0.0"
)

app.include_router(router)