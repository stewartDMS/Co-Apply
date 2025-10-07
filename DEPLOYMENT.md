# Co-Apply Deployment Guide

This guide provides instructions for deploying Co-Apply to Vercel as a web application with a REST API.

> **📌 Important Note**: This repository is configured to deploy to an **existing Vercel project** named 'co-apply'. Contributors and maintainers should link to this existing project rather than creating new ones. See the "Deployment via Vercel CLI" section for instructions on linking to the existing project.

## 🚀 Quick Deploy to Vercel

### Prerequisites

1. A [Vercel account](https://vercel.com/signup)
2. [Vercel CLI](https://vercel.com/docs/cli) installed (optional, but recommended)
3. GitHub account with this repository
4. Access to the existing 'co-apply' Vercel project (for contributors with deployment permissions)

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/stewartDMS/Co-Apply)

Click the button above to deploy Co-Apply to Vercel with one click.

### Manual Deployment via Vercel Dashboard

1. **Fork or Clone the Repository**
   ```bash
   git clone https://github.com/stewartDMS/Co-Apply.git
   cd Co-Apply
   ```

2. **Login to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

3. **Import Project**
   - Click "Add New Project"
   - Select your GitHub repository
   - Vercel will automatically detect the configuration from `vercel.json`

4. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty, handled by Vercel)
   - **Output Directory**: (leave empty, handled by Vercel)

5. **Environment Variables** (Optional)
   - Add any environment variables from `.env.example` if needed
   - For basic functionality, no environment variables are required

6. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (usually 1-2 minutes)
   - Your app will be live at `https://your-project.vercel.app`

### Deployment via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Link to Existing Project (Recommended)**
   
   This repository is configured to deploy to an existing Vercel project named 'co-apply'.
   
   ```bash
   cd Co-Apply
   vercel link
   ```
   
   Follow the prompts:
   - Link to existing project: **Y**
   - Which scope: **(select the appropriate account/organization)**
   - Link to which project: **co-apply**
   
   > **Note**: If you don't have access to the existing project, contact the repository maintainer or create your own deployment by following the "Alternative: Create New Project" section below.

4. **Deploy**
   ```bash
   vercel
   ```

5. **Production Deployment**
   ```bash
   vercel --prod
   ```

### Alternative: Create New Project

If you need to create a new Vercel project (not recommended for contributors):

```bash
cd Co-Apply
vercel
```

Follow the prompts:
- Set up and deploy: Y
- Which scope: (select your account)
- Link to existing project: N
- Project name: co-apply-fork (use a different name)
- In which directory: ./
- Override settings: N

Then deploy to production:
```bash
vercel --prod
```

## 📋 Configuration Files

### vercel.json

The `vercel.json` file configures how Vercel builds and serves your application:

```json
{
  "version": 2,
  "name": "co-apply",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### requirements.txt

All Python dependencies are listed in `requirements.txt` and will be automatically installed during deployment.

### .vercelignore

Similar to `.gitignore`, this file specifies which files should not be uploaded to Vercel.

### .vercel/project.json

This file links the repository to the existing Vercel project. It contains:

```json
{
  "projectId": "prj_PLACEHOLDER_VERCEL_PROJECT_ID",
  "orgId": "team_PLACEHOLDER_VERCEL_ORG_ID"
}
```

**Important Notes:**
- The repository contains placeholder IDs for documentation purposes
- When you run `vercel link` or deploy, the CLI will update this file with actual project IDs
- The `.vercel` directory (except placeholder files) is in `.gitignore` to prevent committing sensitive project information
- Contributors can use `vercel link` to connect to the existing project if they have access
- See `.vercel/README.md` for more details on obtaining project IDs

## 🌐 API Endpoints

Once deployed, your application will expose the following endpoints:

### Health Check
```bash
GET https://your-app.vercel.app/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Co-Apply API",
  "version": "0.1.0"
}
```

### Get Version
```bash
GET https://your-app.vercel.app/api/version
```

**Response:**
```json
{
  "version": "0.1.0",
  "name": "co-apply",
  "python_version": "3.12.x"
}
```

### Parse Job Description
```bash
POST https://your-app.vercel.app/api/parse-job
Content-Type: application/json

