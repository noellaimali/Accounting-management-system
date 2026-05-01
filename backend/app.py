from fastapi import FastAPI
from .routes import router
from .models import init_db

app = FastAPI(title="Accounting System API")

app.include_router(router, prefix="/api")

@app.on_event("startup")
def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
