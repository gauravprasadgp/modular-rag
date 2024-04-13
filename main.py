from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from generator.llm_calls import get_answer
from retrieve.vector_store import create_embeddings_from_file, get_relevant_document
from utils.db import postgres_db

llms = {}

app = FastAPI(title="Modular RAG",
              version="1.0.0", )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await postgres_db.create_connection_pool()
    yield
    await postgres_db.close_connection_pool()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


@app.post("/create")
async def create_embedding(file: UploadFile):
    await create_embeddings_from_file(file)


@app.post("/answer")
async def post_conversation(request: Request):
    payload = await request.json()
    query = payload.get("query")
    context = get_relevant_document(query=query)
    return await get_answer(context=context, query=query)

@app.get("/")
async def get_test(request: Request):
    return "Successfully Deployed"
