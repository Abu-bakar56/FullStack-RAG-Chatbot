import uvicorn
import threading
from app import app as fastapi_app


def run_fastapi():
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",   # Bind to all interfaces
        port=10000        # Use the same port you call in Streamlit
    )


def main():
    # Run FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # Keep main thread alive
    fastapi_thread.join()


if __name__ == "__main__":
    main()
