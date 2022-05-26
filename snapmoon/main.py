# __main__.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from snapmoon.api import images

origins = [
    "https://getedge.glitch.me",
    "http://getedge.glitch.me",
    "https://ai.propvr.tech"
]


def create_app():
    """
    Returns the app after performing all the initialisation steps
    """
    application = FastAPI(
        title="SQY Snapmoon",
        description="This project applies filters on the real estate related"
            " images and is a proprietary software.",
        version="1.0.1"
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(images.router, prefix="/images", tags=["Image filters"])
    return application

app = create_app()


@app.get("/")
def index():
    """
    Test URL that returns "Hello World"
    """
    return "Hello World!"



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
