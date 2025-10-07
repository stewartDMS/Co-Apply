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
