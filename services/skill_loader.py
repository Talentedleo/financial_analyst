"""
Skill Loader Service - Load Celebrity Skills into agents

Handles the SKILL.md format used by celebrity investor skills.
Each skill folder contains:
- SKILL.md: Main skill definition with YAML frontmatter and rich markdown content
- references/: Additional reference documents
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
        """Get list of available skill names (folder names with SKILL.md)"""
        if not self.skills_path.exists():
            return []
        
        skills = []
        for d in self.skills_path.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                skills.append(d.name)
        return sorted(skills)
    
    def _parse_yaml_frontmatter(self, content: str) -> tuple[Dict, str]:
        """Parse YAML frontmatter from markdown content.
        
        Returns:
            (frontmatter_dict, remaining_content)
        """
        # Match YAML frontmatter between --- markers
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n*(.*)$', content, re.DOTALL)
        if match:
            import yaml
            try:
                fm = yaml.safe_load(match.group(1))
                return (fm or {}), match.group(2)
            except yaml.YAMLError:
                pass
        return {}, content
    
    def load_skill(self, skill_name: str) -> Dict:
        """
        Load a celebrity skill by name.
        
        Args:
            skill_name: 'warren_buffett', 'cathie_wood', etc.
        
        Returns:
            Dict with 'name', 'path', 'meta', 'skill_md', 'references'
        """
        if skill_name in self._skills_cache:
            return self._skills_cache[skill_name]
        
        skill_path = self.skills_path / skill_name
        
        if not skill_path.exists():
            available = self.get_available_skills()
            raise ValueError(
                f"Skill '{skill_name}' not found at {skill_path}.\n"
                f"Available skills: {available}"
            )
        
        result = {
            "name": skill_name,
            "path": str(skill_path),
            "meta": {},
            "skill_md": None,
            "references": {}
        }
        
        # Load SKILL.md
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            content = skill_md_path.read_text(encoding='utf-8')
            meta, remaining = self._parse_yaml_frontmatter(content)
            result["meta"] = meta
            result["skill_md"] = remaining.strip() if remaining else content
        else:
            raise ValueError(f"SKILL.md not found for skill '{skill_name}' at {skill_md_path}")
        
        # Load reference files
        ref_path = skill_path / "references"
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
            # Try different field names
            return meta.get('subtitle') or meta.get('description') or skill_name.replace('_', ' ').title()
        except Exception:
            return skill_name.replace('_', ' ').title()
    
    def get_skill_context(self, skill_name: str) -> str:
        """Get full skill content for agent instruction."""
        skill = self.load_skill(skill_name)
        meta = skill.get("meta", {})
        skill_md = skill.get("skill_md", "")
        
        # Build context with meta info followed by full SKILL.md content
        context_parts = []
        
        # Title from meta or name
        name = meta.get('name', skill_name).replace('-', ' ').title()
        context_parts.append(f"# {name}\n")
        
        # Description from meta
        if meta.get('description'):
            context_parts.append(f"{meta.get('description')}\n")
        
        # Full SKILL.md content (which includes Effect Examples, Expression DNA, Mental Models, etc.)
        if skill_md:
            context_parts.append(f"\n---\n\n{skill_md}\n")
        
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


def load_skill(skill_name: str) -> Dict:
    """Convenience function"""
    return get_skill_loader().load_skill(skill_name)


def get_skill_context(skill_name: str) -> str:
    """Convenience function"""
    return get_skill_loader().get_skill_context(skill_name)


def get_available_skills() -> List[str]:
    """Convenience function"""
    return get_skill_loader().get_available_skills()
