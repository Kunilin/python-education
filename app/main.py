from fastapi import FastAPI
from api.endpoints.tasks import router

app = FastAPI(title="Tasks Manger API")
app.include_router(router)