#!/usr/bin/env python3
"""
Demo script to showcase Co-Apply functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from co_apply.core.achievement_library import AchievementLibrary
from co_apply.core.job_parser import JobParser
from co_apply.analysis.matcher import AchievementJobMatcher
from co_apply.analysis.ats_analyzer import ATSAnalyzer
from co_apply.generators.cv_generator import CVGenerator
from co_apply.generators.cover_letter_generator import CoverLetterGenerator
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print(Panel("[bold cyan]Co-Apply Demo - Job Application Copilot[/bold cyan]"))
    
    # Load achievement library
    console.print("\n[bold]Step 1:[/bold] Loading achievement library...")
    library = AchievementLibrary("data/user_achievements.json")
    console.print(f"✓ Loaded profile: {library.profile.name}")
    console.print(f"✓ Loaded {len(library.achievements)} achievements")
    
    # Load job description
    console.print("\n[bold]Step 2:[/bold] Loading job description...")
    parser = JobParser()
    job = parser.load_job("data/jobs/backend-001.json")
    console.print(f"✓ Job: {job.title} at {job.company}")
    console.print(f"✓ Required skills: {', '.join(job.skills_required[:5])}...")
    
    # Match achievements to job
    console.print("\n[bold]Step 3:[/bold] Matching achievements to job requirements...")
    matcher = AchievementJobMatcher()
    matches = matcher.match_achievements_to_job(library.achievements, job)
    
    # Use lower threshold for demo
    relevant_matches = [m for m in matches if m.relevance_score >= 0.15]
    
    console.print(f"✓ Found {len(relevant_matches)} relevant achievements")
    for match in relevant_matches[:3]:
        console.print(f"  • {match.achievement.title}: {match.relevance_score*100:.1f}% match")
    
    # Generate CV
    console.print("\n[bold]Step 4:[/bold] Generating tailored CV...")
    cv_generator = CVGenerator("data/templates")
    cv_content = cv_generator.generate(library.profile, relevant_matches, job, format='markdown')
    
    output_path = "data/generated/demo_cv.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv_generator.save_cv(cv_content, output_path)
    console.print(f"✓ CV generated: {output_path}")
    
    # Generate cover letter
    console.print("\n[bold]Step 5:[/bold] Generating cover letter...")
    letter_generator = CoverLetterGenerator("data/templates")
    letter_content = letter_generator.generate(
        library.profile, relevant_matches, job, tone='professional'
    )
    
    letter_path = "data/generated/demo_cover_letter.txt"
    letter_generator.save_letter(letter_content, letter_path)
    console.print(f"✓ Cover letter generated: {letter_path}")
    
    # ATS Analysis
    console.print("\n[bold]Step 6:[/bold] Analyzing ATS compatibility...")
    analyzer = ATSAnalyzer()
    all_keywords = job.skills_required + job.skills_preferred
    ats_result = analyzer.analyze(all_keywords, cv_content, job.skills_required)
    
    console.print(f"✓ ATS Match Score: {ats_result.match_score:.1f}%")
    console.print(f"✓ Matched Keywords: {len(ats_result.matched_keywords)}")
    console.print(f"✓ Missing Keywords: {len(ats_result.missing_keywords)}")
    
    # Show CV preview
    console.print("\n[bold]Generated CV Preview:[/bold]")
    lines = cv_content.split('\n')[:25]
    console.print('\n'.join(lines))
    console.print("\n... (truncated)")
    
    console.print("\n[bold green]✓ Demo completed successfully![/bold green]")
    console.print("\nGenerated files:")
    console.print(f"  • {output_path}")
    console.print(f"  • {letter_path}")

if __name__ == '__main__':
    main()
