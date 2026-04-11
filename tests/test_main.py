"""
Financial Analyst AI Agent System - Test Suite
"""

import asyncio
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.plan_agent import get_plan_agent
from services import get_llm_service, get_data_service, get_skill_loader


class TestSuite:
    """Test suite for Financial Analyst system"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []

    def log(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.results.append(f"{status} | {test_name}")
        if message:
            self.results.append(f"      {message}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    async def test_llm_service(self) -> bool:
        """Test LLM service initialization"""
        try:
            llm = get_llm_service()
            assert llm.model_name == "minimax/MiniMax-M2.7-highspeed"
            self.log("LLM Service", True, f"Model: {llm.model_name}")
            return True
        except Exception as e:
            self.log("LLM Service", False, str(e))
            return False

    async def test_data_service(self) -> bool:
        """Test data service initialization"""
        try:
            data = get_data_service()
            # Test with a known symbol
            quote = data.get_quote("AAPL")
            assert quote.get('c') > 0, "Invalid quote for AAPL"
            self.log("Data Service", True, f"AAPL quote: ${quote.get('c')}")
            return True
        except Exception as e:
            self.log("Data Service", False, str(e))
            return False

    async def test_skill_loader(self) -> bool:
        """Test skill loader"""
        try:
            loader = get_skill_loader()
            skills = loader.load_all_skills()
            assert len(skills) > 0, "No skills loaded"
            self.log("Skill Loader", True, f"Loaded {len(skills)} skills: {list(skills.keys())}")
            return True
        except Exception as e:
            self.log("Skill Loader", False, str(e))
            return False

    async def test_plan_agent(self) -> bool:
        """Test plan agent creation"""
        try:
            plan_agent = get_plan_agent()
            assert plan_agent.agent is not None
            self.log("Plan Agent", True)
            return True
        except Exception as e:
            self.log("Plan Agent", False, str(e))
            return False

    async def test_buffett_agent(self) -> bool:
        """Test Buffett agent"""
        try:
            from agents.experts import create_buffett_agent
            agent = create_buffett_agent()
            assert agent is not None
            self.log("Buffett Agent", True)
            return True
        except Exception as e:
            self.log("Buffett Agent", False, str(e))
            return False

    async def test_cathie_wood_agent(self) -> bool:
        """Test Cathie Wood agent"""
        try:
            from agents.experts import create_cathie_wood_agent
            agent = create_cathie_wood_agent()
            assert agent is not None
            self.log("Cathie Wood Agent", True)
            return True
        except Exception as e:
            self.log("Cathie Wood Agent", False, str(e))
            return False

    async def test_greg_abel_agent(self) -> bool:
        """Test Greg Abel agent"""
        try:
            from agents.experts import create_greg_abel_agent
            agent = create_greg_abel_agent()
            assert agent is not None
            self.log("Greg Abel Agent", True)
            return True
        except Exception as e:
            self.log("Greg Abel Agent", False, str(e))
            return False

    async def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("Financial Analyst AI Agent - Test Suite")
        print("=" * 60)

        # Check environment
        api_key = os.environ.get("MINIMAX_API_KEY")
        if not api_key:
            print("⚠ Warning: MINIMAX_API_KEY not set")
        else:
            print(f"✓ MINIMAX_API_KEY: {'*' * 20}{api_key[-4:]}")

        finnhub_key = os.environ.get("FINNHUB_API_KEY")
        if not finnhub_key:
            print("⚠ Warning: FINNHUB_API_KEY not set")
        else:
            print(f"✓ FINNHUB_API_KEY: {'*' * 20}{finnhub_key[-4:]}")

        print()

        # Run tests
        await self.test_llm_service()
        await self.test_data_service()
        await self.test_skill_loader()
        await self.test_plan_agent()
        await self.test_buffett_agent()
        await self.test_cathie_wood_agent()
        await self.test_greg_abel_agent()

        # Summary
        print()
        print("=" * 60)
        print("Test Results")
        print("=" * 60)
        for result in self.results:
            print(result)
        print()
        print(f"Total: {self.passed + self.failed} | Passed: {self.passed} | Failed: {self.failed}")
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
