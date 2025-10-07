"""
Achievement-Job Matching Engine
Matches candidate achievements with job requirements
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from ..core.achievement_library import Achievement
from ..core.job_parser import JobDescription


@dataclass
class MatchResult:
    """Result of matching an achievement to a job"""
    achievement: Achievement
    relevance_score: float  # 0-1
    matched_skills: List[str]
    matched_keywords: List[str]
    reasons: List[str]


class AchievementJobMatcher:
    """Matches achievements to job requirements"""

    def __init__(self):
        pass

    def match_achievements_to_job(self, achievements: List[Achievement], 
                                  job: JobDescription,
                                  top_n: int = None) -> List[MatchResult]:
        """
        Match achievements to a job description
        
        Args:
            achievements: List of candidate achievements
            job: Job description
            top_n: Return only top N matches (None for all)
            
        Returns:
            List of MatchResult sorted by relevance
        """
        results = []
        
        # Get all job keywords
        job_keywords = self._extract_job_keywords(job)
        
        for achievement in achievements:
            match = self._score_achievement(achievement, job, job_keywords)
            results.append(match)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        if top_n:
            results = results[:top_n]
        
        return results

    def _extract_job_keywords(self, job: JobDescription) -> List[str]:
        """Extract all relevant keywords from job description"""
        keywords = []
        
        # Add skills
        keywords.extend(job.skills_required or [])
        keywords.extend(job.skills_preferred or [])
        
        # Add keywords from requirements and responsibilities
        for req in (job.requirements or []):
            keywords.extend(self._extract_keywords_from_text(req))
        
        for resp in (job.responsibilities or []):
            keywords.extend(self._extract_keywords_from_text(resp))
        
        # Remove duplicates (case-insensitive)
        keywords_lower = {}
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower not in keywords_lower:
                keywords_lower[kw_lower] = kw
        
        return list(keywords_lower.values())

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        import re
        # Simple extraction - words that are capitalized or technical terms
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        words.extend(re.findall(r'\b[A-Z]{2,}\b', text))
        return words

    def _score_achievement(self, achievement: Achievement, job: JobDescription, 
                          job_keywords: List[str]) -> MatchResult:
        """Score how well an achievement matches a job"""
        score = 0.0
        max_score = 0.0
        matched_skills = []
        matched_keywords = []
        reasons = []
        
        # Job required skills (higher weight)
        job_skills_required = [s.lower() for s in (job.skills_required or [])]
        achievement_skills = [s.lower() for s in achievement.skills]
        
        if job_skills_required:
            max_score += 40
            for skill in achievement_skills:
                if skill in job_skills_required:
                    matched_skills.append(skill)
                    score += 40 / max(len(job_skills_required), 1)
            
            if matched_skills:
                reasons.append(f"Matches {len(matched_skills)} required skills")
        
        # Job preferred skills (medium weight)
        job_skills_preferred = [s.lower() for s in (job.skills_preferred or [])]
        
        if job_skills_preferred:
            max_score += 20
            preferred_matches = 0
            for skill in achievement_skills:
                if skill in job_skills_preferred:
                    preferred_matches += 1
                    score += 20 / max(len(job_skills_preferred), 1)
            
            if preferred_matches:
                reasons.append(f"Matches {preferred_matches} preferred skills")
        
        # Keyword matching (medium weight)
        job_keywords_lower = [k.lower() for k in job_keywords]
        achievement_keywords_lower = [k.lower() for k in achievement.keywords]
        achievement_text = (achievement.title + " " + achievement.description).lower()
        
        if job_keywords_lower:
            max_score += 30
            keyword_score = 0
            for keyword in job_keywords_lower:
                if keyword in achievement_keywords_lower or keyword in achievement_text:
                    matched_keywords.append(keyword)
                    keyword_score += 1
            
            score += min((keyword_score / max(len(job_keywords_lower), 1)) * 30, 30)
            
            if matched_keywords:
                reasons.append(f"Matches {len(matched_keywords)} job keywords")
        
        # Category relevance (low weight)
        max_score += 10
        if job.title:
            job_title_lower = job.title.lower()
            if achievement.category == 'technical' and any(
                tech in job_title_lower for tech in ['engineer', 'developer', 'programmer', 'architect']
            ):
                score += 10
                reasons.append("Technical achievement relevant to role")
            elif achievement.category == 'leadership' and any(
                lead in job_title_lower for lead in ['lead', 'manager', 'director', 'senior', 'principal']
            ):
                score += 10
                reasons.append("Leadership achievement relevant to role")
            elif achievement.category == 'project':
                score += 5
                reasons.append("Project experience")
        
        # Normalize score
        if max_score > 0:
            relevance_score = min(score / max_score, 1.0)
        else:
            relevance_score = 0.0
        
        # Add default reason if no specific reasons
        if not reasons:
            reasons.append("Limited keyword match")
        
        return MatchResult(
            achievement=achievement,
            relevance_score=relevance_score,
            matched_skills=matched_skills,
            matched_keywords=matched_keywords,
            reasons=reasons
        )

    def filter_by_threshold(self, matches: List[MatchResult], 
                           threshold: float = 0.3) -> List[MatchResult]:
        """Filter matches by relevance threshold"""
        return [m for m in matches if m.relevance_score >= threshold]

    def group_by_category(self, matches: List[MatchResult]) -> Dict[str, List[MatchResult]]:
        """Group matches by achievement category"""
        grouped = {}
        for match in matches:
            category = match.achievement.category
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(match)
        return grouped

    def get_coverage_report(self, matches: List[MatchResult], 
                           job: JobDescription) -> Dict[str, any]:
        """Generate a coverage report showing how well achievements cover job requirements"""
        all_matched_skills = set()
        all_matched_keywords = set()
        
        for match in matches:
            all_matched_skills.update([s.lower() for s in match.matched_skills])
            all_matched_keywords.update([k.lower() for k in match.matched_keywords])
        
        # Calculate coverage
        required_skills = set([s.lower() for s in (job.skills_required or [])])
        preferred_skills = set([s.lower() for s in (job.skills_preferred or [])])
        
        required_coverage = 0
        if required_skills:
            required_coverage = len(all_matched_skills & required_skills) / len(required_skills)
        
        preferred_coverage = 0
        if preferred_skills:
            preferred_coverage = len(all_matched_skills & preferred_skills) / len(preferred_skills)
        
        missing_required = required_skills - all_matched_skills
        missing_preferred = preferred_skills - all_matched_skills
        
        return {
            'required_skills_coverage': round(required_coverage * 100, 2),
            'preferred_skills_coverage': round(preferred_coverage * 100, 2),
            'matched_skills_count': len(all_matched_skills),
            'matched_keywords_count': len(all_matched_keywords),
            'missing_required_skills': list(missing_required),
            'missing_preferred_skills': list(missing_preferred),
            'recommendation': self._get_coverage_recommendation(
                required_coverage, preferred_coverage, missing_required
            )
        }

    def _get_coverage_recommendation(self, required_cov: float, preferred_cov: float, 
                                    missing_required: set) -> str:
        """Get recommendation based on coverage"""
        if required_cov >= 0.8:
            return "Excellent coverage! Your achievements align well with job requirements."
        elif required_cov >= 0.6:
            return "Good coverage. Consider highlighting achievements that demonstrate missing skills."
        elif required_cov >= 0.4:
            return "Moderate coverage. Focus on achievements that match the required skills."
        else:
            return f"Low coverage. Missing critical skills: {', '.join(list(missing_required)[:3])}"
