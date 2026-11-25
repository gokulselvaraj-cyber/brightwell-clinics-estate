from fastapi import FastAPI

from .api import router

app = FastAPI(title="Brightwell visit summary", version="1.4.2")
app.include_router(router)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
