"""
Skill Loader Service - Load Celebrity Skills into agents
"""

import os
import json
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
        """Get list of available skill names (folder names with _meta.json)"""
        if not self.skills_path.exists():
            return []
        
        skills = []
        for d in self.skills_path.iterdir():
            if d.is_dir() and (d / "_meta.json").exists():
                skills.append(d.name)
        return sorted(skills)
    
    def load_skill_meta(self, skill_name: str) -> Dict:
        """
        Load skill metadata from _meta.json.
        
        Args:
            skill_name: e.g., 'warren_buffett', 'cathie_wood'
        
        Returns:
            Dict with metadata from _meta.json
        """
        skill_path = self.skills_path / skill_name / "_meta.json"
        
        if not skill_path.exists():
            available = self.get_available_skills()
            raise ValueError(
                f"Skill '{skill_name}' not found. _meta.json missing at {skill_path}.\n"
                f"Available skills: {available}"
            )
        
        with open(skill_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_skill(self, skill_name: str) -> Dict:
        """
        Load a celebrity skill by name.
        
        Args:
            skill_name: 'warren_buffett', 'cathie_wood', etc.
        
        Returns:
            Dict with 'name', 'path', 'meta', 'references'
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
            "meta": None,
            "references": {}
        }
        
        # Load _meta.json (required)
        meta_path = skill_path / "_meta.json"
        if meta_path.exists():
            with open(meta_path, 'r', encoding='utf-8') as f:
                result["meta"] = json.load(f)
        
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
        """Get the description/display name for a skill."""
        try:
            meta = self.load_skill_meta(skill_name)
            # Try different field names across different meta formats
            return meta.get('subtitle') or meta.get('display_name') or meta.get('name', skill_name)
        except Exception:
            return skill_name.replace('_', ' ').title()
    
    def get_skill_context(self, skill_name: str) -> str:
        """Get skill content formatted for agent instruction."""
        skill = self.load_skill(skill_name)
        meta = skill.get("meta", {})
        
        # Build context from meta fields
        context_parts = []
        
        # Title
        name = meta.get('display_name') or meta.get('name', skill_name).replace('_', ' ').title()
        context_parts.append(f"# {name}\n")
        
        # Description
        if meta.get('description'):
            context_parts.append(f"\n## Identity & Philosophy\n{meta.get('description')}\n")
        
        # Subtitle
        if meta.get('subtitle'):
            context_parts.append(f"\n**{meta.get('subtitle')}**\n")
        
        # Tags as keywords
        if meta.get('tags'):
            tags = ', '.join(meta.get('tags', []))
            context_parts.append(f"\n**Keywords:** {tags}\n")
        
        # Triggers
        if meta.get('triggers'):
            triggers = ', '.join(meta.get('triggers', []))
            context_parts.append(f"\n**Triggers/Aliases:** {triggers}\n")
        
        # Sources
        if meta.get('sources'):
            context_parts.append("\n## Primary Sources\n")
            for source in meta.get('sources', []):
                source_name = source.get('name', 'Unknown')
                source_url = source.get('url', '')
                if source_url:
                    context_parts.append(f"- [{source_name}]({source_url})")
                else:
                    context_parts.append(f"- {source_name}")
        
        # References (if any)
        if skill.get("references"):
            context_parts.append("\n## Reference Materials\n")
            for filename, content in skill["references"].items():
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


def load_skill(skill_name: str) -> Dict:
    """Convenience function"""
    return get_skill_loader().load_skill(skill_name)


def get_skill_context(skill_name: str) -> str:
    """Convenience function"""
    return get_skill_loader().get_skill_context(skill_name)


def get_available_skills() -> List[str]:
    """Convenience function"""
    return get_skill_loader().get_available_skills()
