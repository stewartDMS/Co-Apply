"""
Vercel serverless function for Co-Apply API
Main entry point for the web application
"""

from flask import Flask, jsonify, request, render_template_string
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__)

# Simple HTML landing page
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Co-Apply - Job Application Copilot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        header h1 {
            font-size: 3em;
            margin-bottom: 10px;
        }
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }
        .feature {
            padding: 20px;
            border: 2px solid #667eea;
            border-radius: 8px;
            transition: transform 0.3s;
        }
        .feature:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        .feature h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .api-section {
            background: #f7f7f7;
            padding: 30px;
            border-radius: 8px;
            margin: 30px 0;
        }
        .api-section h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        .endpoint {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        .endpoint code {
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }
        .button {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border-radius: 5px;
            text-decoration: none;
            margin: 10px 10px 10px 0;
            transition: background 0.3s;
        }
        .button:hover {
            background: #764ba2;
        }
        .status {
            padding: 20px;
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            margin: 20px 0;
        }
        footer {
            text-align: center;
            padding: 20px;
            color: #666;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Co-Apply</h1>
            <p>Your AI-powered job application copilot</p>
        </header>
        
        <div class="content">
            <div class="status">
                <strong>✓ Deployment Status:</strong> Live and running on Vercel
            </div>

            <h2>About Co-Apply</h2>
            <p>Co-Apply is an intelligent job application assistant that helps you create tailored, ATS-optimized CVs and cover letters by matching your achievements with job requirements. Built with privacy in mind, it runs locally and requires minimal external APIs.</p>

            <div class="features">
                <div class="feature">
                    <h3>✨ Achievement Library</h3>
                    <p>Maintain a structured database of your skills, projects, and accomplishments.</p>
                </div>
                <div class="feature">
                    <h3>🎯 Smart Matching</h3>
                    <p>Automatically match your achievements with job requirements using NLP.</p>
                </div>
                <div class="feature">
                    <h3>📄 Document Generation</h3>
                    <p>Generate tailored CVs and cover letters for each application.</p>
                </div>
                <div class="feature">
                    <h3>🔍 ATS Analysis</h3>
                    <p>Analyze documents for ATS compatibility and keyword optimization.</p>
                </div>
            </div>

            <div class="api-section">
                <h2>API Endpoints</h2>
                <p>This deployment exposes a RESTful API for the Co-Apply functionality:</p>
                
                <div class="endpoint">
                    <strong>GET /api/health</strong>
                    <p>Health check endpoint</p>
                    <code>curl https://your-app.vercel.app/api/health</code>
                </div>
                
                <div class="endpoint">
                    <strong>GET /api/version</strong>
                    <p>Get application version</p>
                    <code>curl https://your-app.vercel.app/api/version</code>
                </div>
                
                <div class="endpoint">
                    <strong>POST /api/parse-job</strong>
                    <p>Parse a job description</p>
                    <code>curl -X POST -H "Content-Type: application/json" -d '{"description":"..."}' https://your-app.vercel.app/api/parse-job</code>
                </div>
                
                <div class="endpoint">
                    <strong>POST /api/analyze-match</strong>
                    <p>Analyze achievement-job matches</p>
                    <code>curl -X POST -H "Content-Type: application/json" -d '{"achievements":[],"job":{}}' https://your-app.vercel.app/api/analyze-match</code>
                </div>
            </div>

            <h2>Getting Started</h2>
            <p>To use Co-Apply locally as a CLI tool:</p>
            <ol style="margin-left: 40px; margin-top: 10px;">
                <li>Clone the repository: <code>git clone https://github.com/stewartDMS/Co-Apply.git</code></li>
                <li>Install dependencies: <code>pip install -e .</code></li>
                <li>Initialize your profile: <code>co-apply profile init</code></li>
                <li>Start adding achievements and applying to jobs!</li>
            </ol>

            <div style="margin-top: 30px;">
                <a href="https://github.com/stewartDMS/Co-Apply" class="button">View on GitHub</a>
                <a href="/api/health" class="button">Check API Health</a>
            </div>
        </div>

        <footer>
            <p>Co-Apply v0.1.0 | MIT License | Built with ❤️ for job seekers</p>
        </footer>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Landing page"""
    return render_template_string(LANDING_PAGE)

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Co-Apply API',
        'version': '0.1.0'
    })

@app.route('/api/version')
def version():
    """Get version information"""
    return jsonify({
        'version': '0.1.0',
        'name': 'co-apply',
        'python_version': sys.version
    })

@app.route('/api/parse-job', methods=['POST'])
def parse_job():
    """Parse a job description"""
    try:
        from co_apply.core.job_parser import JobParser
        
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({'error': 'Job description is required'}), 400
        
        parser = JobParser()
        job = parser.parse(
            data['description'],
            job_id=data.get('job_id', 'temp-job'),
            title=data.get('title', 'Unknown Position'),
            company=data.get('company', 'Unknown Company')
        )
        
        return jsonify({
            'success': True,
            'job': {
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'skills_required': job.skills_required,
                'skills_preferred': job.skills_preferred,
                'responsibilities': job.responsibilities,
                'requirements': job.requirements
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-match', methods=['POST'])
def analyze_match():
    """Analyze achievement-job matching"""
    try:
        from co_apply.analysis.matcher import AchievementJobMatcher
        from co_apply.core.achievement_library import Achievement
        from co_apply.core.job_parser import JobDescription
        
        data = request.get_json()
        if not data or 'achievements' not in data or 'job' not in data:
            return jsonify({'error': 'Achievements and job data are required'}), 400
        
        # Create achievement objects
        achievements = []
        for ach_data in data['achievements']:
            ach = Achievement(
                id=ach_data.get('id', ''),
                title=ach_data.get('title', ''),
                description=ach_data.get('description', ''),
                category=ach_data.get('category', 'technical'),
                skills=ach_data.get('skills', []),
                keywords=ach_data.get('keywords', []),
                impact=ach_data.get('impact'),
                metrics=ach_data.get('metrics'),
                date=ach_data.get('date')
            )
            achievements.append(ach)
        
        # Create job object
        job_data = data['job']
        job = JobDescription(
            id=job_data.get('job_id', 'temp'),
            title=job_data.get('title', ''),
            company=job_data.get('company', ''),
            description=job_data.get('description', ''),
            skills_required=job_data.get('skills_required', []),
            skills_preferred=job_data.get('skills_preferred', []),
            responsibilities=job_data.get('responsibilities', []),
            requirements=job_data.get('requirements', [])
        )
        
        # Match
        matcher = AchievementJobMatcher()
        matches = matcher.match_achievements_to_job(achievements, job)
        
        # Format results
        results = []
        for match in matches:
            results.append({
                'achievement_id': match.achievement.id,
                'achievement_title': match.achievement.title,
                'relevance_score': match.relevance_score,
                'matched_skills': match.matched_skills,
                'reasons': match.reasons
            })
        
        return jsonify({
            'success': True,
            'matches': results,
            'total_matches': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ats-analyze', methods=['POST'])
def ats_analyze():
    """Analyze ATS compatibility"""
    try:
        from co_apply.analysis.ats_analyzer import ATSAnalyzer
        
        data = request.get_json()
        if not data or 'document' not in data or 'keywords' not in data:
            return jsonify({'error': 'Document and keywords are required'}), 400
        
        analyzer = ATSAnalyzer()
        result = analyzer.analyze(
            data['keywords'],
            data['document'],
            data.get('required_skills', [])
        )
        
        return jsonify({
            'success': True,
            'match_score': result.match_score,
            'matched_keywords': result.matched_keywords,
            'missing_keywords': result.missing_keywords,
            'recommendations': result.recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel serverless function handler
def handler(request):
    """Vercel serverless function handler"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()
