
import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-zfc9ax.example.com"
EMAIL = "24f3004934@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_headers(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = (
        f"{time.perf_counter() - start:.6f}"
    )

    return response




@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/stats")
def stats(values: str):
    try:
        numbers = [
            int(value.strip())
            for value in values.split(",")
        ]

        if not numbers:
            raise ValueError("Empty list")

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="values must be comma-separated integers"
        )

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers)
    }
