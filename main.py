import os
import uvicorn
import subprocess
import threading
from app import app as fastapi_app  # Import the FastAPI app from app.py

# Streamlit App Function
def run_streamlit():
    subprocess.run(["streamlit", "run", "frontend.py"])

# Main Function to Run Both Apps
def main():
    if os.getenv("DEPLOY_ENV") == "production":
        # In production, run only the FastAPI server
        uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
    else:
        # In local development, run both FastAPI and Streamlit
        # Start FastAPI server in a separate thread
        fastapi_thread = threading.Thread(target=lambda: uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="info"), daemon=True)
        fastapi_thread.start()
        
        # Start Streamlit app
        run_streamlit()

if __name__ == "__main__":
    main()


    ## make ready for deploy and env problem solve 