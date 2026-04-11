"""
Skill Loader Service - Load Celebrity Skills into agents
"""

import os
from typing import Dict, Optional, List
from pathlib import Path


class SkillLoader:
    """Service for loading and parsing Celebrity Skills"""
    
    def __init__(self, skills_path: Optional[str] = None):
        """
        Initialize SkillLoader.
        
        Args:
            skills_path: Optional explicit path. If not provided, searches in order:
                1. CELEBRITY_SKILLS_PATH env var
                2. Project root (../celebrity_skills from project root)
                3. ~/Desktop/sandbox/celebrity_skills
        """
        self.skills_path = Path(skills_path or self._find_skills_path())
        self._validate_path()
    
    def _find_skills_path(self) -> str:
        """Find the celebrity_skills directory using multiple strategies"""
        # Strategy 1: Environment variable (highest priority)
        env_path = os.environ.get('CELEBRITY_SKILLS_PATH')
        if env_path and Path(env_path).exists():
            return env_path
        
        # Strategy 2: Relative to project root (development)
        # Project structure: src/financial_analyst/services/../ -> src/celebrity_skills
        project_root = Path(__file__).parent.parent
        relative_path = project_root / "celebrity_skills"
        if relative_path.exists():
            return str(relative_path)
        
        # Also try sibling directory (in case services/ is nested differently)
        sibling_path = Path(__file__).parent.parent.parent / "celebrity_skills"
        if sibling_path.exists():
            return str(sibling_path)
        
        # Strategy 3: Home directory sandbox
        home_path = Path.home() / "Desktop/sandbox/celebrity_skills"
        if home_path.exists():
            return str(home_path)
        
        # Strategy 4: Environment variable fallback (even if doesn't exist, try it)
        if env_path:
            return env_path
        
        raise FileNotFoundError(
            f"celebrity_skills directory not found. "
            f"Set CELEBRITY_SKILLS_PATH environment variable or "
            f"place celebrity_skills directory next to this project."
        )
    
    def _validate_path(self) -> None:
        """Validate that skills path exists"""
        if not self.skills_path.exists():
            raise FileNotFoundError(
                f"Skills path does not exist: {self.skills_path}\n"
                f"Set CELEBRITY_SKILLS_PATH environment variable."
            )
    
    def get_available_skills(self) -> List[str]:
        """Get list of available skill names"""
        if not self.skills_path.exists():
            return []
        return [
            d.name for d in self.skills_path.iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()
        ]
    
    def load_skill(self, skill_name: str) -> Dict[str, str]:
        """
        Load a celebrity skill by name.
        
        Args:
            skill_name: 'warren_buffett', 'cathie_wood', 'greg_abel'
        
        Returns:
            Dict with 'name', 'path', 'skill_md', 'files'
        """
        skill_path = self.skills_path / skill_name
        
        if not skill_path.exists():
            available = self.get_available_skills()
            raise ValueError(
                f"Skill '{skill_name}' not found at {skill_path}. "
                f"Available skills: {available}"
            )
        
        result = {
            "name": skill_name,
            "path": str(skill_path),
            "skill_md": None,
            "files": {}
        }
        
        # Load SKILL.md
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            result["skill_md"] = skill_md_path.read_text(encoding='utf-8')
        
        # Load reference files
        ref_path = skill_path / "references"
        if ref_path.exists():
            for ref_file in ref_path.glob("*.md"):
                result["files"][ref_file.name] = ref_file.read_text(encoding='utf-8')
        
        return result
    
    def load_all_skills(self) -> Dict[str, Dict]:
        """Load all available celebrity skills"""
        skills = {}
        for skill_name in self.get_available_skills():
            try:
                skills[skill_name] = self.load_skill(skill_name)
            except Exception as e:
                print(f"Warning: Could not load skill '{skill_name}': {e}")
        return skills
    
    def get_skill_context(self, skill_name: str) -> str:
        """
        Get skill content formatted for agent instruction.
        
        Returns:
            Skill content as string for system prompt
        """
        skill = self.load_skill(skill_name)
        
        context_parts = [f"# {skill_name.upper()} SKILL\n"]
        
        if skill.get("skill_md"):
            context_parts.append(skill["skill_md"])
        
        if skill.get("files"):
            context_parts.append("\n\n## Reference Materials\n")
            for filename, content in skill["files"].items():
                context_parts.append(f"\n### {filename}\n\n{content}\n")
        
        return "\n".join(context_parts)
    
    def get_all_skills_context(self) -> str:
        """Get all skills context combined"""
        all_context = []
        for skill_name in self.get_available_skills():
            try:
                context = self.get_skill_context(skill_name)
                all_context.append(context)
            except Exception as e:
                print(f"Warning: Could not load skill '{skill_name}': {e}")
        
        return "\n\n---\n\n".join(all_context)


# Global singleton
_skill_loader: Optional[SkillLoader] = None


def get_skill_loader() -> SkillLoader:
    """Get or create global skill loader instance"""
    global _skill_loader
    if _skill_loader is None:
        _skill_loader = SkillLoader()
    return _skill_loader


def load_skill(skill_name: str) -> Dict[str, str]:
    """Convenience function"""
    return get_skill_loader().load_skill(skill_name)


def get_skill_context(skill_name: str) -> str:
    """Convenience function"""
    return get_skill_loader().get_skill_context(skill_name)
