# Co-Apply Usage Guide

## Quick Start Guide

### 1. Installation

```bash
# Clone repository
git clone https://github.com/stewartDMS/Co-Apply.git
cd Co-Apply

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# (Optional) Install Playwright for autofill
playwright install chromium
```

### 2. First Time Setup

#### Initialize Your Profile

```bash
co-apply profile init
```

You'll be prompted for:
- Full Name
- Email
- Phone
- Location (optional)

#### Add Your Achievements

You can add achievements one by one:

```bash
co-apply achievement add
```

Or use the sample data to get started:

```bash
cp data/examples/sample_achievement.json data/user_achievements.json
```

### 3. Basic Workflow

#### Step 1: Parse a Job Description

Save the job description to a text file (e.g., `job.txt`), then:

```bash
co-apply job parse job.txt \
  --job-id "company-position-2024" \
  --title "Software Engineer" \
  --company "TechCorp"
```

This creates a structured JSON file in `data/jobs/`.

#### Step 2: Analyze Match Quality

```bash
co-apply analyze match company-position-2024
```

This shows:
- Relevance scores for each achievement
- Skills coverage percentage
- Recommendations

#### Step 3: Generate Tailored Documents

Generate a CV:
```bash
co-apply generate cv company-position-2024 -o my_cv.md
```

Generate a cover letter:
```bash
co-apply generate cover-letter company-position-2024 -o cover_letter.txt --tone professional
```

Cover letter tones:
- `professional` (default): Formal and balanced
- `enthusiastic`: More energetic and excited
- `formal`: Very formal and traditional

#### Step 4: Check ATS Compatibility

```bash
co-apply analyze ats my_cv.md company-position-2024
```

This provides:
- ATS match score (0-100%)
- Matched keywords
- Missing keywords
- Recommendations for improvement

#### Step 5: Track Your Application

```bash
# Add to tracker
co-apply track add company-position-2024 --status submitted

# List all applications
co-apply track list

# View statistics
co-apply track stats
```

Application statuses:
- `draft`: Working on application
- `submitted`: Application submitted
- `interviewing`: Interview scheduled/completed
- `offered`: Offer received
- `rejected`: Application rejected
- `accepted`: Offer accepted
- `withdrawn`: Application withdrawn

## Advanced Features

### Custom Achievements Format

Your `user_achievements.json` should follow this structure:

```json
{
  "profile": {
    "name": "Your Name",
    "email": "email@example.com",
    "phone": "+1234567890",
    "location": "City, State",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "github": "https://github.com/yourusername",
    "website": "https://yoursite.com",
    "summary": "Brief professional summary"
  },
  "achievements": [
    {
      "id": "unique_id",
      "title": "Achievement Title",
      "description": "Detailed description of what you did",
      "category": "technical",
      "skills": ["Python", "AWS", "Docker"],
      "keywords": ["development", "cloud", "automation"],
      "impact": "What was the impact/outcome",
      "metrics": "Quantifiable metrics (e.g., '50% performance improvement')",
      "date": "2023-01 to 2023-06",
      "context": "Additional context (optional)"
    }
  ]
}
```

Categories:
- `technical`: Technical projects and implementations
- `leadership`: Leadership and management achievements
- `project`: Project delivery and management
- `certification`: Certifications and training

### Multiple CV Versions

Generate different versions programmatically:

```python
from co_apply.generators.cv_generator import CVGenerator
from co_apply.core.achievement_library import AchievementLibrary
from co_apply.core.job_parser import JobParser
from co_apply.analysis.matcher import AchievementJobMatcher

library = AchievementLibrary()
parser = JobParser()
job = parser.load_job("data/jobs/job-001.json")
matcher = AchievementJobMatcher()
matches = matcher.match_achievements_to_job(library.achievements, job)

generator = CVGenerator()
versions = generator.generate_multiple_versions(library.profile, matches, job)

# versions['concise'] - 1-page version
# versions['standard'] - Standard 2-page version
# versions['detailed'] - Detailed version with all achievements
```

### Diff Comparison

Compare two versions of your CV:

```python
from co_apply.analysis.diff_reviewer import DiffReviewer

reviewer = DiffReviewer()

with open('cv_v1.md', 'r') as f:
    original = f.read()
    
with open('cv_v2.md', 'r') as f:
    updated = f.read()

result = reviewer.compare(original, updated)

print(f"Similarity: {result.similarity_score}%")
print(f"Changes: {result.statistics['total_changes']}")

# Generate report
summary = reviewer.generate_change_summary(result)
print(summary)

# Save HTML diff for visual comparison
reviewer.save_html_diff(result, 'diff_report.html')
```

