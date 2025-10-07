# Co-Apply API Examples

This directory contains example scripts demonstrating how to use the Co-Apply API.

## 📁 Files

### api_usage_example.py

A comprehensive example showing how to:
1. Parse job descriptions
2. Match achievements to jobs
3. Analyze ATS compatibility

## 🚀 Usage

### Step 1: Update the Base URL

Edit `api_usage_example.py` and replace the BASE_URL:

```python
# Replace with your actual Vercel deployment URL
BASE_URL = "https://your-app.vercel.app"
```

For local testing:
```python
BASE_URL = "http://127.0.0.1:5000"
```

### Step 2: Run the Example

```bash
cd examples
python api_usage_example.py
```

### Step 3: Review the Output

The script will:
- Parse a sample job description
- Match sample achievements to the job
- Analyze a sample CV for ATS compatibility
- Display detailed results for each operation

## 📝 Output Example

```
🚀 Co-Apply API Usage Examples
============================================================

Base URL: https://your-app.vercel.app

✅ API is accessible and healthy!

============================================================
  Example 1: Parse Job Description
============================================================

📤 Sending job description to API...
✅ Job parsed successfully!

Job ID: techcorp-senior-python-001
Title: Senior Python Developer
Company: Tech Corp

Required Skills: Python, Django, PostgreSQL, REST API, Git
Preferred Skills: Docker, AWS, CI/CD

Responsibilities: 5 items
Requirements: 4 items

============================================================
  Example 2: Match Achievements to Job
============================================================

📤 Matching achievements to job requirements...
✅ Found 4 matches!

1. Built Scalable Django REST API
   Relevance: 🟢 High (85.3%)
   Matched Skills: Python, Django, PostgreSQL, REST API
   Reasons: Matches 4 required skills

...
```

## 🔧 Customization

You can modify the example to use your own data:

### Custom Job Description

```python
job_description = """
Your actual job description here...
"""
```

### Custom Achievements

```python
achievements = [
    {
        "id": "your-ach-001",
        "title": "Your Achievement",
        "description": "What you did...",
        "skills": ["Skill1", "Skill2"],
        "keywords": ["keyword1", "keyword2"]
    }
]
```

### Custom CV

```python
sample_cv = """
Your actual CV content here...
"""
```

## 📚 Additional Resources

- [API Reference](../API_REFERENCE.md) - Complete API documentation
- [Deployment Guide](../DEPLOYMENT.md) - How to deploy to Vercel
- [Quick Start](../VERCEL_QUICKSTART.md) - Fast deployment guide

## 💡 Tips

1. **Rate Limiting**: Be mindful of API rate limits when making multiple requests
2. **Error Handling**: Always check response status codes
3. **Caching**: Cache parsed job descriptions to reduce API calls
4. **Validation**: Validate input data before sending to the API

## 🐛 Troubleshooting

### Connection Refused

Make sure:
- The API is deployed and running
- The BASE_URL is correct
- You have internet connection (for remote APIs)

### 500 Internal Server Error

Check:
- Your request payload format matches the expected schema
- All required fields are provided
- Field types are correct (arrays, strings, etc.)

### Timeout Errors

Try:
- Reducing the size of your request
- Increasing the request timeout
- Using a different network connection

## 🆘 Need Help?

- [GitHub Issues](https://github.com/stewartDMS/Co-Apply/issues)
- [Full Documentation](../README.md)