{
  "description": "We are looking for a Senior Python Developer...",
  "job_id": "job-001",
  "title": "Senior Python Developer",
  "company": "Tech Corp"
}
```

**Response:**
```json
{
  "success": true,
  "job": {
    "id": "job-001",
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "skills_required": ["Python", "Django", "PostgreSQL"],
    "skills_preferred": ["Docker", "AWS"],
    "responsibilities": [...],
    "qualifications": [...]
  }
}
```

### Analyze Achievement-Job Match
```bash
POST https://your-app.vercel.app/api/analyze-match
Content-Type: application/json

{
  "achievements": [
    {
      "id": "ach-001",
      "title": "Built REST API",
      "description": "Developed a scalable REST API using Django",
      "skills": ["Python", "Django", "REST API"],
      "keywords": ["backend", "api", "scalable"]
    }
  ],
  "job": {
    "job_id": "job-001",
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "skills_required": ["Python", "Django", "REST API"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "matches": [
    {
      "achievement_id": "ach-001",
      "achievement_title": "Built REST API",
      "relevance_score": 0.85,
      "matched_skills": ["Python", "Django", "REST API"],
      "reasoning": "High relevance due to matching core skills"
    }
  ],
  "total_matches": 1
}
```

### Analyze ATS Compatibility
```bash
POST https://your-app.vercel.app/api/ats-analyze
Content-Type: application/json

{
  "document": "John Doe\nSenior Python Developer\nSkills: Python, Django, PostgreSQL...",
  "keywords": ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
  "required_skills": ["Python", "Django", "PostgreSQL"]
}
```

**Response:**
```json
{
  "success": true,
  "match_score": 85.5,
  "matched_keywords": ["Python", "Django", "PostgreSQL"],
  "missing_keywords": ["Docker", "AWS"],
  "recommendations": ["Add 'Docker' to your CV", "Add 'AWS' to your CV"]
}
```

## 🧪 Testing Your Deployment

### Using curl

1. **Test Health Endpoint**
   ```bash
   curl https://your-app.vercel.app/api/health
   ```

2. **Test Version Endpoint**
   ```bash
   curl https://your-app.vercel.app/api/version
   ```

3. **Test Job Parsing**
   ```bash
   curl -X POST https://your-app.vercel.app/api/parse-job \
     -H "Content-Type: application/json" \
     -d '{
       "description": "Looking for a Python developer with Django experience",
       "job_id": "test-001",
       "title": "Python Developer",
       "company": "Test Corp"
     }'
   ```

### Using Python

Create a test script `test_api.py`:

```python
import requests
import json

# Base URL of your deployed app
BASE_URL = "https://your-app.vercel.app"

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    print("Health Check:", response.json())

def test_parse_job():
    data = {
        "description": "We need a Python developer with Django and PostgreSQL experience",
        "job_id": "test-001",
        "title": "Python Developer",
        "company": "Test Corp"
    }
    response = requests.post(f"{BASE_URL}/api/parse-job", json=data)
    print("Job Parse:", json.dumps(response.json(), indent=2))

def test_analyze_match():
    data = {
        "achievements": [
            {
                "id": "ach-001",
                "title": "Built Django Application",
                "description": "Created a web app with Django and PostgreSQL",
                "skills": ["Python", "Django", "PostgreSQL"],
                "keywords": ["web", "backend", "database"]
            }
        ],
        "job": {
            "job_id": "test-001",
            "title": "Python Developer",
            "company": "Test Corp",
            "skills_required": ["Python", "Django", "PostgreSQL"]
        }
    }
    response = requests.post(f"{BASE_URL}/api/analyze-match", json=data)
    print("Match Analysis:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_health()
    test_parse_job()
    test_analyze_match()
```

Run the test:
```bash
python test_api.py
```

### Using the Web Interface

Simply visit `https://your-app.vercel.app` in your browser to see the landing page with API documentation and status.

## 🔧 Managing Your Deployment

### Viewing Logs

1. **Via Vercel Dashboard**
   - Go to your project on vercel.com
   - Click on "Deployments"
   - Select a deployment
   - Click "View Function Logs"

2. **Via Vercel CLI**
   ```bash
   vercel logs
   ```

### Updating Your Deployment

1. **Automatic Deployments** (Recommended)
   - Connect your GitHub repository to Vercel
   - Every push to the main branch will trigger a new deployment
   - Pull requests will create preview deployments

2. **Manual Deployments**
   ```bash
   git pull origin main
   vercel --prod
   ```

### Rolling Back

If a deployment has issues:

1. **Via Dashboard**
   - Go to "Deployments"
   - Find a previous working deployment
   - Click the three dots menu
   - Select "Promote to Production"

2. **Via CLI**
   ```bash
   vercel rollback
   ```

## 🔐 Environment Variables

To add environment variables:

1. **Via Dashboard**
   - Go to your project settings
   - Click "Environment Variables"
   - Add variables (Name, Value, Environment)

2. **Via CLI**
   ```bash
   vercel env add VARIABLE_NAME
   ```

Common environment variables:
- `FLASK_ENV`: production
- `FLASK_DEBUG`: 0
- `PYTHONPATH`: /var/task/src (automatically set)

## 🐛 Troubleshooting

### Build Failures

**Issue**: Build fails with "Module not found"
**Solution**: Ensure all dependencies are listed in `requirements.txt`

**Issue**: Build timeout
**Solution**: Reduce dependencies or contact Vercel support for increased limits

### Runtime Errors

**Issue**: 500 Internal Server Error
**Solution**: Check function logs in Vercel dashboard

**Issue**: Import errors
**Solution**: Verify PYTHONPATH is correctly set in `vercel.json`

### Performance Issues

**Issue**: Slow cold starts
**Solution**: 
- Reduce dependencies
- Use Vercel Pro for better cold start performance
- Consider using regional deployments

## 📊 Monitoring

### Built-in Metrics

Vercel provides built-in analytics:
- Request count
- Error rate
- Response time
- Bandwidth usage

Access via: Project → Analytics

### Custom Monitoring

For advanced monitoring, integrate with:
- Sentry for error tracking
- DataDog for APM
- LogRocket for session replay

## 🔒 Security

### Best Practices

1. **Environment Variables**: Never commit secrets to Git
2. **HTTPS**: All Vercel deployments use HTTPS by default
3. **CORS**: Configure CORS if needed for frontend apps
4. **Rate Limiting**: Implement rate limiting for public APIs
5. **Authentication**: Add authentication for sensitive endpoints

### Adding CORS

If you need to allow cross-origin requests:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

Add to requirements.txt:
```
flask-cors>=4.0.0
```

## 📈 Scaling

Vercel automatically scales your application:
- **Serverless**: Each request is handled independently
- **Global CDN**: Content is served from the nearest edge location
- **Auto-scaling**: Handles traffic spikes automatically

### Limits (Free Tier)

- 100 GB bandwidth per month
- 100 hours of serverless function execution
- 6,000 minutes of build time

For higher limits, upgrade to Vercel Pro or Enterprise.

## 🆘 Support

### Getting Help

1. **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
2. **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
3. **Co-Apply Issues**: [github.com/stewartDMS/Co-Apply/issues](https://github.com/stewartDMS/Co-Apply/issues)

### Common Resources

- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [Serverless Functions](https://vercel.com/docs/functions/serverless-functions)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Custom Domains](https://vercel.com/docs/projects/domains)

## 🎯 Next Steps

After successful deployment:

1. ✅ Test all API endpoints
2. ✅ Set up custom domain (optional)
3. ✅ Configure GitHub integration for automatic deployments
4. ✅ Add monitoring and error tracking
5. ✅ Implement authentication if needed
6. ✅ Add rate limiting for production use
7. ✅ Document your API for users

---

**Congratulations!** 🎉 Your Co-Apply application is now live on Vercel!
