from fastapi import FastAPI
from controllers.blog_proxy import router as blog_router


app = FastAPI()

app.include_router(blog_router)