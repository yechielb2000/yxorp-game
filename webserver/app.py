from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(a: FastAPI):
    load_dotenv()
    yield


app = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    uvicorn.run("cnc:app", host="0.0.0.0", port=8000)
