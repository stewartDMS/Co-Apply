"""
Achievement Library Management
Stores and manages candidate achievements, skills, and experiences
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Achievement:
    """Represents a single achievement or experience"""
    id: str
    title: str
    description: str
    category: str  # e.g., "technical", "leadership", "project", "certification"
    skills: List[str]
    keywords: List[str]
    impact: Optional[str] = None
    metrics: Optional[str] = None
    date: Optional[str] = None
    context: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Achievement':
        return cls(**data)


@dataclass
class CandidateProfile:
    """Candidate's complete profile"""
    name: str
    email: str
    phone: str
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    summary: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'CandidateProfile':
        return cls(**data)


class AchievementLibrary:
    """Manages the candidate's achievement library"""

    def __init__(self, data_file: str = "data/user_achievements.json"):
        self.data_file = data_file
        self.profile: Optional[CandidateProfile] = None
        self.achievements: List[Achievement] = []
        self.load()

    def load(self):
        """Load achievements from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    content = f.read()
                    if not content.strip():
                        return
                    data = json.loads(content)
                    if 'profile' in data:
                        self.profile = CandidateProfile.from_dict(data['profile'])
                    if 'achievements' in data:
                        self.achievements = [
                            Achievement.from_dict(a) for a in data['achievements']
                        ]
            except json.JSONDecodeError:
                # Empty or invalid file, start fresh
                pass

    def save(self):
        """Save achievements to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        data = {
            'profile': self.profile.to_dict() if self.profile else None,
            'achievements': [a.to_dict() for a in self.achievements]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_achievement(self, achievement: Achievement):
        """Add a new achievement"""
        self.achievements.append(achievement)
        self.save()

    def update_achievement(self, achievement_id: str, updated: Achievement):
        """Update an existing achievement"""
        for i, achievement in enumerate(self.achievements):
            if achievement.id == achievement_id:
                self.achievements[i] = updated
                self.save()
                return True
        return False

    def delete_achievement(self, achievement_id: str) -> bool:
        """Delete an achievement"""
        initial_length = len(self.achievements)
        self.achievements = [a for a in self.achievements if a.id != achievement_id]
        if len(self.achievements) < initial_length:
            self.save()
            return True
        return False

    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Get a specific achievement"""
        for achievement in self.achievements:
            if achievement.id == achievement_id:
                return achievement
        return None

    def search_by_keywords(self, keywords: List[str]) -> List[Achievement]:
        """Search achievements by keywords"""
        keywords_lower = [k.lower() for k in keywords]
        results = []
        for achievement in self.achievements:
            achievement_keywords = [k.lower() for k in achievement.keywords]
            achievement_skills = [s.lower() for s in achievement.skills]
            achievement_text = (
                achievement.title.lower() + " " + achievement.description.lower()
            )
            
            # Check if any keyword matches
            for keyword in keywords_lower:
                if (keyword in achievement_keywords or
                    keyword in achievement_skills or
                    keyword in achievement_text):
                    results.append(achievement)
                    break
        return results

    def search_by_category(self, category: str) -> List[Achievement]:
        """Get all achievements in a category"""
        return [a for a in self.achievements if a.category == category]

    def get_all_skills(self) -> List[str]:
        """Get all unique skills from achievements"""
        skills = set()
        for achievement in self.achievements:
            skills.update(achievement.skills)
        return sorted(list(skills))

    def set_profile(self, profile: CandidateProfile):
        """Set or update candidate profile"""
        self.profile = profile
        self.save()
