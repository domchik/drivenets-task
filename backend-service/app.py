from app.main import app

# This file is kept as an entry point for backward compatibility
# All actual implementation has been moved to the app/ package

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5001, reload=True)
