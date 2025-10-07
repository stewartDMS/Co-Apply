"""
Job Description Parser
Extracts key information from job descriptions
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class JobDescription:
    """Represents a parsed job description"""
    id: str
    title: str
    company: str
    location: Optional[str] = None
    description: str = ""
    requirements: List[str] = None
    responsibilities: List[str] = None
    skills_required: List[str] = None
    skills_preferred: List[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    url: Optional[str] = None
    posted_date: Optional[str] = None
    raw_text: str = ""

    def __post_init__(self):
        if self.requirements is None:
            self.requirements = []
        if self.responsibilities is None:
            self.responsibilities = []
        if self.skills_required is None:
            self.skills_required = []
        if self.skills_preferred is None:
            self.skills_preferred = []

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'JobDescription':
        return cls(**data)


class JobParser:
    """Parses job descriptions and extracts structured information"""

    # Common section headers
    SECTION_PATTERNS = {
        'requirements': r'(?i)(requirements?|qualifications?|what (we\'re|you\'ll need)|you (have|bring))',
        'responsibilities': r'(?i)(responsibilities|duties|what you\'ll do|role description|the role)',
        'skills': r'(?i)(skills?|technical skills?|required skills?|must have)',
        'preferred': r'(?i)(preferred|nice to have|bonus|plus|desirable)',
        'education': r'(?i)(education|degree|qualification)',
        'experience': r'(?i)(\d+\+?\s*years?|experience level)',
    }

    # Common skill patterns
    SKILL_INDICATORS = [
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',  # Capitalized words/phrases
        r'\b([A-Z]{2,}(?:\.[A-Z]+)*)\b',  # Acronyms
    ]

    def __init__(self):
        self.common_skills = self._load_common_skills()

    def _load_common_skills(self) -> List[str]:
        """Load common technical and soft skills"""
        return [
            # Programming languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
            'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB',
            # Frameworks
            'React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring', 'Node.js',
            'Express', 'FastAPI', 'Rails', 'Laravel', '.NET', 'ASP.NET',
            # Databases
            'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Cassandra',
            'Oracle', 'DynamoDB', 'Elasticsearch',
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab',
            'GitHub Actions', 'Terraform', 'Ansible', 'CI/CD',
            # Data Science & ML
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Spark',
            'Hadoop', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            # Soft skills
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Agile', 'Scrum', 'Project Management',
        ]

    def parse(self, text: str, job_id: str, title: str = "", company: str = "") -> JobDescription:
        """Parse job description text into structured format"""
        job = JobDescription(
            id=job_id,
            title=title,
            company=company,
            raw_text=text
        )

        # Extract sections
        job.description = self._extract_description(text)
        job.requirements = self._extract_section(text, 'requirements')
        job.responsibilities = self._extract_section(text, 'responsibilities')
        
        # Extract skills
        skills = self._extract_skills(text)
        job.skills_required = skills['required']
        job.skills_preferred = skills['preferred']

        # Extract other fields
        job.education = self._extract_education(text)
        job.experience = self._extract_experience(text)
        job.salary_range = self._extract_salary(text)
        job.job_type = self._extract_job_type(text)

        return job

    def _extract_description(self, text: str) -> str:
        """Extract general job description"""
        # Take first paragraph or few sentences
        lines = text.split('\n')
        description = []
        for line in lines[:10]:  # First 10 lines
            line = line.strip()
            if line and len(line) > 30:
                description.append(line)
            if len(description) >= 3:
                break
        return ' '.join(description)

    def _extract_section(self, text: str, section_type: str) -> List[str]:
        """Extract bullet points from a specific section"""
        pattern = self.SECTION_PATTERNS.get(section_type, '')
        if not pattern:
            return []

        # Find section start
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if not match:
            return []

        # Extract text after section header
        start_pos = match.end()
        remaining_text = text[start_pos:]

        # Find next section or end
        next_section = None
        for other_pattern in self.SECTION_PATTERNS.values():
            next_match = re.search(other_pattern, remaining_text, re.IGNORECASE)
            if next_match and (next_section is None or next_match.start() < next_section):
                next_section = next_match.start()

        section_text = remaining_text[:next_section] if next_section else remaining_text

        # Extract bullet points
        bullets = []
        bullet_pattern = r'(?:^|\n)\s*(?:[-•*]|\d+\.)\s+(.+?)(?=\n|$)'
        for match in re.finditer(bullet_pattern, section_text, re.MULTILINE):
            bullet = match.group(1).strip()
            if len(bullet) > 10:  # Filter out very short items
                bullets.append(bullet)

        # If no bullets found, try to split by newlines
        if not bullets:
            lines = section_text.split('\n')
            bullets = [line.strip() for line in lines if len(line.strip()) > 20]

        return bullets[:15]  # Limit to 15 items

    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract required and preferred skills"""
        skills = {'required': [], 'preferred': []}

        # Look for skills section
        skills_section = self._extract_section(text, 'skills')
        preferred_section = self._extract_section(text, 'preferred')

        # Extract from sections
        all_text = text.lower()
        for skill in self.common_skills:
            skill_lower = skill.lower()
            if skill_lower in all_text:
                # Check if in preferred section
                if any(skill_lower in p.lower() for p in preferred_section):
                    if skill not in skills['preferred']:
                        skills['preferred'].append(skill)
                else:
                    if skill not in skills['required']:
                        skills['required'].append(skill)

        return skills

    def _extract_education(self, text: str) -> Optional[str]:
        """Extract education requirements"""
        patterns = [
            r"(?i)(Bachelor'?s?|Master'?s?|PhD|Doctorate|Associate'?s?|MBA)(?:\s+degree)?\s+in\s+([A-Za-z\s,]+)",
            r"(?i)(Bachelor'?s?|Master'?s?|PhD|Doctorate|Associate'?s?|MBA)(?:\s+degree)?",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).strip()
        return None

    def _extract_experience(self, text: str) -> Optional[str]:
        """Extract experience requirements"""
        pattern = r'(\d+\+?)\s*(?:to|-|\s+)?\s*(\d+)?\s*(?:\+)?\s*years?(?:\s+of)?\s+(?:experience|exp\.?)?'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return None

    def _extract_salary(self, text: str) -> Optional[str]:
        """Extract salary range if mentioned"""
        patterns = [
            r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|-)\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'\$\s*(\d{1,3}(?:,\d{3})*(?:k|K)?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).strip()
        return None

    def _extract_job_type(self, text: str) -> Optional[str]:
        """Extract job type (full-time, part-time, etc.)"""
        job_types = ['full-time', 'part-time', 'contract', 'temporary', 'internship', 'remote', 'hybrid']
        text_lower = text.lower()
        
        for job_type in job_types:
            if job_type in text_lower:
                return job_type
        return None

    def save_job(self, job: JobDescription, filepath: str):
        """Save parsed job description to file"""
        with open(filepath, 'w') as f:
            json.dump(job.to_dict(), f, indent=2)

    def load_job(self, filepath: str) -> JobDescription:
        """Load job description from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return JobDescription.from_dict(data)
