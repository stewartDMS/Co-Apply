# Co-Apply API Reference

Complete reference guide for the Co-Apply REST API.

## Base URL

- **Production**: `https://your-app.vercel.app`
- **Local Development**: `http://127.0.0.1:5000`

## Authentication

Currently, the API does not require authentication. For production use, consider implementing:
- API keys
- JWT tokens
- OAuth 2.0

## Response Format

All API responses are in JSON format and follow this structure:

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error message description"
}
```

## Endpoints

### Health Check

Check if the API is running and healthy.

**Endpoint**: `GET /api/health`

**Parameters**: None

**Response**:
```json
{
  "status": "healthy",
  "service": "Co-Apply API",
  "version": "0.1.0"
}
```

**Example**:
```bash
curl https://your-app.vercel.app/api/health
```

---

### Get Version

Get version information about the API and Python runtime.

**Endpoint**: `GET /api/version`

**Parameters**: None

**Response**:
```json
{
  "version": "0.1.0",
  "name": "co-apply",
  "python_version": "3.12.x"
}
```

**Example**:
```bash
curl https://your-app.vercel.app/api/version
```

---

### Parse Job Description

Parse a job description and extract structured information including skills, responsibilities, and requirements.

**Endpoint**: `POST /api/parse-job`

**Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
  "description": "Job description text...",
  "job_id": "unique-job-id",
  "title": "Job Title",
  "company": "Company Name"
}
```

**Parameters**:
- `description` (required): The full job description text
- `job_id` (optional): Unique identifier for the job (default: "temp-job")
- `title` (optional): Job title (default: "Unknown Position")
- `company` (optional): Company name (default: "Unknown Company")

**Response**:
```json
{
  "success": true,
  "job": {
    "id": "unique-job-id",
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "skills_required": ["Python", "Django", "PostgreSQL"],
    "skills_preferred": ["Docker", "AWS"],
    "responsibilities": ["Develop APIs", "Optimize performance"],
    "requirements": ["5+ years experience", "Bachelor's degree"]
  }
}
```

**Example**:
```bash
curl -X POST https://your-app.vercel.app/api/parse-job \
  -H "Content-Type: application/json" \
  -d '{
    "description": "We are looking for a Senior Python Developer with Django experience...",
    "job_id": "tech-corp-001",
    "title": "Senior Python Developer",
    "company": "Tech Corp"
  }'
```

**Python Example**:
```python
import requests

data = {
    "description": "We need a Python developer with Django and PostgreSQL experience...",
    "job_id": "job-001",
    "title": "Python Developer",
    "company": "Tech Corp"
}

response = requests.post(
    "https://your-app.vercel.app/api/parse-job",
    json=data
)
print(response.json())
```

---

### Analyze Achievement-Job Match

Match achievements against job requirements and calculate relevance scores.

**Endpoint**: `POST /api/analyze-match`

**Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
  "achievements": [
    {
      "id": "ach-001",
      "title": "Achievement Title",
      "description": "Detailed description",
      "category": "technical",
      "skills": ["Python", "Django"],
      "keywords": ["backend", "api"],
      "impact": "Impact description",
      "metrics": "Quantifiable results",
      "date": "YYYY-MM to YYYY-MM"
    }
  ],
  "job": {
    "job_id": "job-001",
    "title": "Job Title",
    "company": "Company Name",
    "description": "Job description",
    "skills_required": ["Python", "Django"],
    "skills_preferred": ["Docker"],
    "responsibilities": [],
    "requirements": []
  }
}
```

**Parameters**:
- `achievements` (required): Array of achievement objects
  - `id`: Unique achievement identifier
  - `title`: Achievement title
  - `description`: Detailed description
  - `category`: Category (technical, leadership, project, certification)
  - `skills`: Array of skills used
  - `keywords`: Array of relevant keywords
  - `impact` (optional): Impact statement
  - `metrics` (optional): Quantifiable metrics
  - `date` (optional): Date range
- `job` (required): Job description object
  - `job_id`: Job identifier
  - `title`: Job title
  - `company`: Company name
  - `skills_required`: Required skills array
  - `skills_preferred` (optional): Preferred skills array
  - Other fields are optional

**Response**:
```json
{
  "success": true,
  "matches": [
    {
      "achievement_id": "ach-001",
      "achievement_title": "Built Django REST API",
      "relevance_score": 0.85,
      "matched_skills": ["Python", "Django", "REST API"],
      "reasons": [
        "Matches required skill: Python",
        "Matches required skill: Django"
      ]
    }
  ],
  "total_matches": 1
}
```

**Relevance Score**:
- `0.0 - 0.3`: Low relevance
- `0.3 - 0.6`: Medium relevance  
- `0.6 - 0.8`: High relevance
- `0.8 - 1.0`: Very high relevance

**Example**:
```bash
curl -X POST https://your-app.vercel.app/api/analyze-match \
  -H "Content-Type: application/json" \
  -d '{
    "achievements": [{
      "id": "ach-001",
      "title": "Built Django API",
      "description": "Created REST API with Django",
      "skills": ["Python", "Django", "PostgreSQL"],
      "keywords": ["backend", "api"]
    }],
    "job": {
      "job_id": "job-001",
      "title": "Python Developer",
      "company": "Tech Corp",
      "skills_required": ["Python", "Django"]
    }
  }'
```

**Python Example**:
```python
import requests

