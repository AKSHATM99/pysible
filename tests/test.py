from fastapi import FastAPI, Depends
from pysible.core import PyRate

app = FastAPI()

@app.get("/check")
async def func(rate = Depends(PyRate.rate_limiter(1, 5))):
    return {"message": "Hi I am working fine ...."}