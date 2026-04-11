"""
Financial Analyst AI Agent System - Main Entry Point
"""

import os
import asyncio

# Check required environment variables
required_env = ["MINIMAX_API_KEY"]
missing_env = [k for k in required_env if not os.environ.get(k)]

if missing_env:
    print(f"⚠ Warning: Missing environment variables: {missing_env}")

optional_env = ["FINNHUB_API_KEY"]
missing_optional = [k for k in optional_env if not os.environ.get(k)]

if missing_optional:
    print(f"ℹ Note: Optional variables not set: {missing_optional}")

print("=" * 60)
print("Financial Analyst AI Agent System")
print("=" * 60)

# Import components
from agents.plan_agent import get_plan_agent
from services import get_llm_service, get_data_service, get_skill_loader


async def init_services():
    """Initialize all services"""
    print("\n📦 Initializing services...")
    
    # LLM Service
    try:
        llm = get_llm_service()
        print(f"  ✓ LLM Service: {llm.model_name}")
    except Exception as e:
        print(f"  ✗ LLM Service failed: {e}")
    
    # Data Service
    try:
        data = get_data_service()
        print(f"  ✓ Data Service: Finnhub connected")
    except Exception as e:
        print(f"  ✗ Data Service failed: {e}")
    
    # Skill Loader
    try:
        loader = get_skill_loader()
        skills = loader.load_all_skills()
        print(f"  ✓ Skill Loader: {len(skills)} skills loaded")
    except Exception as e:
        print(f"  ℹ Skill Loader: {e}")


async def demo():
    """Run demo queries"""
    print("\n" + "=" * 60)
    print("Demo Analysis")
    print("=" * 60)
    
    plan_agent = get_plan_agent()
    
    demo_queries = [
        "Should I invest in Apple using Buffett's framework?",
        "What does Cathie Wood think about Tesla?",
    ]
    
    for query in demo_queries:
        print(f"\n❓ Query: {query}")
        print("-" * 50)
        try:
            # For demo, just print the query structure
            print("   [Agent would analyze and return response]")
        except Exception as e:
            print(f"   Error: {e}")


async def main():
    """Main entry point"""
    await init_services()
    await demo()
    
    print("\n" + "=" * 60)
    print("🚀 System Ready!")
    print("=" * 60)
    print("\nTo start the API server:")
    print("  uvicorn api.main:app --reload --port 8000")
    print("\nOr run directly:")
    print("  python -m uvicorn api.main:app --reload --port 8000")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
