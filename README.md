# Co-Apply 🚀

> Your AI-powered job application copilot

Co-Apply is an intelligent job application assistant that helps you create tailored, ATS-optimized CVs and cover letters by matching your achievements with job requirements. Built with privacy in mind, it runs locally and requires minimal external APIs.

## ✨ Features

- **🎯 Achievement Library**: Maintain a comprehensive library of your professional achievements, skills, and experiences
- **📝 Smart Job Parser**: Automatically extract requirements, skills, and responsibilities from job descriptions
- **🤖 Intelligent Matching**: Match your achievements to job requirements using relevance scoring
- **📄 CV Generation**: Generate tailored, ATS-optimized CVs in multiple formats (Markdown, HTML)
- **✉️ Cover Letter Creation**: Create personalized cover letters with different tones (professional, enthusiastic, formal)
- **🔍 ATS Analysis**: Analyze documents for Applicant Tracking System compatibility with keyword matching
- **📊 Diff Review**: Compare document versions to track improvements
- **📈 Application Tracker**: Track all your job applications with status updates and statistics
- **🖥️ Auto-fill Helper**: Desktop automation using Playwright to fill application forms (optional)
- **🔒 Privacy-First**: All processing happens locally, with optional LLM integration

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/stewartDMS/Co-Apply.git
cd Co-Apply

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# (Optional) Install Playwright browsers for autofill
playwright install chromium
```

### Initialize Your Profile

```bash
# Set up your candidate profile
co-apply profile init

# View your profile
co-apply profile show
```

### Add Your Achievements

```bash
# Add achievements to your library
co-apply achievement add

# List all achievements
co-apply achievement list
```

You can also import the sample data:
```bash
cp data/examples/sample_achievement.json data/user_achievements.json
```

### Parse a Job Description

```bash
# Parse a job description from a text file
co-apply job parse data/examples/sample_job_description.txt \
  --job-id "senior-backend-2024" \
  --title "Senior Software Engineer - Backend" \
  --company "Tech Corp"
```

### Generate Tailored Documents

```bash
# Generate a tailored CV
co-apply generate cv senior-backend-2024 -o my_cv.md

# Generate a cover letter
co-apply generate cover-letter senior-backend-2024 -o my_cover_letter.txt --tone professional
```

### Analyze Match Quality

```bash
# Analyze how well your achievements match the job
co-apply analyze match senior-backend-2024

# Check ATS compatibility
co-apply analyze ats my_cv.md senior-backend-2024
```

### Track Your Applications

```bash
# Add application to tracker
co-apply track add senior-backend-2024 --status submitted

# List all applications
co-apply track list

# View statistics
co-apply track stats
```

## 📖 Documentation

### Project Structure

```
Co-Apply/
├── src/co_apply/
│   ├── core/                    # Core modules
│   │   ├── achievement_library.py  # Achievement management
│   │   ├── job_parser.py          # Job description parsing
│   │   └── tracker.py             # Application tracking
│   ├── analysis/                # Analysis modules
│   │   ├── ats_analyzer.py       # ATS keyword analysis
│   │   ├── matcher.py            # Achievement-job matching
│   │   └── diff_reviewer.py      # Document comparison
│   ├── generators/              # Document generators
│   │   ├── cv_generator.py       # CV generation
│   │   └── cover_letter_generator.py
│   ├── autofill/                # Autofill automation
│   │   └── form_filler.py        # Playwright-based autofill
│   └── cli.py                   # Command-line interface
├── data/
│   ├── templates/               # Document templates
│   ├── examples/                # Sample data
│   ├── jobs/                    # Parsed job descriptions
│   └── generated/               # Generated documents
├── tests/                       # Test suite
└── README.md
```

### Key Concepts

#### Achievement Library
Your professional achievements, skills, and experiences are stored in a structured format. Each achievement includes:
- Title and detailed description
- Category (technical, leadership, project, certification)
- Skills and keywords for matching
- Impact and metrics (quantifiable results)
- Context and dates

#### Job Parsing
The job parser extracts structured information from job descriptions:
- Requirements and responsibilities
- Required and preferred skills
- Education and experience requirements
- Job type, salary range, and location

#### Matching Engine
The matcher scores how well each achievement aligns with job requirements:
- Matches required and preferred skills
- Analyzes keyword overlap
- Considers achievement categories
- Provides relevance scores (0-1)

#### ATS Analysis
The ATS analyzer checks your documents for:
- Keyword match percentage
- Missing important keywords
- Format compatibility issues
- Recommendations for improvement

#### Document Generation
Generate tailored documents using:
- Jinja2 templates for customization
- Automatic skill filtering based on job requirements
- Multiple format support (Markdown, HTML)
- Professional, human-readable output

## 🎯 Use Cases

### Scenario 1: Quick Application
```bash
# Parse job, generate documents, and track in one workflow
co-apply job parse job.txt --job-id "job-001" --title "Developer" --company "TechCo"
co-apply generate cv job-001 -o cv.md
co-apply generate cover-letter job-001 -o cover.txt
co-apply track add job-001 --status draft
```

### Scenario 2: Optimize for ATS
```bash
# Generate CV, analyze, and iterate
co-apply generate cv job-001 -o cv_v1.md
co-apply analyze ats cv_v1.md job-001

