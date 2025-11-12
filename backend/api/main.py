from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import game_router

# Create FastAPI app
app = FastAPI(
    title="De Beer is Los! API",
    description="API for the 'De Beer is Los!' board game",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(game_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to De Beer is Los! API",
        "docs": "/docs",
        "health": "OK"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "de-beer-is-los-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)