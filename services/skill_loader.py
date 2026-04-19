"""
Skill Loader Service - Load Celebrity Skills

Each skill folder contains:
- SKILL.md: Skill definition with YAML frontmatter
- references/: Additional reference documents

Simply scans skills/ folder and reads SKILL.md for each subdirectory.
No naming restrictions - any folder with SKILL.md is a valid skill.
"""

import re
from typing import Dict, Optional, List
from pathlib import Path


class SkillLoader:
    """Service for loading and parsing Celebrity Skills"""
    
    def __init__(self, skills_path: Optional[str] = None):
        if skills_path:
            self.skills_path = Path(skills_path)
        else:
            self.skills_path = Path(__file__).parent.parent / "skills"
        
        self._validate_path()
        self._skills_cache: Dict[str, Dict] = {}
    
    def _validate_path(self) -> None:
        if not self.skills_path.exists():
            raise FileNotFoundError(
                f"Skills path does not exist: {self.skills_path}"
            )
    
    def get_available_skills(self) -> List[str]:
        """Get list of skill names (folder names with SKILL.md)."""
        if not self.skills_path.exists():
            return []
        
        skills = []
        for folder in self.skills_path.iterdir():
            if folder.is_dir() and (folder / "SKILL.md").exists():
                skills.append(folder.name)
        return sorted(skills)
    
    def load_skill(self, skill_name: str) -> Dict:
        """
        Load a skill by folder name.
        
        Args:
            skill_name: Folder name, e.g., 'warren_buffett', 'cathie_wood'
        
        Returns:
            Dict with 'name', 'path', 'meta', 'content', 'references'
        """
        if skill_name in self._skills_cache:
            return self._skills_cache[skill_name]
        
        folder_path = self.skills_path / skill_name
        if not folder_path.exists() or not folder_path.is_dir():
            available = self.get_available_skills()
            raise ValueError(f"Skill '{skill_name}' not found. Available: {available}")
        
        skill_md_path = folder_path / "SKILL.md"
        if not skill_md_path.exists():
            raise ValueError(f"SKILL.md not found for skill '{skill_name}'")
        
        content = skill_md_path.read_text(encoding='utf-8')
        
        # Parse frontmatter
        meta = {}
        body = content
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if match:
            import yaml
            try:
                meta = yaml.safe_load(match.group(1)) or {}
                body = match.group(2).strip()
            except yaml.YAMLError:
                body = content
        
        result = {
            "name": skill_name,
            "path": str(folder_path),
            "meta": meta,
            "content": body,
            "references": {}
        }
        
        # Load references
        ref_path = folder_path / "references"
        if ref_path.exists():
            for ref_file in ref_path.glob("*.md"):
                result["references"][ref_file.name] = ref_file.read_text(encoding='utf-8')
        
        self._skills_cache[skill_name] = result
        return result
    
    def load_all_skills(self) -> Dict[str, Dict]:
        """Load all available skills."""
        skills = {}
        for skill_name in self.get_available_skills():
            try:
                skills[skill_name] = self.load_skill(skill_name)
            except Exception as e:
                print(f"Warning: Could not load skill '{skill_name}': {e}")
        return skills
    
    def get_skill_description(self, skill_name: str) -> str:
        """Get description from skill meta."""
        try:
            skill = self.load_skill(skill_name)
            meta = skill.get("meta", {})
            return meta.get('description', skill_name)
        except Exception:
            return skill_name
    
    def get_skill_context(self, skill_name: str) -> str:
        """Get full skill context for agent instruction."""
        skill = self.load_skill(skill_name)
        meta = skill.get("meta", {})
        content = skill.get("content", "")
        
        name = meta.get('name', skill_name).replace('-', ' ').replace('_', ' ').title()
        parts = [f"# {name}\n"]
        
        if meta.get('description'):
            parts.append(f"\n{meta.get('description')}\n")
        if content:
            parts.append(f"\n---\n\n{content}\n")
        
        return "\n".join(parts)


# Global singleton
_skill_loader: Optional[SkillLoader] = None


def get_skill_loader() -> SkillLoader:
    global _skill_loader
    if _skill_loader is None:
        _skill_loader = SkillLoader()
    return _skill_loader


def load_skill(skill_name: str) -> Dict:
    return get_skill_loader().load_skill(skill_name)


def get_skill_context(skill_name: str) -> str:
    return get_skill_loader().get_skill_context(skill_name)


def get_available_skills() -> List[str]:
    return get_skill_loader().get_available_skills()
