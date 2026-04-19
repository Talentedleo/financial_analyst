"""
Skill Loader Service - Load Celebrity Skills

Each skill folder contains:
- SKILL.md: ADK skill definition with YAML frontmatter (name, description, triggers)
- references/: Additional reference documents

This loader reads SKILL.md for metadata and can provide context for agents.
"""

import os
import re
from typing import Dict, Optional, List
from pathlib import Path


class SkillLoader:
    """Service for loading and parsing Celebrity Skills"""
    
    def __init__(self, skills_path: Optional[str] = None):
        """
        Initialize SkillLoader.
        
        Args:
            skills_path: Optional explicit path. Defaults to local skills/ directory.
        """
        if skills_path:
            self.skills_path = Path(skills_path)
        else:
            # Default: local skills/ directory in project
            self.skills_path = Path(__file__).parent.parent / "skills"
        
        self._validate_path()
        self._skills_cache: Dict[str, Dict] = {}
    
    def _validate_path(self) -> None:
        """Validate that skills path exists"""
        if not self.skills_path.exists():
            raise FileNotFoundError(
                f"Skills path does not exist: {self.skills_path}\n"
                f"Ensure celebrity skills are copied to the skills/ directory."
            )
    
    def get_available_skills(self) -> List[str]:
        """Get list of available skill names (from SKILL.md name field)"""
        if not self.skills_path.exists():
            return []
        
        skills = []
        for folder in self.skills_path.iterdir():
            if not folder.is_dir():
                continue
            skill_md_path = folder / "SKILL.md"
            if not skill_md_path.exists():
                continue
            
            content = skill_md_path.read_text(encoding='utf-8')
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                continue
            
            import yaml
            try:
                meta = yaml.safe_load(match.group(1))
                name = meta.get('name')
                if name:
                    skills.append(name)
            except yaml.YAMLError:
                continue
        
        return sorted(skills)
    
    def load_skill(self, skill_name: str) -> Dict:
        """
        Load a celebrity skill by name (from SKILL.md).
        
        Args:
            skill_name: 'warren-buffett', 'cathie-wood', etc.
        
        Returns:
            Dict with 'name', 'path', 'meta', 'references'
        """
        if skill_name in self._skills_cache:
            return self._skills_cache[skill_name]
        
        # Find the folder containing this skill
        folder_path = None
        for folder in self.skills_path.iterdir():
            if not folder.is_dir():
                continue
            skill_md_path = folder / "SKILL.md"
            if not skill_md_path.exists():
                continue
            
            content = skill_md_path.read_text(encoding='utf-8')
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                continue
            
            import yaml
            try:
                meta = yaml.safe_load(match.group(1))
                if meta.get('name') == skill_name:
                    folder_path = folder
                    break
            except yaml.YAMLError:
                continue
        
        if folder_path is None:
            available = self.get_available_skills()
            raise ValueError(
                f"Skill '{skill_name}' not found. Available: {available}"
            )
        
        result = {
            "name": skill_name,
            "path": str(folder_path),
            "meta": {},
            "references": {}
        }
        
        # Load SKILL.md
        skill_md_path = folder_path / "SKILL.md"
        content = skill_md_path.read_text(encoding='utf-8')
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if match:
            import yaml
            try:
                result["meta"] = yaml.safe_load(match.group(1)) or {}
                result["content"] = match.group(2).strip()
            except yaml.YAMLError:
                result["meta"] = {}
                result["content"] = content
        
        # Load reference files
        ref_path = folder_path / "references"
        if ref_path.exists():
            for ref_file in ref_path.glob("*.md"):
                result["references"][ref_file.name] = ref_file.read_text(encoding='utf-8')
        
        self._skills_cache[skill_name] = result
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
    
    def get_skill_description(self, skill_name: str) -> str:
        """Get the description for a skill."""
        try:
            skill = self.load_skill(skill_name)
            meta = skill.get("meta", {})
            return meta.get('description', skill_name)
        except Exception:
            return skill_name
    
    def get_skill_context(self, skill_name: str) -> str:
        """Get skill content for context (meta + content)."""
        skill = self.load_skill(skill_name)
        meta = skill.get("meta", {})
        content = skill.get("content", "")
        
        parts = []
        if meta.get('name'):
            parts.append(f"# {meta.get('name').replace('-', ' ').title()}\n")
        if meta.get('description'):
            parts.append(f"\n{meta.get('description')}\n")
        if content:
            parts.append(f"\n---\n\n{content}\n")
        
        return "\n".join(parts)


# Global singleton
_skill_loader: Optional[SkillLoader] = None


def get_skill_loader() -> SkillLoader:
    """Get or create global skill loader instance"""
    global _skill_loader
    if _skill_loader is None:
        _skill_loader = SkillLoader()
    return _skill_loader


def load_skill(skill_name: str) -> Dict:
    """Convenience function"""
    return get_skill_loader().load_skill(skill_name)


def get_skill_context(skill_name: str) -> str:
    """Convenience function"""
    return get_skill_loader().get_skill_context(skill_name)


def get_available_skills() -> List[str]:
    """Convenience function"""
    return get_skill_loader().get_available_skills()
