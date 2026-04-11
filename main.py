"""
Financial Analyst AI Agent System - Legacy Entry Point

This file is kept for backward compatibility.
Please use app.py for startup and tests/test_main.py for testing.
"""

if __name__ == "__main__":
    import sys
    import os
    
    # Check if running tests
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        from tests.test_main import main as test_main
        import asyncio
        asyncio.run(test_main())
    else:
        # Forward to app.py
        os.execv(sys.executable, [sys.executable, "app.py"] + sys.argv[1:])
