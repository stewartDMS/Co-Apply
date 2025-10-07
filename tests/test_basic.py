"""
Basic tests for Co-Apply functionality
"""

import pytest
import os
import sys
import tempfile
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from co_apply.core.achievement_library import Achievement, CandidateProfile, AchievementLibrary
from co_apply.core.job_parser import JobParser, JobDescription
from co_apply.analysis.matcher import AchievementJobMatcher
from co_apply.analysis.ats_analyzer import ATSAnalyzer


def test_achievement_creation():
    """Test creating an achievement"""
    achievement = Achievement(
        id="test_001",
        title="Test Achievement",
        description="This is a test achievement",
        category="technical",
        skills=["Python", "Testing"],
        keywords=["test", "python", "development"]
    )
    
    assert achievement.title == "Test Achievement"
    assert "Python" in achievement.skills
    assert achievement.category == "technical"


def test_candidate_profile():
    """Test creating a candidate profile"""
    profile = CandidateProfile(
        name="Test User",
        email="test@example.com",
        phone="555-1234",
        location="Test City"
    )
    
    assert profile.name == "Test User"
    assert profile.email == "test@example.com"


def test_achievement_library():
    """Test achievement library operations"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        library = AchievementLibrary(data_file=temp_file)
        
        # Set profile
        profile = CandidateProfile(
            name="Test User",
            email="test@example.com",
            phone="555-1234"
        )
        library.set_profile(profile)
        
        # Add achievement
        achievement = Achievement(
            id="test_001",
            title="Test Achievement",
            description="Test description",
            category="technical",
            skills=["Python"],
            keywords=["python", "test"]
        )
        library.add_achievement(achievement)
        
        # Verify
        assert library.profile.name == "Test User"
        assert len(library.achievements) == 1
        
        # Test search
        results = library.search_by_keywords(["python"])
        assert len(results) == 1
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_job_parser():
    """Test job description parsing"""
    job_text = """
    Senior Software Engineer
    
    Requirements:
    - 5+ years of experience
    - Strong Python skills
    - Experience with AWS
    - Excellent communication
    
    Responsibilities:
    - Design and implement features
    - Lead technical discussions
    - Mentor junior developers
    """
    
    parser = JobParser()
    job = parser.parse(job_text, "test_job", "Senior Engineer", "Test Corp")
    
    assert job.title == "Senior Engineer"
    assert job.company == "Test Corp"
    # Either requirements or responsibilities should be extracted
    assert len(job.requirements) > 0 or len(job.responsibilities) > 0
    assert "Python" in job.skills_required


def test_matcher():
    """Test achievement-job matching"""
    # Create test achievement
    achievement = Achievement(
        id="test_001",
        title="Python Developer",
        description="Developed Python applications",
        category="technical",
        skills=["Python", "AWS", "Docker"],
        keywords=["python", "aws", "development"]
    )
    
    # Create test job
    job = JobDescription(
        id="test_job",
        title="Senior Python Developer",
        company="Test Corp",
        description="Looking for Python expert",
        skills_required=["Python", "AWS"],
        skills_preferred=["Docker"]
    )
    
    # Match
    matcher = AchievementJobMatcher()
    matches = matcher.match_achievements_to_job([achievement], job)
    
    assert len(matches) == 1
    assert matches[0].relevance_score > 0
    assert len(matches[0].matched_skills) > 0


def test_ats_analyzer():
    """Test ATS analysis"""
    job_keywords = ["Python", "AWS", "Docker", "Kubernetes"]
    
    cv_text = """
    John Doe
    Software Engineer
    
    Skills: Python, AWS, Docker
    
    Experience:
    - Developed applications using Python
    - Deployed services on AWS
    - Containerized applications with Docker
    """
    
    analyzer = ATSAnalyzer()
    result = analyzer.analyze(job_keywords, cv_text)
    
    assert result.match_score > 0
    assert len(result.matched_keywords) >= 3  # Python, AWS, Docker
    assert "Kubernetes" in result.missing_keywords or result.match_score < 100


def test_ats_format_check():
    """Test ATS format checking"""
    analyzer = ATSAnalyzer()
    
    # Good text
    good_text = "This is a simple CV with standard ASCII characters."
    result = analyzer.check_ats_friendly_format(good_text)
    assert result['is_ats_friendly'] == True
    
    # Text with tabs
    bad_text = "This\thas\ttabs"
    result = analyzer.check_ats_friendly_format(bad_text)
    assert len(result['issues']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
