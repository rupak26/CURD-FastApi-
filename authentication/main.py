from fastapi import FastAPI
from utils import authentications
from controlers import user
from database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(authentications.router)
app.include_router(user.router)

@app.get("/health")
def health():
    return {"status": "ok"}
