# Co-Apply Architecture

## System Overview

Co-Apply is a modular job application copilot designed with privacy and minimal API dependencies in mind. All processing happens locally, with optional LLM integration.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Interface                            │
│                      (co_apply.cli)                             │
└────────────────────────┬───────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
┌────────▼──────────┐          ┌────────▼──────────┐
│   Core Modules    │          │  Analysis Modules  │
│                   │          │                    │
│ • Achievement     │          │ • ATS Analyzer     │
│   Library         │          │ • Matcher Engine   │
│ • Job Parser      │          │ • Diff Reviewer    │
│ • Tracker (SQLite)│          │                    │
└────────┬──────────┘          └────────┬───────────┘
         │                               │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │                               │
┌────────▼──────────┐          ┌────────▼──────────┐
│    Generators     │          │   Autofill        │
│                   │          │                    │
│ • CV Generator    │          │ • Form Filler     │
│ • Cover Letter    │          │   (Playwright)    │
│   Generator       │          │                    │
│ • Templates       │          │                    │
│   (Jinja2)        │          │                    │
└───────────────────┘          └────────────────────┘
```

## Component Details

### Core Modules (`src/co_apply/core/`)

#### 1. Achievement Library (`achievement_library.py`)
- **Purpose**: Manage candidate's achievements, skills, and profile
- **Storage**: JSON file (local)
- **Features**:
  - CRUD operations for achievements
  - Search by keywords and categories
  - Profile management
  - Skill extraction

#### 2. Job Parser (`job_parser.py`)
- **Purpose**: Extract structured data from job descriptions
- **Input**: Plain text job description
- **Output**: Structured JobDescription object
- **Extraction**:
  - Requirements and responsibilities
  - Required/preferred skills
  - Education, experience, salary
  - Job type and location

#### 3. Application Tracker (`tracker.py`)
- **Purpose**: Track application status and history
- **Storage**: SQLite database
- **Features**:
  - Application CRUD operations
  - Event logging
  - Statistics and reporting
  - Status management

### Analysis Modules (`src/co_apply/analysis/`)

#### 1. ATS Analyzer (`ats_analyzer.py`)
- **Purpose**: Analyze ATS compatibility and keyword matching
- **Features**:
  - Keyword frequency analysis
  - Match score calculation (0-100%)
  - Format compatibility checks
  - Recommendations generation

#### 2. Matcher Engine (`matcher.py`)
- **Purpose**: Match achievements to job requirements
- **Algorithm**:
  - Skill matching (required: 40%, preferred: 20%)
  - Keyword matching (30%)
  - Category relevance (10%)
  - Relevance score: 0-1 scale

#### 3. Diff Reviewer (`diff_reviewer.py`)
- **Purpose**: Compare document versions
- **Features**:
  - Line-by-line comparison
  - Similarity scoring
  - Keyword change tracking
  - HTML diff generation

### Generators (`src/co_apply/generators/`)

#### 1. CV Generator (`cv_generator.py`)
- **Purpose**: Generate tailored CVs
- **Input**: Profile + Matched Achievements + Job
- **Output**: Formatted CV (Markdown, HTML)
- **Features**:
  - Template-based generation (Jinja2)
  - Skill filtering
  - Multiple versions (concise, standard, detailed)
  - ATS optimization

#### 2. Cover Letter Generator (`cover_letter_generator.py`)
- **Purpose**: Generate personalized cover letters
- **Input**: Profile + Top Achievements + Job
- **Output**: Cover letter text
- **Features**:
  - Multiple tones (professional, enthusiastic, formal)
  - Length control (short, medium, long)
  - Achievement highlighting
  - Template support

### Autofill (`src/co_apply/autofill/`)

#### Form Filler (`form_filler.py`)
- **Purpose**: Automate application form filling
- **Technology**: Playwright (browser automation)
- **Features**:
  - Field detection and mapping
  - Profile data autofill
  - File upload handling
  - Screenshot capture
  - State saving/restoration

## Data Flow

### 1. Application Generation Flow

```
Job Description (text)
        │
        ▼
   Job Parser
        │
        ▼
Job Description (structured)
        │
        ├──────────┐
        │          │
        ▼          ▼
Achievement    Matcher Engine
Library            │
        │          ▼
        │    Match Results
        │       (scored)
        │          │
        └────┬─────┘
             │
             ▼
    Document Generators
             │
        ┌────┴────┐
        │         │
        ▼         ▼
       CV    Cover Letter
```

### 2. ATS Analysis Flow

```
Generated CV (text)
        │
        ├─────────────────┐
        │                 │
        ▼                 ▼
Job Keywords      ATS Analyzer
        │                 │
        └────────┬─────────┘
                 │
                 ▼
          ATS Analysis
        (score + recommendations)
```

### 3. Tracking Flow

```
Application Data
        │
        ▼
   Tracker DB
        │
        ├─────┬─────┬─────┐
        │     │     │     │
        ▼     ▼     ▼     ▼
     Create Update List Stats
