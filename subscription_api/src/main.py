from fastapi import FastAPI

app = FastAPI()


@app.get("/subscription/api/v1/hello")
async def root():
    return {"message": "Hello World"}
