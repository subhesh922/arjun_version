#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to call API (we’ll connect React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to localhost later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "DFMEA GenAI platform is alive!"}
