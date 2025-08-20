import os
import uvicorn
import subprocess
import threading
from app import app as fastapi_app  


def run_streamlit():
    subprocess.run(["streamlit", "run", "frontend.py"])


def main():
    # if os.getenv("DEPLOY_ENV") == "production":
    #     # In production, run only the FastAPI server
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
    # else:
    #     # In local development, run both FastAPI and Streamlit
    #     # Start FastAPI server in a separate thread
    #     fastapi_thread = threading.Thread(target=lambda: uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="info"), daemon=True)
    #     fastapi_thread.start()
        
        # Start Streamlit app
        run_streamlit()

if __name__ == "__main__":
    main()


