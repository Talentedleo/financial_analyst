"""
Skill Loader Service - Load Celebrity Skills into agents
"""

import os
from typing import Dict, Optional
from pathlib import Path


class SkillLoader:
    """Service for loading and parsing Celebrity Skills"""
    
    def __init__(self, skills_path: Optional[str] = None):
        self.skills_path = Path(skills_path or self._find_skills_path())
    
    def _find_skills_path(self) -> str:
        """Find the celebrity_skills directory"""
        # Try relative path first (for development)
        relative_path = Path(__file__).parent.parent / "celebrity_skills"
        if relative_path.exists():
            return str(relative_path)
        
        # Try home directory
        home_path = Path.home() / "Desktop/sandbox/celebrity_skills"
        if home_path.exists():
            return str(home_path)
        
        raise FileNotFoundError("celebrity_skills directory not found")
    
    def load_skill(self, skill_name: str) -> Dict[str, str]:
        """
        Load a celebrity skill by name.
        
        Args:
            skill_name: 'buffett', 'cathie_wood', 'greg_abel'
        
        Returns:
            Dict with 'skill_md' and 'reference_files'
        """
        skill_path = self.skills_path / skill_name
        
        if not skill_path.exists():
            raise ValueError(f"Skill '{skill_name}' not found at {skill_path}")
        
        result = {
            "name": skill_name,
            "path": str(skill_path),
            "files": {}
        }
        
        # Load SKILL.md
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            result["skill_md"] = skill_md_path.read_text()
        
        # Load reference files
        ref_path = skill_path / "references"
        if ref_path.exists():
            for ref_file in ref_path.glob("*.md"):
                result["files"][ref_file.name] = ref_file.read_text()
        
        return result
    
    def load_all_skills(self) -> Dict[str, Dict]:
        """Load all available celebrity skills"""
        skills = {}
        for skill_dir in self.skills_path.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skills[skill_dir.name] = self.load_skill(skill_dir.name)
        return skills
    
    def get_skill_context(self, skill_name: str) -> str:
        """
        Get skill content formatted for agent instruction.
        
        Returns:
            Skill content as string for system prompt
        """
        skill = self.load_skill(skill_name)
        
        context = f"# {skill_name.upper()} SKILL\n\n"
        
        if "skill_md" in skill:
            context += skill["skill_md"]
        
        context += "\n\n## Reference Materials\n\n"
        for filename, content in skill.get("files", {}).items():
            context += f"### {filename}\n\n{content}\n\n"
        
        return context
    
    def get_all_skills_context(self) -> str:
        """Get all skills context combined"""
        all_context = []
        for skill_name in ["warren_buffett", "cathie_wood", "greg_abel"]:
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
