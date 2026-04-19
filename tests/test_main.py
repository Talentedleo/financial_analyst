"""
Financial Analyst AI Agent System - Test Suite

Comprehensive test suite covering:
- Environment and configuration
- Services (LLM, Data, Skill Loader)
- Tools (Stock, News, Fundamentals)
- Agents (Dynamic Factory with ADK Skills)
- API endpoints (smoke test)
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestSuite:
    """Comprehensive test suite for Financial Analyst system"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
        self.warnings = []

    def log(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.results.append(f"{status} | {test_name}")
        if message:
            self.results.append(f"      └─ {message}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def warn(self, message: str):
        """Log warning"""
        self.warnings.append(f"⚠  {message}")

    # ========== Environment Tests ==========

    async def test_environment_variables(self):
        """Test required environment variables"""
        required = ["MINIMAX_API_KEY"]
        optional = ["FINNHUB_API_KEY", "API_MASTER_KEY"]
        
        missing_required = [k for k in required if not os.environ.get(k)]
        if missing_required:
            self.warn(f"Missing required env: {missing_required}")
        
        for k in optional:
            if not os.environ.get(k):
                self.warn(f"Missing optional env: {k}")
        
        self.log("Environment Variables", len(missing_required) == 0, 
                 f"Required: OK" if not missing_required else f"Missing: {missing_required}")

    async def test_project_structure(self):
        """Test project directory structure"""
        required_dirs = ["agents", "api", "services", "tools", "skills", "tests"]
        required_files = ["main.py", "requirements.txt"]
        
        missing = []
        for d in required_dirs:
            if not (PROJECT_ROOT / d).exists():
                missing.append(f"dir: {d}")
        for f in required_files:
            if not (PROJECT_ROOT / f).exists():
                missing.append(f"file: {f}")
        
        self.log("Project Structure", len(missing) == 0, 
                 "All required paths exist" if not missing else f"Missing: {missing}")

    # ========== Service Tests ==========

    async def test_llm_service_init(self):
        """Test LLM service initialization"""
        try:
            from services import get_llm_service
            llm = get_llm_service()
            assert llm.model_name == "minimax/MiniMax-M2.7-highspeed"
            self.log("LLM Service Init", True, f"Model: {llm.model_name}")
            return True
        except Exception as e:
            self.log("LLM Service Init", False, str(e))
            return False

    async def test_llm_service_model(self):
        """Test LLM service model creation"""
        try:
            from services import get_llm_service
            llm = get_llm_service()
            model = llm.create_model(temperature=0.7)
            assert model is not None
            self.log("LLM Service Model", True, "Model created successfully")
            return True
        except Exception as e:
            self.log("LLM Service Model", False, str(e))
            return False

    async def test_data_service_init(self):
        """Test data service initialization"""
        try:
            from services import get_data_service
            data = get_data_service()
            self.log("Data Service Init", True, "Finnhub + Yahoo Finance initialized")
            return True
        except Exception as e:
            self.log("Data Service Init", False, str(e))
            return False

    async def test_data_service_quote(self):
        """Test stock quote retrieval"""
        try:
            from services import get_data_service
            data = get_data_service()
            quote = data.get_quote("AAPL")
            assert quote.get('c') > 0, "Invalid quote price"
            self.log("Data Service Quote", True, f"AAPL: ${quote.get('c')}")
            return True
        except Exception as e:
            self.log("Data Service Quote", False, str(e))
            return False

    async def test_data_service_search(self):
        """Test symbol search"""
        try:
            from services import get_data_service
            data = get_data_service()
            results = data.search_symbol("Apple")
            assert len(results) > 0, "No search results"
            self.log("Data Service Search", True, f"Found {len(results)} results for 'Apple'")
            return True
        except Exception as e:
            self.log("Data Service Search", False, str(e))
            return False

    async def test_data_service_candles(self):
        """Test candlestick data retrieval"""
        try:
            from services import get_data_service
            data = get_data_service()
            candles = data.get_candles("AAPL", days=30)
            assert 'c' in candles and len(candles.get('c', [])) > 0, "No candle data"
            self.log("Data Service Candles", True, f"Got {len(candles.get('c', []))} candles")
            return True
        except Exception as e:
            self.log("Data Service Candles", False, str(e))
            return False

    async def test_data_service_company_news(self):
        """Test company news retrieval"""
        try:
            from services import get_data_service
            data = get_data_service()
            news = data.get_company_news("AAPL", days=7)
            self.log("Data Service News", True, f"Got {len(news)} news articles")
            return True
        except Exception as e:
            self.log("Data Service News", False, str(e))
            return False

    async def test_skill_loader_init(self):
        """Test skill loader initialization"""
        try:
            from services import get_skill_loader
            loader = get_skill_loader()
            assert loader.skills_path.exists()
            self.log("Skill Loader Init", True, f"Path: {loader.skills_path}")
            return True
        except Exception as e:
            self.log("Skill Loader Init", False, str(e))
            return False

    async def test_skill_loader_skills(self):
        """Test skill loading"""
        try:
            from services import get_skill_loader
            loader = get_skill_loader()
            skills = loader.load_all_skills()
            assert len(skills) >= 3, f"Expected 3+ skills, got {len(skills)}"
            skill_names = list(skills.keys())
            self.log("Skill Loader Skills", True, f"Loaded: {', '.join(skill_names)}")
            return True
        except Exception as e:
            self.log("Skill Loader Skills", False, str(e))
            return False

    async def test_skill_loader_context(self):
        """Test skill context generation"""
        try:
            from services import get_skill_context
            # Use underscore naming
            context = get_skill_context("warren-buffett")
            assert len(context) > 100, "Context too short"
            self.log("Skill Loader Context", True, f"Context length: {len(context)} chars")
            return True
        except Exception as e:
            self.log("Skill Loader Context", False, str(e))
            return False

    # ========== Tool Tests ==========

    async def test_tools_stock(self):
        """Test stock tools"""
        try:
            from tools.stock_tools import stock_tools
            assert len(stock_tools) == 3, f"Expected 3 stock tools, got {len(stock_tools)}"
            tool_names = [t.name for t in stock_tools]
            self.log("Tools - Stock", True, f"Tools: {', '.join(tool_names)}")
            return True
        except Exception as e:
            self.log("Tools - Stock", False, str(e))
            return False

    async def test_tools_news(self):
        """Test news tools"""
        try:
            from tools.news_tools import news_tools
            assert len(news_tools) >= 2, f"Expected 2+ news tools, got {len(news_tools)}"
            tool_names = [t.name for t in news_tools]
            self.log("Tools - News", True, f"Tools: {', '.join(tool_names)}")
            return True
        except Exception as e:
            self.log("Tools - News", False, str(e))
            return False

    async def test_tools_fundamentals(self):
        """Test fundamentals tools"""
        try:
            from tools.fundamentals_tools import fundamentals_tools
            assert len(fundamentals_tools) >= 3, f"Expected 3+ fundamentals tools, got {len(fundamentals_tools)}"
            tool_names = [t.name for t in fundamentals_tools]
            self.log("Tools - Fundamentals", True, f"Tools: {', '.join(tool_names)}")
            return True
        except Exception as e:
            self.log("Tools - Fundamentals", False, str(e))
            return False

    async def test_bark_tools(self):
        """Test bark notification tools"""
        try:
            from tools.bark_tools import bark_tools, send_notification, send_analysis_notification
            assert len(bark_tools) == 3, f"Expected 3 bark tools, got {len(bark_tools)}"
            tool_names = [t.name for t in bark_tools]
            self.log("Tools - Bark", True, f"Tools: {', '.join(tool_names)}")
            return True
        except Exception as e:
            self.log("Tools - Bark", False, str(e))
            return False

    # ========== Agent Tests (Dynamic Factory with ADK) ==========

    async def test_buffett_agent_init(self):
        """Test Buffett agent initialization via factory"""
        try:
            from agents import create_expert_agent
            agent = create_expert_agent("warren-buffett")
            assert agent is not None
            assert agent.name == "warren_buffett_agent"
            self.log("Buffett Agent Init", True, f"Tools: {len(agent.tools)}")
            return True
        except Exception as e:
            self.log("Buffett Agent Init", False, str(e))
            return False

    async def test_cathie_wood_agent_init(self):
        """Test Cathie Wood agent initialization via factory"""
        try:
            from agents import create_expert_agent
            agent = create_expert_agent("cathie-wood")
            assert agent is not None
            assert agent.name == "cathie_wood_agent"
            self.log("Cathie Wood Agent Init", True, f"Tools: {len(agent.tools)}")
            return True
        except Exception as e:
            self.log("Cathie Wood Agent Init", False, str(e))
            return False

    async def test_greg_abel_agent_init(self):
        """Test Greg Abel agent initialization via factory"""
        try:
            from agents import create_expert_agent
            agent = create_expert_agent("greg-abel")
            assert agent is not None
            assert agent.name == "greg_abel_agent"
            self.log("Greg Abel Agent Init", True, f"Tools: {len(agent.tools)}")
            return True
        except Exception as e:
            self.log("Greg Abel Agent Init", False, str(e))
            return False

    async def test_dynamic_agent_count(self):
        """Test that all skills have corresponding agents"""
        try:
            from agents import get_available_celebrities, get_available_celebrities
            agents_info = get_available_celebrities()
            skills = get_available_celebrities()
            assert len(agents_info) >= len(skills), f"Agent count mismatch"
            self.log("Dynamic Agent Count", True, f"{len(agents_info)} agents for {len(skills)} skills")
            return True
        except Exception as e:
            self.log("Dynamic Agent Count", False, str(e))
            return False

    # ========== API Tests ==========

    async def test_api_imports(self):
        """Test API routes can be imported"""
        try:
            from api import app
            assert app is not None
            self.log("API Imports", True, "FastAPI app imported successfully")
            return True
        except Exception as e:
            self.log("API Imports", False, str(e))
            return False

    async def test_api_endpoints_exist(self):
        """Test API endpoints are registered"""
        try:
            from api import app
            routes = [r.path for r in app.routes]
            expected = ["/", "/health", "/analyze", "/search", "/agents", "/clear-session"]
            missing = [e for e in expected if e not in routes]
            self.log("API Endpoints", len(missing) == 0, 
                     f"Endpoints registered" if not missing else f"Missing: {missing}")
            return len(missing) == 0
        except Exception as e:
            self.log("API Endpoints", False, str(e))
            return False

    # ========== Run All Tests ==========

    async def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("  Financial Analyst AI Agent - Test Suite")
        print("=" * 60)
        print()

        # Environment
        print("📋 Environment Tests")
        print("-" * 40)
        await self.test_environment_variables()
        await self.test_project_structure()
        print()

        # Services
        print("📦 Service Tests")
        print("-" * 40)
        await self.test_llm_service_init()
        await self.test_llm_service_model()
        await self.test_data_service_init()
        await self.test_data_service_quote()
        await self.test_data_service_search()
        await self.test_data_service_candles()
        await self.test_data_service_company_news()
        await self.test_skill_loader_init()
        await self.test_skill_loader_skills()
        await self.test_skill_loader_context()
        print()

        # Tools
        print("🔧 Tool Tests")
        print("-" * 40)
        await self.test_tools_stock()
        await self.test_tools_news()
        await self.test_tools_fundamentals()
        await self.test_bark_tools()
        print()

        # Agents
        print("🤖 Agent Tests (ADK Dynamic Factory)")
        print("-" * 40)
        await self.test_buffett_agent_init()
        await self.test_cathie_wood_agent_init()
        await self.test_greg_abel_agent_init()
        await self.test_dynamic_agent_count()
        print()

        # API
        print("🌐 API Tests")
        print("-" * 40)
        await self.test_api_imports()
        await self.test_api_endpoints_exist()
        print()

        # Summary
        print("=" * 60)
        print("  Test Results")
        print("=" * 60)
        for result in self.results:
            print(result)
        print()
        
        if self.warnings:
            print("⚠  Warnings:")
            for w in self.warnings:
                print(w)
            print()

        total = self.passed + self.failed
        pct = (self.passed / total * 100) if total > 0 else 0
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed} ({pct:.1f}%)")
        print("=" * 60)

        return self.failed == 0


async def main():
    """Run test suite"""
    suite = TestSuite()
    success = await suite.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
