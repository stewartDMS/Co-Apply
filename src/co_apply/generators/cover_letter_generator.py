"""
Cover Letter Generator
Generates tailored cover letters based on job descriptions and achievements
"""

import os
from typing import List, Dict, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from ..core.achievement_library import Achievement, CandidateProfile
from ..core.job_parser import JobDescription
from ..analysis.matcher import MatchResult


class CoverLetterGenerator:
    """Generates tailored cover letters"""

    def __init__(self, template_dir: str = "data/templates"):
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, profile: CandidateProfile, matches: List[MatchResult],
                job: JobDescription, tone: str = 'professional',
                length: str = 'medium') -> str:
        """
        Generate a tailored cover letter
        
        Args:
            profile: Candidate profile
            matches: Matched achievements (sorted by relevance)
            job: Target job description
            tone: Tone of the letter ('professional', 'enthusiastic', 'formal')
            length: Length preference ('short', 'medium', 'long')
            
        Returns:
            Generated cover letter content
        """
        # Prepare data
        data = self._prepare_letter_data(profile, matches, job, tone, length)
        
        # Try to load template
        template_name = f"cover_letter_{tone}.j2"
        
        try:
            template = self.env.get_template(template_name)
            return template.render(**data)
        except:
            # Fallback to generated letter
            return self._generate_letter(data)

    def _prepare_letter_data(self, profile: CandidateProfile, matches: List[MatchResult],
                            job: JobDescription, tone: str, length: str) -> Dict:
        """Prepare data for cover letter generation"""
        
        # Select top achievements based on length
        num_achievements = {'short': 2, 'medium': 3, 'long': 4}.get(length, 3)
        top_matches = matches[:num_achievements]
        
        # Extract key points
        key_skills = []
        for match in top_matches:
            key_skills.extend(match.matched_skills[:2])
        key_skills = list(set(key_skills))[:5]
        
        return {
            'profile': profile,
            'job': job,
            'top_matches': top_matches,
            'key_skills': key_skills,
            'tone': tone,
            'length': length,
            'date': datetime.now().strftime("%B %d, %Y"),
        }

    def _generate_letter(self, data: Dict) -> str:
        """Generate cover letter content"""
        profile = data['profile']
        job = data['job']
        top_matches = data['top_matches']
        key_skills = data['key_skills']
        
        paragraphs = []
        
        # Header
        header = f"{profile.name}\n"
        if profile.email:
            header += f"{profile.email}\n"
        if profile.phone:
            header += f"{profile.phone}\n"
        if profile.location:
            header += f"{profile.location}\n"
        header += f"\n{data['date']}\n\n"
        
        if job.company:
            header += f"Hiring Manager\n{job.company}\n\n"
        
        paragraphs.append(header)
        
        # Opening paragraph
        opening = self._generate_opening(job, data['tone'])
        paragraphs.append(opening)
        paragraphs.append("")
        
        # Body paragraphs - highlight achievements
        for i, match in enumerate(top_matches):
            if i < 2:  # Limit to 2 achievement paragraphs
                body_para = self._generate_achievement_paragraph(match, job)
                paragraphs.append(body_para)
                paragraphs.append("")
        
        # Skills paragraph
        if key_skills:
            skills_para = self._generate_skills_paragraph(key_skills, job)
            paragraphs.append(skills_para)
            paragraphs.append("")
        
        # Closing paragraph
        closing = self._generate_closing(job, data['tone'])
        paragraphs.append(closing)
        paragraphs.append("")
        
        # Signature
        signature = f"Sincerely,\n\n{profile.name}"
        paragraphs.append(signature)
        
        return "\n".join(paragraphs)

    def _generate_opening(self, job: JobDescription, tone: str) -> str:
        """Generate opening paragraph"""
        openings = {
            'professional': (
                f"I am writing to express my strong interest in the {job.title} position at {job.company}. "
                f"With my background and experience, I am confident I can contribute significantly to your team."
            ),
            'enthusiastic': (
                f"I am excited to apply for the {job.title} position at {job.company}! "
                f"This opportunity perfectly aligns with my career goals and expertise, and I am eager to bring my skills to your innovative team."
            ),
            'formal': (
                f"I respectfully submit my application for the {job.title} position at {job.company}. "
                f"My qualifications and professional experience make me a strong candidate for this role."
            ),
        }
        
        return openings.get(tone, openings['professional'])

    def _generate_achievement_paragraph(self, match: MatchResult, job: JobDescription) -> str:
        """Generate paragraph highlighting an achievement"""
        achievement = match.achievement
        
        # Start with the achievement
        paragraph = f"In my previous role, {achievement.description} "
        
        # Add impact if available
        if achievement.impact:
            paragraph += f"{achievement.impact} "
        
        # Add metrics if available
        if achievement.metrics:
            paragraph += f"Specifically, {achievement.metrics}. "
        
        # Connect to job requirements
        if match.matched_skills:
            skills_str = ", ".join(match.matched_skills[:3])
            paragraph += f"This experience demonstrates my proficiency in {skills_str}, "
            paragraph += f"which I understand are key requirements for the {job.title} role."
        
        return paragraph

    def _generate_skills_paragraph(self, skills: List[str], job: JobDescription) -> str:
        """Generate paragraph about skills alignment"""
        skills_str = ", ".join(skills[:-1])
        if len(skills) > 1:
            skills_str += f", and {skills[-1]}"
        else:
            skills_str = skills[0]
        
        paragraph = (
            f"My technical expertise includes {skills_str}, all of which align directly with "
            f"the requirements outlined in your job description. I am committed to staying current "
            f"with industry best practices and continuously expanding my skill set to drive innovation and efficiency."
        )
        
        return paragraph

    def _generate_closing(self, job: JobDescription, tone: str) -> str:
        """Generate closing paragraph"""
        closings = {
            'professional': (
                f"I am enthusiastic about the opportunity to contribute to {job.company} and would welcome "
                f"the chance to discuss how my background and skills would be an asset to your team. "
                f"Thank you for considering my application."
            ),
            'enthusiastic': (
                f"I would be thrilled to join {job.company} and contribute to your continued success! "
                f"I look forward to the opportunity to discuss how I can add value to your team. "
                f"Thank you so much for your consideration!"
            ),
            'formal': (
                f"I appreciate your consideration of my application for the {job.title} position. "
                f"I am available at your convenience for an interview to discuss my qualifications further. "
                f"Thank you for your time and consideration."
            ),
        }
        
        return closings.get(tone, closings['professional'])

    def save_letter(self, content: str, filepath: str):
        """Save cover letter to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_variations(self, profile: CandidateProfile, matches: List[MatchResult],
                           job: JobDescription) -> Dict[str, str]:
        """Generate multiple variations with different tones"""
        variations = {}
        
        for tone in ['professional', 'enthusiastic', 'formal']:
            variations[tone] = self.generate(profile, matches, job, tone=tone)
        
        return variations

    def optimize_for_ats(self, letter_content: str, job: JobDescription) -> str:
        """Optimize cover letter for ATS"""
        # Ensure key job information is mentioned
        optimized = letter_content
        
        # Add job ID if available
        if hasattr(job, 'id') and job.id:
            optimized = f"Re: Job ID {job.id}\n\n" + optimized
        
        return optimized

    def estimate_reading_time(self, content: str) -> int:
        """Estimate reading time in minutes"""
        words = len(content.split())
        # Average reading speed is ~200-250 words per minute
        minutes = words / 225
        return max(1, round(minutes))
