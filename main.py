import random

import uvicorn
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Modular RAG",
    version="1.0.0",)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


@app.post("/answer")
async def post_conversation(request: Request):
    payload=await request.json()

@app.get("/")
async def get_test(request: Request):
    return "Successfully Depployed"