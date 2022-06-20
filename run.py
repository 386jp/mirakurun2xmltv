import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="trace" if os.getenv("DEV_MODE", 'False') == 'True' else "critical")

if __name__ == "__main__":
    main()