# Make improvements and compare
co-apply analyze ats cv_v2.md job-001
```

### Scenario 3: Autofill Application (Advanced)
```python
from co_apply.autofill.form_filler import autofill_application

profile_data = {
    'first_name': 'Jane',
    'last_name': 'Doe',
    'email': 'jane@example.com',
    'phone': '555-1234'
}

file_uploads = {
    'resume': '/path/to/cv.pdf',
    'cover_letter': '/path/to/cover.pdf'
}

result = autofill_application(
    url='https://company.com/apply',
    profile_data=profile_data,
    file_uploads=file_uploads,
    headless=False  # Show browser for verification
)
```

## 🔧 Advanced Features

### Custom Templates
Create custom CV templates in `data/templates/`:
```jinja2
# cv_custom.j2
{{ profile.name }}
{{ profile.email }}

{% for match in achievements %}
- {{ match.achievement.title }}
{% endfor %}
```

### Local LLM Integration (Optional)
For enhanced document generation, integrate a local LLM:
```bash
pip install llama-cpp-python
```

Then configure in your code to enhance summaries and descriptions.

### Database Export
Export your application data:
```python
from co_apply.core.tracker import ApplicationTracker

tracker = ApplicationTracker()
tracker.export_to_json('data/backup/applications.json')
```

## 🛡️ Privacy & Security

- **Local Processing**: All data stays on your machine
- **No Cloud Dependencies**: Works completely offline (except autofill for web forms)
- **Optional LLM**: Use local models if needed
- **Data Control**: Full control over your data with JSON exports

## 🌐 Deployment

Co-Apply can be deployed as a web application with a REST API on Vercel.

> **📌 Important**: This repository is configured to deploy to an existing Vercel project named 'co-apply'. If you're a contributor, use `vercel link` to connect to the existing project. See the [Deployment Guide](DEPLOYMENT.md) for details.

### Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/stewartDMS/Co-Apply)

### For Contributors - Link to Existing Project

If you have access to the main 'co-apply' Vercel project:

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Link to the existing project
cd Co-Apply
vercel link

# Deploy
vercel --prod
```

### For Forks - Create Your Own Deployment

If you're forking this repository for your own use:

1. **Fork this repository** on GitHub
2. **Sign up for [Vercel](https://vercel.com)** (free tier available)
3. **Import your forked repository** in Vercel dashboard
4. **Deploy** - Vercel will automatically detect the configuration

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### API Endpoints

Once deployed, the following endpoints are available:

- `GET /api/health` - Health check
- `GET /api/version` - Get version info
- `POST /api/parse-job` - Parse job descriptions
- `POST /api/analyze-match` - Analyze achievement-job matches
- `POST /api/ats-analyze` - Analyze ATS compatibility

### Testing Your Deployment

```bash
# Test health endpoint
curl https://your-app.vercel.app/api/health

# Test job parsing
curl -X POST https://your-app.vercel.app/api/parse-job \
  -H "Content-Type: application/json" \
  -d '{"description":"Looking for a Python developer...","job_id":"test-001","title":"Python Developer","company":"Test Corp"}'
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete testing instructions and API documentation.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional document formats (LaTeX, PDF)
- More ATS analysis features
- Enhanced matching algorithms
- Integration with job boards
- UI/GUI interface

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- Python 3.8+
- Jinja2 for templating
- Playwright for automation
- Rich for beautiful CLI
- Click for command-line interface

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Check the documentation in `docs/`

---

**Co-Apply** - Making job applications easier, one tailored CV at a time! 🎯