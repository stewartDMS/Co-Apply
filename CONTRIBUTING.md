# Contributing to Co-Apply

Thank you for your interest in contributing to Co-Apply! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Co-Apply.git`
3. Create a virtual environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Install in development mode: `pip install -e .`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest tests/`
4. Commit your changes: `git commit -m "Description of changes"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage

## Vercel Deployment (For Maintainers)

This repository is configured to deploy to an existing Vercel project named 'co-apply'.

### Deploying Changes

If you're a maintainer with access to the main Vercel project:

1. **Link to the project** (first time only):
   ```bash
   vercel link
   ```
   Select the existing 'co-apply' project when prompted.

2. **Deploy your changes**:
   ```bash
   vercel --prod
   ```

### Project Configuration

- The `.vercel/project.json` file contains placeholder IDs for documentation
- When you run `vercel link` or deploy, Vercel CLI will update this file with actual project IDs
- The `.vercel` directory is git-ignored (except for the placeholder files)
- **DO NOT commit** real project IDs to the repository

### For Contributors Without Deployment Access

If you're contributing but don't have access to the main Vercel deployment:
- You can test your API changes locally using `python api/index.py`
- For testing on Vercel, create your own project deployment
- The maintainers will handle deploying your merged changes to the main project

## Areas for Contribution

- **Document Formats**: Add support for LaTeX, PDF, DOCX
- **ATS Analysis**: Enhance keyword analysis algorithms
- **Matching Engine**: Improve relevance scoring
- **Templates**: Create more CV and cover letter templates
- **UI/GUI**: Build a graphical interface
- **Job Board Integration**: Connect with popular job boards
- **Documentation**: Improve docs and add tutorials

## Questions?

Open an issue or start a discussion on GitHub!
