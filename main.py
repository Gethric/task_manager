from fastapi import FastAPI
from auth.routes import router as auth_router
from tasks.routes import router as task_router

# FastAPI app
app = FastAPI()

# Include authentication and task routes
app.include_router(auth_router, prefix="/auth")
app.include_router(task_router, prefix="/tasks")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API"}