```

## Storage

### File System Structure

```
data/
├── user_achievements.json    # Achievement library
├── jobs/                     # Parsed job descriptions
│   ├── job-001.json
│   └── job-002.json
├── generated/                # Generated documents
│   ├── cv_job-001.md
│   └── cover_job-001.txt
├── templates/                # Document templates
│   ├── cv_markdown.j2
│   └── cover_letter_professional.j2
└── applications.db           # SQLite database
```

### Database Schema

```sql
-- Applications table
CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    job_id TEXT,
    job_title TEXT,
    company TEXT,
    status TEXT,
    applied_date TEXT,
    last_updated TEXT,
    cv_path TEXT,
    cover_letter_path TEXT,
    match_score REAL,
    ats_score REAL
);

-- Events table
CREATE TABLE application_events (
    id INTEGER PRIMARY KEY,
    application_id INTEGER,
    event_type TEXT,
    event_date TEXT,
    description TEXT,
    FOREIGN KEY (application_id) REFERENCES applications(id)
);
```

## Key Design Decisions

### 1. Local-First Architecture
- **Rationale**: Privacy, offline capability, no API costs
- **Implementation**: File-based storage, local processing
- **Trade-off**: No cloud sync (can be added later)

### 2. Minimal External Dependencies
- **Core**: Only Python standard library + essential packages
- **Optional**: LLM (llama-cpp-python), Playwright
- **Benefit**: Easy installation, lightweight, maintainable

### 3. Modular Design
- **Benefit**: Easy to extend, test, and maintain
- **Flexibility**: Can swap components (e.g., different generators)
- **Testing**: Unit tests per module

### 4. Template-Based Generation
- **Technology**: Jinja2 templates
- **Benefit**: Users can customize output format
- **Flexibility**: Easy to add new formats (LaTeX, DOCX, etc.)

### 5. Rule-Based Matching (No ML Required)
- **Algorithm**: Weighted scoring based on skill/keyword matches
- **Benefit**: Predictable, explainable, fast
- **Future**: Can add ML-based scoring as enhancement

### 6. SQLite for Tracking
- **Rationale**: Lightweight, serverless, built-in Python
- **Benefit**: No database server needed
- **Scalability**: Sufficient for individual use

## Extension Points

### Adding New Document Formats

1. Create template in `data/templates/`:
```jinja2
# cv_latex.j2
\documentclass{article}
\begin{document}
\title{{{ profile.name }}}
...
\end{document}
```

2. Update generator to support new format
3. No other changes needed

### Adding LLM Integration

```python
from llama_cpp import Llama

class EnhancedGenerator(CVGenerator):
    def __init__(self, model_path):
        super().__init__()
        self.llm = Llama(model_path=model_path)
    
    def _generate_summary(self, profile, job, matches):
        prompt = f"Generate professional summary for {job.title}..."
        return self.llm(prompt)
```

### Adding New Analysis Modules

```python
class CustomAnalyzer:
    def analyze(self, document, criteria):
        # Your analysis logic
        return results
```

Register in CLI or use programmatically.

## Performance Considerations

### Typical Operation Times

- Parse job description: < 1 second
- Match achievements: < 1 second
- Generate CV: < 1 second
- ATS analysis: < 1 second
- Full workflow: ~3-5 seconds

### Scalability

- Achievements: Tested up to 100+ (linear performance)
- Jobs: Unlimited (stored as separate files)
- Applications: SQLite handles 100K+ records easily
- Document size: No practical limits

## Security & Privacy

### Data Protection

1. **All data stays local**: No cloud uploads
2. **No external API calls**: Unless explicitly enabled (LLM, autofill)
3. **No tracking**: No analytics or telemetry
4. **Open source**: Transparent code

### Sensitive Data

- Credentials: Never stored or transmitted
- Personal info: Only in local files
- Job data: Can be anonymized if needed

## Future Enhancements

### Planned Features

1. **PDF Export**: Direct PDF generation
2. **Job Board Integration**: Scrape/parse from Indeed, LinkedIn
3. **Email Tracking**: Track email responses
4. **Resume Builder UI**: Web/desktop interface
5. **Team Features**: Share achievement libraries
6. **Analytics**: Success metrics and insights

### Potential Improvements

1. **ML-based matching**: Train model on successful applications
2. **NLP enhancements**: Better keyword extraction
3. **Multi-language support**: i18n for international jobs
4. **Mobile app**: iOS/Android companion
5. **Browser extension**: Quick apply from job sites

## Maintenance

### Dependencies Update

```bash
# Check outdated packages
pip list --outdated

# Update
pip install --upgrade package-name
```

### Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=src/co_apply
```

### Code Quality

```bash
# Format code
black src/

# Lint
pylint src/co_apply/

# Type check
mypy src/co_apply/
```

## Support

- **Documentation**: README.md, USAGE_GUIDE.md
- **Examples**: data/examples/
- **Issues**: GitHub Issues
- **Contributing**: CONTRIBUTING.md
