# Co-Apply Quick Reference Card

## Installation

```bash
git clone https://github.com/stewartDMS/Co-Apply.git && cd Co-Apply
python -m venv venv && source venv/bin/activate
pip install -e .
```

## Essential Commands

### Setup
```bash
co-apply profile init                    # Initialize profile
co-apply achievement add                 # Add achievement
co-apply profile show                    # View profile
co-apply achievement list                # List achievements
```

### Workflow
```bash
# 1. Parse job
co-apply job parse job.txt --job-id "JOB_ID" --title "TITLE" --company "COMPANY"

# 2. Analyze match
co-apply analyze match JOB_ID

# 3. Generate documents
co-apply generate cv JOB_ID -o cv.md
co-apply generate cover-letter JOB_ID -o cover.txt --tone professional

# 4. Check ATS
co-apply analyze ats cv.md JOB_ID

# 5. Track
co-apply track add JOB_ID --status submitted
```

### Tracking
```bash
co-apply track list                      # List applications
co-apply track list --status submitted   # Filter by status
co-apply track stats                     # View statistics
```

## File Structure

```
data/
├── user_achievements.json      # Your achievements
├── jobs/JOB_ID.json           # Parsed jobs
├── generated/cv_JOB_ID.md     # Generated CVs
└── applications.db            # Tracking database
```

## Achievement Format

```json
{
  "id": "unique_id",
  "title": "What you did",
  "description": "Detailed description",
  "category": "technical|leadership|project|certification",
  "skills": ["Skill1", "Skill2"],
  "keywords": ["keyword1", "keyword2"],
  "impact": "The outcome/impact",
  "metrics": "Quantifiable results",
  "date": "YYYY-MM to YYYY-MM"
}
```

## Categories

- `technical`: Technical projects
- `leadership`: Leadership achievements
- `project`: Project delivery
- `certification`: Certifications/training

## Tones (Cover Letter)

- `professional`: Formal and balanced (default)
- `enthusiastic`: Energetic and excited
- `formal`: Very formal and traditional

## Application Statuses

- `draft`: Working on it
- `submitted`: Application sent
- `interviewing`: Interview stage
- `offered`: Offer received
- `rejected`: Application rejected
- `accepted`: Offer accepted
- `withdrawn`: Application withdrawn

## Tips

1. **Add metrics**: Quantify everything possible
2. **Use keywords**: Match job description terms
3. **Be specific**: Concrete examples work best
4. **Update regularly**: Keep achievements current
5. **Test ATS**: Aim for 70%+ match score

## Common Issues

### No relevant achievements found
Lower the threshold (default 0.3):
```python
matches = matcher.filter_by_threshold(matches, threshold=0.2)
```

### Low ATS score
- Add missing keywords from job description
- Use exact terminology from job posting
- Include technical terms and skills

### Playwright issues
```bash
playwright install chromium
playwright install --force
```

## Python API

```python
from co_apply.core.achievement_library import AchievementLibrary
from co_apply.core.job_parser import JobParser
from co_apply.analysis.matcher import AchievementJobMatcher
from co_apply.generators.cv_generator import CVGenerator

# Load data
library = AchievementLibrary()
parser = JobParser()
job = parser.load_job("data/jobs/job-001.json")

# Match and generate
matcher = AchievementJobMatcher()
matches = matcher.match_achievements_to_job(library.achievements, job)

generator = CVGenerator()
cv = generator.generate(library.profile, matches, job)
```

## Example: Complete Workflow

```bash
# Setup (once)
cp data/examples/sample_achievement.json data/user_achievements.json

# For each job
co-apply job parse job.txt --job-id "google-swe-2024" --title "SWE" --company "Google"
co-apply analyze match google-swe-2024
co-apply generate cv google-swe-2024 -o cv_google.md
co-apply generate cover-letter google-swe-2024 -o cover_google.txt
co-apply analyze ats cv_google.md google-swe-2024
co-apply track add google-swe-2024 --status submitted
```

## Resources

- Full docs: `README.md`
- Usage guide: `USAGE_GUIDE.md`
- Architecture: `ARCHITECTURE.md`
- Examples: `data/examples/`
- Demo: `python demo.py`

## Help

```bash
co-apply --help                    # General help
co-apply COMMAND --help            # Command-specific help
```

## Version

```bash
co-apply --version                 # Show version
```

---

**Remember**: Privacy first! All data stays on your machine. 🔒