data = {
    "achievements": [
        {
            "id": "ach-001",
            "title": "Built Django Application",
            "description": "Developed scalable web app",
            "skills": ["Python", "Django", "PostgreSQL"],
            "keywords": ["web", "backend"]
        }
    ],
    "job": {
        "job_id": "job-001",
        "title": "Python Developer",
        "company": "Tech Corp",
        "skills_required": ["Python", "Django"]
    }
}

response = requests.post(
    "https://your-app.vercel.app/api/analyze-match",
    json=data
)
print(response.json())
```

---

### Analyze ATS Compatibility

Analyze a document for Applicant Tracking System (ATS) compatibility by checking keyword matches.

**Endpoint**: `POST /api/ats-analyze`

**Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
  "document": "Full document text...",
  "keywords": ["Python", "Django", "PostgreSQL"],
  "required_skills": ["Python", "Django"]
}
```

**Parameters**:
- `document` (required): The full document text (CV, resume, etc.)
- `keywords` (required): Array of all keywords to check
- `required_skills` (optional): Array of required skills for priority checking

**Response**:
```json
{
  "success": true,
  "match_score": 85.5,
  "matched_keywords": ["Python", "Django", "PostgreSQL", "REST API"],
  "missing_keywords": ["Docker", "AWS"],
  "recommendations": [
    "Add 'Docker' to your CV",
    "Add 'AWS' to your CV"
  ]
}
```

**Match Score**:
- `0-50%`: Poor ATS compatibility
- `50-70%`: Fair ATS compatibility
- `70-85%`: Good ATS compatibility
- `85-100%`: Excellent ATS compatibility

**Example**:
```bash
curl -X POST https://your-app.vercel.app/api/ats-analyze \
  -H "Content-Type: application/json" \
  -d '{
    "document": "John Doe\nSenior Python Developer\nSkills: Python, Django, PostgreSQL...",
    "keywords": ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
    "required_skills": ["Python", "Django", "PostgreSQL"]
  }'
```

**Python Example**:
```python
import requests

data = {
    "document": """
    John Doe
    Senior Python Developer
    
    Skills: Python, Django, PostgreSQL, REST API
    
    Experience:
    - Built scalable Django applications
    - Optimized PostgreSQL databases
    """,
    "keywords": ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
    "required_skills": ["Python", "Django", "PostgreSQL"]
}

response = requests.post(
    "https://your-app.vercel.app/api/ats-analyze",
    json=data
)
result = response.json()
print(f"ATS Score: {result['match_score']}%")
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Endpoint doesn't exist |
| 500 | Internal Server Error |

## Rate Limiting

The API currently has no rate limiting on Vercel's free tier, but Vercel enforces:
- 100GB bandwidth per month
- 100 hours of serverless function execution
- Maximum 10 second execution time per request

For production use, consider implementing rate limiting.

## CORS

CORS is not enabled by default. To enable cross-origin requests, add Flask-CORS:

```python
from flask_cors import CORS
CORS(app)
```

## Best Practices

1. **Error Handling**: Always check for errors in responses
2. **Validation**: Validate input data before sending requests
3. **Timeouts**: Set appropriate timeouts for requests
4. **Caching**: Cache parsed job descriptions to reduce API calls
5. **Batching**: For multiple achievements, send them in a single request

## Example Client

Here's a complete Python client example:

```python
import requests
from typing import List, Dict

class CoApplyClient:
    def __init__(self, base_url: str = "https://your-app.vercel.app"):
        self.base_url = base_url
        
    def health_check(self) -> Dict:
        """Check API health"""
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()
    
    def parse_job(self, description: str, job_id: str, 
                  title: str = "", company: str = "") -> Dict:
        """Parse a job description"""
        data = {
            "description": description,
            "job_id": job_id,
            "title": title,
            "company": company
        }
        response = requests.post(
            f"{self.base_url}/api/parse-job",
            json=data
        )
        return response.json()
    
    def analyze_match(self, achievements: List[Dict], job: Dict) -> Dict:
        """Analyze achievement-job matches"""
        data = {
            "achievements": achievements,
            "job": job
        }
        response = requests.post(
            f"{self.base_url}/api/analyze-match",
            json=data
        )
        return response.json()
    
    def analyze_ats(self, document: str, keywords: List[str],
                    required_skills: List[str] = None) -> Dict:
        """Analyze ATS compatibility"""
        data = {
            "document": document,
            "keywords": keywords,
            "required_skills": required_skills or []
        }
        response = requests.post(
            f"{self.base_url}/api/ats-analyze",
            json=data
        )
        return response.json()

# Usage
client = CoApplyClient("https://your-app.vercel.app")

# Check health
print(client.health_check())

# Parse job
job_result = client.parse_job(
    description="Looking for Python developer...",
    job_id="job-001",
    title="Python Developer",
    company="Tech Corp"
)
print(job_result)
```

## Testing

Use the provided test script to verify all endpoints:

```bash
python test_api.py --url https://your-app.vercel.app
```

Or use the shell script for comprehensive testing:

```bash
./scripts/test_deployment.sh
```

## Support

For issues or questions:
- GitHub Issues: [github.com/stewartDMS/Co-Apply/issues](https://github.com/stewartDMS/Co-Apply/issues)
- Documentation: [github.com/stewartDMS/Co-Apply](https://github.com/stewartDMS/Co-Apply)

---

**Co-Apply API v0.1.0**
