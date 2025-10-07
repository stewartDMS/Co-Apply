#!/usr/bin/env python3
"""
Test script for Co-Apply API endpoints
Run this locally before deploying to verify all endpoints work correctly
"""

import requests
import json
import sys

def test_api(base_url="http://127.0.0.1:5000"):
    """Test all API endpoints"""
    
    print("🧪 Testing Co-Apply API\n")
    print(f"Base URL: {base_url}\n")
    
    # Test 1: Health Check
    print("1️⃣  Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
        else:
            print(f"   ❌ Health check failed: {response.status_code}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 2: Version
    print("2️⃣  Testing Version Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/version", timeout=5)
        if response.status_code == 200:
            print("   ✅ Version check passed")
            print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
        else:
            print(f"   ❌ Version check failed: {response.status_code}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 3: Parse Job
    print("3️⃣  Testing Job Parsing...")
    job_data = {
        "description": """
        We are looking for a Senior Python Developer with experience in Django and PostgreSQL.
        
        Requirements:
        - 5+ years of Python experience
        - Strong knowledge of Django framework
        - Experience with PostgreSQL and database design
        - REST API development
        - Git version control
        
        Preferred:
        - Docker and containerization
        - AWS or cloud experience
        - CI/CD pipelines
        """,
        "job_id": "test-001",
        "title": "Senior Python Developer",
        "company": "Test Corp"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/parse-job",
            json=job_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Job parsing passed")
            result = response.json()
            print(f"   Parsed skills: {result.get('job', {}).get('skills_required', [])}\n")
        else:
            print(f"   ❌ Job parsing failed: {response.status_code}")
            print(f"   Response: {response.text}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 4: Analyze Match
    print("4️⃣  Testing Achievement-Job Matching...")
    match_data = {
        "achievements": [
            {
                "id": "ach-001",
                "title": "Built Django REST API",
                "description": "Developed a scalable REST API using Django and PostgreSQL",
                "category": "technical",
                "skills": ["Python", "Django", "PostgreSQL", "REST API"],
                "keywords": ["backend", "api", "database", "scalable"],
                "impact": "Improved application response time by 40%",
                "metrics": "Handles 10,000 requests per minute",
                "date": "2023-01 to 2024-01"
            },
            {
                "id": "ach-002",
                "title": "Implemented CI/CD Pipeline",
                "description": "Set up automated testing and deployment using Docker and AWS",
                "category": "technical",
                "skills": ["Docker", "AWS", "CI/CD", "Git"],
                "keywords": ["devops", "automation", "cloud"],
                "impact": "Reduced deployment time from hours to minutes",
                "metrics": "99.9% uptime achieved",
                "date": "2023-06 to 2024-02"
            }
        ],
        "job": {
            "job_id": "test-001",
            "title": "Senior Python Developer",
            "company": "Test Corp",
            "description": "Looking for Python developer",
            "skills_required": ["Python", "Django", "PostgreSQL", "REST API"],
            "skills_preferred": ["Docker", "AWS", "CI/CD"],
            "responsibilities": ["Develop APIs", "Optimize database"],
            "qualifications": ["5+ years experience"]
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/analyze-match",
            json=match_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Match analysis passed")
            result = response.json()
            print(f"   Total matches: {result.get('total_matches', 0)}")
            for match in result.get('matches', [])[:2]:
                print(f"   - {match['achievement_title']}: {match['relevance_score']:.2%} relevant\n")
        else:
            print(f"   ❌ Match analysis failed: {response.status_code}")
            print(f"   Response: {response.text}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 5: ATS Analysis
    print("5️⃣  Testing ATS Analysis...")
    ats_data = {
        "document": """
        John Doe
        Senior Python Developer
        
        Skills: Python, Django, PostgreSQL, REST API, Git
        
        Experience:
        - Built Django REST API with PostgreSQL
        - Developed scalable backend systems
        - Implemented database optimization
        """,
        "keywords": ["Python", "Django", "PostgreSQL", "REST API", "Docker", "AWS"],
        "required_skills": ["Python", "Django", "PostgreSQL"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/ats-analyze",
            json=ats_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ ATS analysis passed")
            result = response.json()
            print(f"   Match score: {result.get('match_score', 0):.1f}%")
            print(f"   Matched keywords: {len(result.get('matched_keywords', []))}")
            print(f"   Missing keywords: {len(result.get('missing_keywords', []))}\n")
        else:
            print(f"   ❌ ATS analysis failed: {response.status_code}")
            print(f"   Response: {response.text}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    print("=" * 60)
    print("✅ All API tests passed successfully!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Co-Apply API")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:5000",
        help="Base URL of the API (default: http://127.0.0.1:5000)"
    )
    
    args = parser.parse_args()
    
    success = test_api(args.url)
    sys.exit(0 if success else 1)