### Autofill (Advanced)

Use Playwright to automate form filling:

```python
from co_apply.autofill.form_filler import autofill_application

profile_data = {
    'first_name': 'Jane',
    'last_name': 'Doe',
    'email': 'jane@example.com',
    'phone': '555-1234',
    'linkedin': 'https://linkedin.com/in/janedoe',
    'github': 'https://github.com/janedoe'
}

file_uploads = {
    'resume': '/absolute/path/to/cv.pdf',
    'cover_letter': '/absolute/path/to/cover.pdf'
}

result = autofill_application(
    url='https://company.com/careers/apply/12345',
    profile_data=profile_data,
    file_uploads=file_uploads,
    headless=False  # Show browser for verification
)

if result['success']:
    print(f"Filled {result['fields_filled']} fields")
    print(f"Screenshot: {result['screenshot']}")
else:
    print(f"Error: {result['error']}")
```

**Safety Notes:**
- Always review before submitting
- `auto_submit=False` by default
- Take screenshots for verification
- Test on dummy applications first

## Tips & Best Practices

### Writing Good Achievements

1. **Use the STAR method**: Situation, Task, Action, Result
2. **Include metrics**: Quantify impact whenever possible
3. **Be specific**: Use concrete examples
4. **Include skills**: List all relevant technical skills used
5. **Add keywords**: Include industry-standard terms

Example:
```
Title: "Optimized Database Performance"
Description: "Identified performance bottlenecks in PostgreSQL database supporting 1M+ users. Redesigned indexes, optimized queries, and implemented connection pooling."
Impact: "Reduced API response time by 60% and database CPU usage by 40%"
Metrics: "Improved average query time from 800ms to 320ms"
Skills: ["PostgreSQL", "SQL", "Performance Optimization", "Database Design"]
Keywords: ["database", "optimization", "performance", "sql", "postgresql"]
```

### Maximizing ATS Score

1. **Use standard section headers**: "Experience", "Education", "Skills"
2. **Include exact keywords**: Copy key terms from job description
3. **Avoid fancy formatting**: Keep it simple and readable
4. **Use standard fonts**: Arial, Calibri, Times New Roman
5. **Save as .txt or .docx**: For best ATS compatibility
6. **Repeat important keywords**: Naturally throughout the document

### Managing Multiple Applications

Use descriptive job IDs:
```bash
# Good
co-apply job parse job.txt --job-id "google-swe-backend-2024"
co-apply job parse job.txt --job-id "amazon-sde2-seattle-2024"

# Less helpful
co-apply job parse job.txt --job-id "job1"
co-apply job parse job.txt --job-id "job2"
```

### Iterative Improvement

1. Generate initial version
2. Check ATS score
3. Add missing keywords
4. Compare versions using diff
5. Repeat until satisfied

```bash
# Initial generation
co-apply generate cv job-001 -o cv_v1.md
co-apply analyze ats cv_v1.md job-001

# After manual improvements
co-apply analyze ats cv_v2.md job-001

# Compare
python -c "
from co_apply.analysis.diff_reviewer import DiffReviewer
reviewer = DiffReviewer()
with open('cv_v1.md') as f1, open('cv_v2.md') as f2:
    result = reviewer.compare(f1.read(), f2.read())
    print(reviewer.generate_change_summary(result))
"
```

## Troubleshooting

### "No relevant achievements found"

The matching threshold (default 0.3) might be too high. Lower it programmatically:

```python
from co_apply.analysis.matcher import AchievementJobMatcher

matcher = AchievementJobMatcher()
matches = matcher.match_achievements_to_job(achievements, job)
relevant = matcher.filter_by_threshold(matches, threshold=0.2)
```

### ATS Score Too Low

1. Add more keywords from job description to your achievements
2. Ensure skills match exactly (case-insensitive)
3. Include company-specific terms and technologies
4. Use industry-standard terminology

### Playwright Issues

```bash
# Reinstall Playwright browsers
playwright install --force chromium

# Check browser installation
playwright install --help
```

## Examples

See the `data/examples/` directory for:
- `sample_achievement.json`: Example achievement library
- `sample_job_description.txt`: Example job description

Run the demo:
```bash
python demo.py
```

## Getting Help

- GitHub Issues: Report bugs or request features
- Documentation: Check README.md and this guide
- Examples: See example data in `data/examples/`

## Next Steps

1. Add all your achievements to the library
2. Parse job descriptions as you find them
3. Generate tailored documents for each application
4. Track your applications
5. Iterate based on ATS analysis

Good luck with your job search! 🎯
