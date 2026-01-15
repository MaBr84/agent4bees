"""
main.py

Setup & Initialization Script.
Run this ONCE to prepare the environment and databases.
"""

import os
import sys
from dotenv import load_dotenv

# Import initialization functions from our app
from app.database import init_sql_db, init_vector_db

def main():
    print("🐝 Hive SME: System Initialization")
    print("----------------------------------")

    # 1. Check Environment
    print("[1/3] Checking Environment...")
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY is missing from .env file.")
        print("   Please create a .env file with your API key.")
        sys.exit(1)
    print("✅ Environment variables loaded.")

    # 2. Initialize SQL Database
    print("\n[2/3] Initializing SQL Database...")
    try:
        init_sql_db()
        print("✅ SQL Database ready.")
    except Exception as e:
        print(f"❌ Error initializing SQL DB: {e}")
        sys.exit(1)

    # 3. Initialize Vector Database
    print("\n[3/3] Initializing Vector Database...")
    try:
        init_vector_db()
        print("✅ Vector Database initialization attempt complete.")
    except Exception as e:
        print(f"❌ Error initializing Vector DB: {e}")
        # Don't exit here, might just be missing pdfs
    
    print("\n----------------------------------")
    print("🎉 System Ready! You can now run the agent:")
    print("   python agent.py")

if __name__ == "__main__":
    main()
