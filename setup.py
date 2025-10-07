from setuptools import setup, find_packages

setup(
    name="co-apply",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml>=6.0",
        "jinja2>=3.1.0",
        "python-docx>=1.1.0",
        "pdfkit>=1.0.0",
        "markdown>=3.5.0",
        "pandas>=2.0.0",
        "nltk>=3.8.0",
        "playwright>=1.40.0",
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "llm": ["llama-cpp-python>=0.2.0"],
    },
    entry_points={
        "console_scripts": [
            "co-apply=co_apply.cli:main",
        ],
    },
    python_requires=">=3.8",
)
