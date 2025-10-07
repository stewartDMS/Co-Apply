#!/usr/bin/env python3
"""
Co-Apply API Usage Example

This script demonstrates how to use the Co-Apply API deployed on Vercel.
It shows how to:
1. Parse job descriptions
2. Match achievements to jobs
3. Analyze ATS compatibility

Replace BASE_URL with your actual Vercel deployment URL.
"""

import requests
import json
import sys

# Replace with your Vercel deployment URL
BASE_URL = "https://your-app.vercel.app"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def example_1_parse_job():
    """Example 1: Parse a job description"""
    print_section("Example 1: Parse Job Description")
    
    job_description = """
    Senior Python Developer - Tech Corp
    
    We are looking for an experienced Python developer to join our backend team.
    
    Requirements:
    - 5+ years of Python development experience
    - Strong knowledge of Django or Flask frameworks
    - Experience with PostgreSQL and database design
    - Proficiency in REST API development
    - Experience with Git version control
    - Bachelor's degree in Computer Science or related field
    
    Preferred Qualifications:
    - Experience with Docker and containerization
    - AWS or other cloud platform experience
    - Knowledge of CI/CD pipelines
    - Experience with microservices architecture
    
    Responsibilities:
    - Design and develop scalable backend services
    - Optimize database queries and performance
    - Collaborate with frontend team on API design
    - Write clean, maintainable code with tests
    - Participate in code reviews
    """
    
    payload = {
        "description": job_description,
        "job_id": "techcorp-senior-python-001",
        "title": "Senior Python Developer",
        "company": "Tech Corp"
    }
    
    print("📤 Sending job description to API...")
    response = requests.post(f"{BASE_URL}/api/parse-job", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        job = result['job']
        
        print("✅ Job parsed successfully!\n")
        print(f"Job ID: {job['id']}")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"\nRequired Skills: {', '.join(job['skills_required'][:5])}")
        print(f"Preferred Skills: {', '.join(job['skills_preferred'][:5])}")
        print(f"\nResponsibilities: {len(job['responsibilities'])} items")
        print(f"Requirements: {len(job['requirements'])} items")
        
        return job
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def example_2_match_achievements(job):
    """Example 2: Match achievements to a job"""
    print_section("Example 2: Match Achievements to Job")
    
    achievements = [
        {
            "id": "ach-001",
            "title": "Built Scalable Django REST API",
            "description": "Designed and developed a high-performance REST API using Django and PostgreSQL, handling 10,000+ requests per minute",
            "category": "technical",
            "skills": ["Python", "Django", "PostgreSQL", "REST API", "Git"],
            "keywords": ["backend", "api", "scalable", "database", "performance"],
            "impact": "Improved application response time by 40% and supported 3x user growth",
            "metrics": "Handles 10,000 requests/min with <100ms latency",
            "date": "2023-01 to 2024-01"
        },
        {
            "id": "ach-002",
            "title": "Implemented CI/CD Pipeline with Docker",
            "description": "Set up automated testing and deployment pipeline using Docker, GitHub Actions, and AWS ECS",
            "category": "technical",
            "skills": ["Docker", "AWS", "CI/CD", "Git", "Python"],
            "keywords": ["devops", "automation", "cloud", "containers"],
            "impact": "Reduced deployment time from 2 hours to 15 minutes",
            "metrics": "99.9% uptime, zero-downtime deployments",
            "date": "2023-06 to 2024-02"
        },
        {
            "id": "ach-003",
            "title": "Database Performance Optimization",
            "description": "Optimized PostgreSQL queries and implemented caching strategy, dramatically improving application performance",
            "category": "technical",
            "skills": ["PostgreSQL", "SQL", "Python", "Redis"],
            "keywords": ["database", "optimization", "performance", "caching"],
            "impact": "Reduced average query time by 70%",
            "metrics": "From 500ms to 150ms average query time",
            "date": "2023-09 to 2023-12"
        },
        {
            "id": "ach-004",
            "title": "Led Frontend Team Migration to React",
            "description": "Led team of 4 developers in migrating legacy frontend to React with TypeScript",
            "category": "leadership",
            "skills": ["React", "TypeScript", "JavaScript", "Team Leadership"],
            "keywords": ["frontend", "leadership", "migration"],
            "impact": "Improved code maintainability and developer productivity",
            "metrics": "50% reduction in bug reports",
            "date": "2022-06 to 2023-03"
        }
    ]
    
    payload = {
        "achievements": achievements,
        "job": job
    }
    
    print("📤 Matching achievements to job requirements...")
    response = requests.post(f"{BASE_URL}/api/analyze-match", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        matches = result['matches']
        
        print(f"✅ Found {result['total_matches']} matches!\n")
        
        # Sort by relevance score
        matches.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        for i, match in enumerate(matches, 1):
            score = match['relevance_score'] * 100
            
            # Determine relevance level
            if score >= 60:
                level = "🟢 High"
            elif score >= 30:
                level = "🟡 Medium"
            else:
                level = "🔴 Low"
            
            print(f"{i}. {match['achievement_title']}")
            print(f"   Relevance: {level} ({score:.1f}%)")
            print(f"   Matched Skills: {', '.join(match['matched_skills'][:4])}")
            if match['reasons']:
                print(f"   Reasons: {match['reasons'][0]}")
            print()
        
        return matches
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def example_3_ats_analysis():
    """Example 3: Analyze ATS compatibility of a CV"""
    print_section("Example 3: Analyze ATS Compatibility")
    
    sample_cv = """
    John Doe
    Senior Python Developer
    john.doe@email.com | +1-555-0123 | linkedin.com/in/johndoe
    
    PROFESSIONAL SUMMARY
    Experienced Python developer with 6+ years of expertise in building scalable backend
    systems using Django and PostgreSQL. Strong background in REST API development,
    database optimization, and cloud deployment with Docker.
    
    TECHNICAL SKILLS
    Languages: Python, SQL, JavaScript
    Frameworks: Django, Flask, REST API
    Databases: PostgreSQL, Redis, MongoDB
    Tools: Docker, Git, AWS, CI/CD
    
    WORK EXPERIENCE
    
    Senior Python Developer | Tech Solutions Inc | 2021-Present
    - Developed and maintained Django REST APIs serving 10,000+ requests per minute
    - Optimized PostgreSQL database queries, reducing response time by 40%
    - Implemented Docker containerization for microservices architecture
    - Set up CI/CD pipelines using GitHub Actions and AWS ECS
    - Collaborated with frontend team on API design and integration
    
    Python Developer | StartupCo | 2018-2021
    - Built scalable backend services using Flask and PostgreSQL
    - Designed and implemented RESTful APIs for mobile applications
    - Performed database schema design and optimization
    - Mentored junior developers on Python best practices
    
    EDUCATION
    Bachelor of Science in Computer Science | University of Technology | 2018
    
    ACHIEVEMENTS
    - Reduced API response time by 70% through query optimization
    - Led migration to microservices architecture with zero downtime
    - Implemented automated testing, increasing code coverage to 95%
    """
    
    keywords = [
        "Python", "Django", "Flask", "PostgreSQL", "REST API",
        "Docker", "AWS", "CI/CD", "Git", "Microservices",
        "SQL", "Database", "Backend", "API", "Scalable"
    ]
    
    required_skills = [
        "Python", "Django", "PostgreSQL", "REST API", "Git"
    ]
    
    payload = {
        "document": sample_cv,
        "keywords": keywords,
        "required_skills": required_skills
    }
    
    print("📤 Analyzing CV for ATS compatibility...")
    response = requests.post(f"{BASE_URL}/api/ats-analyze", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        score = result['match_score']
        
        # Determine score level
        if score >= 85:
            level = "🟢 Excellent"
        elif score >= 70:
            level = "🟢 Good"
        elif score >= 50:
            level = "🟡 Fair"
        else:
            level = "🔴 Poor"
        
        print(f"✅ Analysis complete!\n")
        print(f"ATS Match Score: {level} ({score:.1f}%)\n")
        
        print(f"✅ Matched Keywords ({len(result['matched_keywords'])}):")
        for keyword in result['matched_keywords'][:10]:
            print(f"   • {keyword}")
        
        if result['missing_keywords']:
            print(f"\n❌ Missing Keywords ({len(result['missing_keywords'])}):")
            for keyword in result['missing_keywords'][:5]:
                print(f"   • {keyword}")
        
        if result['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in result['recommendations'][:5]:
                print(f"   • {rec}")
        
        return result
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def main():
    """Run all examples"""
    print("\n" + "🚀 Co-Apply API Usage Examples".center(60))
    print("=" * 60)
    print(f"\nBase URL: {BASE_URL}\n")
    
    # Check if API is accessible
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ API is not accessible. Please check the BASE_URL.")
            print(f"   Current URL: {BASE_URL}")
            print("\n   Update BASE_URL in this script with your Vercel deployment URL.")
            sys.exit(1)
        print("✅ API is accessible and healthy!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print(f"\n   Current URL: {BASE_URL}")
        print("   Update BASE_URL in this script with your Vercel deployment URL.")
        print("\n   For local testing, use: https://your-app.vercel.app")
        sys.exit(1)
    
    # Run examples
    job = example_1_parse_job()
    
    if job:
        matches = example_2_match_achievements(job)
    
    ats_result = example_3_ats_analysis()
    
    print_section("Summary")
    print("✅ All examples completed successfully!")
    print("\n📚 Learn more:")
    print("   • API Reference: API_REFERENCE.md")
    print("   • Deployment Guide: DEPLOYMENT.md")
    print("   • GitHub: https://github.com/stewartDMS/Co-Apply")
    print("\n")

if __name__ == "__main__":
    main()
