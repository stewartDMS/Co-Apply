"""
CV/Resume Generator
Generates tailored CVs based on job descriptions and achievements
"""

import os
from typing import List, Dict, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from ..core.achievement_library import Achievement, CandidateProfile
from ..core.job_parser import JobDescription
from ..analysis.matcher import MatchResult


class CVGenerator:
    """Generates tailored CVs in various formats"""

    def __init__(self, template_dir: str = "data/templates"):
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, profile: CandidateProfile, matches: List[MatchResult],
                job: JobDescription, format: str = 'markdown',
                include_all_skills: bool = False) -> str:
        """
        Generate a tailored CV
        
        Args:
            profile: Candidate profile
            matches: Matched achievements (sorted by relevance)
            job: Target job description
            format: Output format (markdown, html, latex)
            include_all_skills: Include all skills or only job-relevant ones
            
        Returns:
            Generated CV content as string
        """
        # Prepare data for template
        data = self._prepare_cv_data(profile, matches, job, include_all_skills)
        
        # Select template
        template_name = f"cv_{format}.j2"
        
        try:
            template = self.env.get_template(template_name)
            return template.render(**data)
        except Exception as e:
            # Fallback to markdown if template not found
            return self._generate_markdown_cv(data)

    def _prepare_cv_data(self, profile: CandidateProfile, matches: List[MatchResult],
                        job: JobDescription, include_all_skills: bool) -> Dict:
        """Prepare data structure for CV template"""
        
        # Extract unique skills from matched achievements
        all_skills = set()
        job_skills = set([s.lower() for s in (job.skills_required or []) + (job.skills_preferred or [])])
        
        for match in matches:
            all_skills.update(match.achievement.skills)
        
        # Filter skills if needed
        if not include_all_skills:
            relevant_skills = [
                skill for skill in all_skills 
                if skill.lower() in job_skills
            ]
        else:
            relevant_skills = list(all_skills)
        
        # Group achievements by category
        grouped_achievements = {}
        for match in matches:
            category = match.achievement.category
            if category not in grouped_achievements:
                grouped_achievements[category] = []
            grouped_achievements[category].append(match)
        
        # Generate summary (if not already in profile)
        summary = profile.summary or self._generate_summary(profile, job, matches)
        
        return {
            'profile': profile,
            'summary': summary,
            'skills': sorted(relevant_skills),
            'achievements': matches,
            'grouped_achievements': grouped_achievements,
            'job_title': job.title,
            'job_company': job.company,
            'generated_date': datetime.now().strftime("%Y-%m-%d"),
        }

    def _generate_summary(self, profile: CandidateProfile, job: JobDescription,
                         matches: List[MatchResult]) -> str:
        """Generate a tailored professional summary"""
        # Get top skills from matches
        top_skills = []
        for match in matches[:5]:
            top_skills.extend(match.matched_skills[:2])
        top_skills = list(set(top_skills))[:5]
        
        # Basic template for summary
        summary_parts = []
        
        if job.title:
            summary_parts.append(f"Experienced professional seeking {job.title} position")
        
        if top_skills:
            skills_str = ", ".join(top_skills[:3])
            summary_parts.append(f"with expertise in {skills_str}")
        
        if matches:
            summary_parts.append(f"Proven track record in {matches[0].achievement.category} achievements")
        
        return ". ".join(summary_parts) + "."

    def _generate_markdown_cv(self, data: Dict) -> str:
        """Generate a markdown CV as fallback"""
        profile = data['profile']
        
        lines = []
        
        # Header
        lines.append(f"# {profile.name}")
        lines.append("")
        
        # Contact info
        contact = []
        if profile.email:
            contact.append(f"📧 {profile.email}")
        if profile.phone:
            contact.append(f"📱 {profile.phone}")
        if profile.location:
            contact.append(f"📍 {profile.location}")
        
        lines.append(" | ".join(contact))
        lines.append("")
        
        # Links
        links = []
        if profile.linkedin:
            links.append(f"[LinkedIn]({profile.linkedin})")
        if profile.github:
            links.append(f"[GitHub]({profile.github})")
        if profile.website:
            links.append(f"[Website]({profile.website})")
        
        if links:
            lines.append(" | ".join(links))
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        # Summary
        if data.get('summary'):
            lines.append("## Professional Summary")
            lines.append("")
            lines.append(data['summary'])
            lines.append("")
        
        # Skills
        if data.get('skills'):
            lines.append("## Skills")
            lines.append("")
            skills_formatted = " • ".join(data['skills'])
            lines.append(skills_formatted)
            lines.append("")
        
        # Achievements/Experience
        if data.get('achievements'):
            lines.append("## Professional Experience & Achievements")
            lines.append("")
            
            for match in data['achievements']:
                achievement = match.achievement
                lines.append(f"### {achievement.title}")
                
                if achievement.date:
                    lines.append(f"*{achievement.date}*")
                
                lines.append("")
                lines.append(achievement.description)
                lines.append("")
                
                if achievement.impact:
                    lines.append(f"**Impact:** {achievement.impact}")
                    lines.append("")
                
                if achievement.metrics:
                    lines.append(f"**Metrics:** {achievement.metrics}")
                    lines.append("")
                
                if match.matched_skills:
                    lines.append(f"**Key Skills:** {', '.join(match.matched_skills[:5])}")
                    lines.append("")
        
        # Footer
        lines.append("---")
        lines.append(f"*Tailored for {data.get('job_title', 'Position')} at {data.get('job_company', 'Company')}*")
        lines.append(f"*Generated on {data['generated_date']}*")
        
        return "\n".join(lines)

    def save_cv(self, content: str, filepath: str, format: str = 'markdown'):
        """Save CV to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_multiple_versions(self, profile: CandidateProfile,
                                   matches: List[MatchResult],
                                   job: JobDescription) -> Dict[str, str]:
        """Generate multiple versions of CV (with different levels of detail)"""
        versions = {}
        
        # Concise version (top 5 achievements)
        versions['concise'] = self.generate(
            profile, matches[:5], job, format='markdown'
        )
        
        # Standard version (top 10 achievements)
        versions['standard'] = self.generate(
            profile, matches[:10], job, format='markdown'
        )
        
        # Detailed version (all relevant achievements)
        versions['detailed'] = self.generate(
            profile, matches, job, format='markdown', include_all_skills=True
        )
        
        return versions

    def optimize_for_ats(self, cv_content: str, job: JobDescription) -> str:
        """Optimize CV content for ATS"""
        # Add job-specific keywords strategically
        optimized = cv_content
        
        # Ensure job title appears
        if job.title and job.title not in cv_content:
            # Add to summary section
            optimized = optimized.replace(
                "## Professional Summary",
                f"## Professional Summary\n\nTarget Role: {job.title}"
            )
        
        return optimized
