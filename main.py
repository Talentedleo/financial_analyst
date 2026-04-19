"""
Financial Analyst AI Agent System - Main Entry Point

Usage:
    python main.py                    # Start API server (default port 8000)
    python main.py --port 8000       # Start with custom port
    python main.py --host 127.0.0.1   # Start with custom host
"""

import os
import sys
import asyncio
import argparse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# Check required environment variables
required_env = ["MINIMAX_API_KEY"]
missing_env = [k for k in required_env if not os.environ.get(k)]

if missing_env:
    print(f"⚠ Warning: Missing environment variables: {missing_env}")
    print("   Required: MINIMAX_API_KEY")
    print("   Optional: FINNHUB_API_KEY")

print("=" * 60)
print("  Financial Analyst AI Agent System")
print("=" * 60)


def init_services():
    """Initialize all services"""
    print("\n📦 Initializing services...")
    
    # LLM Service
    try:
        from services import get_llm_service
        llm = get_llm_service()
        print(f"  ✓ LLM Service: {llm.model_name}")
    except Exception as e:
        print(f"  ✗ LLM Service failed: {e}")
    
    # Data Service
    try:
        from services import get_data_service
        data = get_data_service()
        print(f"  ✓ Data Service: initialized")
    except Exception as e:
        print(f"  ✗ Data Service failed: {e}")

    # Skill Loader
    try:
        from services import get_skill_loader
        loader = get_skill_loader()
        skills = loader.get_available_skills()
        print(f"  ✓ Skill Loader: {len(skills)} skills loaded")
        for skill in skills:
            print(f"      - {skill}")
    except Exception as e:
        print(f"  ✗ Skill Loader failed: {e}")


def main():
    """Main entry point - starts API server by default"""
    parser = argparse.ArgumentParser(description="Financial Analyst AI Agent")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host (default: 0.0.0.0)")
    args = parser.parse_args()
    
    # Initialize services
    init_services()
    
    # Import FastAPI app
    
    # Start API server
    print("\n" + "=" * 60)
    print(f"🚀 Starting API Server on {args.host}:{args.port}")
    print("=" * 60)
    print(f"\n📖 API Docs: http://localhost:{args.port}/docs")
    print(f"📖 ReDoc: http://localhost:{args.port}/redoc")
    print()
    
    uvicorn.run(
        "api:app",
        host=args.host,
        port=args.port,
        reload=True
    )


if __name__ == "__main__":
    main()
