from fastapi import FastAPI
from settings import settings
import uvicorn

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=settings.webserver_port) # TODO: should be as webserver port.