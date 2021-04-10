from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Access /docs for API documentation"}


@app.get(
    "/ping",
    name="Ping Pong Test",
    description="""ping pong test to verify the functioning
     of the system routes""",
)
async def pong():
    return {"ping": "pong!"}
