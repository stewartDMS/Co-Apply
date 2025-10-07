"""
Command Line Interface for Co-Apply
"""

import click
import os
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from datetime import datetime

from .core.achievement_library import AchievementLibrary, Achievement, CandidateProfile
from .core.job_parser import JobParser, JobDescription
from .core.tracker import ApplicationTracker, Application
from .analysis.matcher import AchievementJobMatcher
from .analysis.ats_analyzer import ATSAnalyzer
from .analysis.diff_reviewer import DiffReviewer
from .generators.cv_generator import CVGenerator
from .generators.cover_letter_generator import CoverLetterGenerator

console = Console()


@click.group()
@click.version_option(version='0.1.0')
def main():
    """Co-Apply: Job Application Copilot"""
    pass


@main.group()
def profile():
    """Manage your candidate profile"""
    pass


@profile.command('init')
@click.option('--name', prompt='Full Name', help='Your full name')
@click.option('--email', prompt='Email', help='Your email address')
@click.option('--phone', prompt='Phone', help='Your phone number')
@click.option('--location', prompt='Location', default='', help='Your location')
def init_profile(name, email, phone, location):
    """Initialize your candidate profile"""
    library = AchievementLibrary()
    
    profile = CandidateProfile(
        name=name,
        email=email,
        phone=phone,
        location=location or None
    )
    
    library.set_profile(profile)
    console.print("[green]✓[/green] Profile created successfully!")
    console.print(f"Profile saved to: {library.data_file}")


@profile.command('show')
def show_profile():
    """Display your current profile"""
    library = AchievementLibrary()
    
    if not library.profile:
        console.print("[red]✗[/red] No profile found. Run 'co-apply profile init' first.")
        return
    
    profile = library.profile
    
    table = Table(title="Your Profile")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Name", profile.name)
    table.add_row("Email", profile.email or "")
    table.add_row("Phone", profile.phone or "")
    table.add_row("Location", profile.location or "")
    table.add_row("LinkedIn", profile.linkedin or "")
    table.add_row("GitHub", profile.github or "")
    
    console.print(table)


@main.group()
def achievement():
    """Manage your achievements"""
    pass


@achievement.command('add')
@click.option('--title', prompt='Achievement Title', help='Title of the achievement')
@click.option('--description', prompt='Description', help='Detailed description')
@click.option('--category', prompt='Category', 
              type=click.Choice(['technical', 'leadership', 'project', 'certification']),
              help='Achievement category')
@click.option('--skills', prompt='Skills (comma-separated)', help='Related skills')
@click.option('--keywords', prompt='Keywords (comma-separated)', help='Keywords for matching')
def add_achievement(title, description, category, skills, keywords):
    """Add a new achievement to your library"""
    library = AchievementLibrary()
    
    achievement = Achievement(
        id=f"ach_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title=title,
        description=description,
        category=category,
        skills=[s.strip() for s in skills.split(',')],
        keywords=[k.strip() for k in keywords.split(',')],
    )
    
    library.add_achievement(achievement)
    console.print(f"[green]✓[/green] Achievement added: {title}")


@achievement.command('list')
def list_achievements():
    """List all achievements"""
    library = AchievementLibrary()
    
    if not library.achievements:
        console.print("[yellow]No achievements found. Add some with 'co-apply achievement add'[/yellow]")
        return
    
    table = Table(title=f"Your Achievements ({len(library.achievements)})")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="cyan")
    table.add_column("Category", style="green")
    table.add_column("Skills", style="yellow")
    
    for ach in library.achievements:
        table.add_row(
            ach.id[:15] + "...",
            ach.title[:40],
            ach.category,
            ", ".join(ach.skills[:3])
        )
    
    console.print(table)


@main.group()
def job():
    """Manage job descriptions"""
    pass


@job.command('parse')
@click.argument('job_file', type=click.Path(exists=True))
@click.option('--job-id', prompt='Job ID', help='Unique identifier for this job')
@click.option('--title', prompt='Job Title', help='Job title')
@click.option('--company', prompt='Company', help='Company name')
def parse_job(job_file, job_id, title, company):
    """Parse a job description from a text file"""
    with open(job_file, 'r') as f:
        job_text = f.read()
    
    parser = JobParser()
    job = parser.parse(job_text, job_id, title, company)
    
    # Save parsed job
    output_path = f"data/jobs/{job_id}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    parser.save_job(job, output_path)
    
    console.print(f"[green]✓[/green] Job parsed and saved to: {output_path}")
    
    # Display summary
    console.print("\n[bold]Job Summary:[/bold]")
    console.print(f"Title: {job.title}")
    console.print(f"Company: {job.company}")
    console.print(f"Required Skills: {', '.join(job.skills_required[:5])}")
    console.print(f"Preferred Skills: {', '.join(job.skills_preferred[:3])}")


@main.group()
def generate():
    """Generate CVs and cover letters"""
    pass


@generate.command('cv')
@click.argument('job_id')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', default='markdown', type=click.Choice(['markdown', 'html']),
              help='Output format')
def generate_cv(job_id, output, format):
    """Generate a tailored CV for a specific job"""
    # Load data
    library = AchievementLibrary()
    if not library.profile:
        console.print("[red]✗[/red] No profile found. Run 'co-apply profile init' first.")
        return
    
    # Load job
    job_file = f"data/jobs/{job_id}.json"
    if not os.path.exists(job_file):
        console.print(f"[red]✗[/red] Job not found: {job_file}")
        return
    
    parser = JobParser()
    job = parser.load_job(job_file)
    
    # Match achievements
    matcher = AchievementJobMatcher()
    matches = matcher.match_achievements_to_job(library.achievements, job)
    
    # Filter relevant matches
    relevant_matches = matcher.filter_by_threshold(matches, threshold=0.3)
    
    if not relevant_matches:
        console.print("[yellow]⚠[/yellow] No relevant achievements found for this job.")
        console.print("Consider adding more achievements or lowering the threshold.")
        return
    
    # Generate CV
    with console.status("[bold green]Generating CV..."):
        generator = CVGenerator()
        cv_content = generator.generate(library.profile, relevant_matches, job, format=format)
    
    # Save CV
    if not output:
        output = f"data/generated/{job_id}_cv.{format}"
    
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generator.save_cv(cv_content, output, format)
    
    console.print(f"[green]✓[/green] CV generated: {output}")
    console.print(f"[cyan]Matched {len(relevant_matches)} relevant achievements[/cyan]")


@generate.command('cover-letter')
@click.argument('job_id')
@click.option('--output', '-o', help='Output file path')
@click.option('--tone', default='professional', 
              type=click.Choice(['professional', 'enthusiastic', 'formal']),
              help='Tone of the cover letter')
def generate_cover_letter(job_id, output, tone):
    """Generate a tailored cover letter for a specific job"""
    # Load data
    library = AchievementLibrary()
    if not library.profile:
        console.print("[red]✗[/red] No profile found. Run 'co-apply profile init' first.")
        return
    
    # Load job
    job_file = f"data/jobs/{job_id}.json"
    if not os.path.exists(job_file):
        console.print(f"[red]✗[/red] Job not found: {job_file}")
        return
    
    parser = JobParser()
    job = parser.load_job(job_file)
    
    # Match achievements
    matcher = AchievementJobMatcher()
    matches = matcher.match_achievements_to_job(library.achievements, job)
    relevant_matches = matcher.filter_by_threshold(matches, threshold=0.3)
    
    if not relevant_matches:
        console.print("[yellow]⚠[/yellow] No relevant achievements found for this job.")
        return
    
    # Generate cover letter
    with console.status("[bold green]Generating cover letter..."):
        generator = CoverLetterGenerator()
        letter_content = generator.generate(library.profile, relevant_matches, job, tone=tone)
    
    # Save letter
    if not output:
        output = f"data/generated/{job_id}_cover_letter.txt"
    
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generator.save_letter(letter_content, output)
    
    console.print(f"[green]✓[/green] Cover letter generated: {output}")


@main.group()
def analyze():
    """Analyze job matches and ATS compatibility"""
    pass


@analyze.command('match')
@click.argument('job_id')
def analyze_match(job_id):
    """Analyze how well your achievements match a job"""
    library = AchievementLibrary()
    
    # Load job
    job_file = f"data/jobs/{job_id}.json"
    if not os.path.exists(job_file):
        console.print(f"[red]✗[/red] Job not found: {job_file}")
        return
    
    parser = JobParser()
    job = parser.load_job(job_file)
    
    # Match achievements
    matcher = AchievementJobMatcher()
    matches = matcher.match_achievements_to_job(library.achievements, job)
    
    # Display results
    table = Table(title=f"Achievement Match Analysis: {job.title}")
    table.add_column("Achievement", style="cyan")
    table.add_column("Score", style="green")
    table.add_column("Matched Skills", style="yellow")
    
    for match in matches[:10]:
        score_pct = f"{match.relevance_score * 100:.1f}%"
        skills = ", ".join(match.matched_skills[:3])
        table.add_row(match.achievement.title[:40], score_pct, skills)
    
    console.print(table)
    
    # Coverage report
    coverage = matcher.get_coverage_report(matches, job)
    console.print("\n[bold]Coverage Report:[/bold]")
    console.print(f"Required Skills Coverage: {coverage['required_skills_coverage']:.1f}%")
    console.print(f"Preferred Skills Coverage: {coverage['preferred_skills_coverage']:.1f}%")
    console.print(f"Recommendation: {coverage['recommendation']}")


@analyze.command('ats')
@click.argument('document', type=click.Path(exists=True))
@click.argument('job_id')
def analyze_ats(document, job_id):
    """Analyze document for ATS compatibility"""
    # Load document
    with open(document, 'r') as f:
        doc_content = f.read()
    
    # Load job
    job_file = f"data/jobs/{job_id}.json"
    if not os.path.exists(job_file):
        console.print(f"[red]✗[/red] Job not found: {job_file}")
        return
    
    parser = JobParser()
    job = parser.load_job(job_file)
    
    # Analyze
    analyzer = ATSAnalyzer()
    
    # Get all keywords from job
    all_keywords = (job.skills_required or []) + (job.skills_preferred or [])
    
    result = analyzer.analyze(all_keywords, doc_content, job.skills_required)
    
    # Display results
    console.print(Panel(f"[bold]ATS Score: {result.match_score:.1f}%[/bold]", 
                       style="green" if result.match_score >= 70 else "yellow"))
    
    console.print(f"\n[green]✓ Matched Keywords ({len(result.matched_keywords)}):[/green]")
    console.print(", ".join(result.matched_keywords[:15]))
    
    if result.missing_keywords:
        console.print(f"\n[yellow]⚠ Missing Keywords ({len(result.missing_keywords)}):[/yellow]")
        console.print(", ".join(result.missing_keywords[:15]))
    
    console.print("\n[bold]Recommendations:[/bold]")
    for rec in result.recommendations:
        console.print(f"  • {rec}")


@main.group()
def track():
    """Track job applications"""
    pass


@track.command('add')
@click.argument('job_id')
@click.option('--status', default='draft', help='Application status')
def track_add(job_id, status):
    """Add a job application to tracker"""
    # Load job
    job_file = f"data/jobs/{job_id}.json"
    if not os.path.exists(job_file):
        console.print(f"[red]✗[/red] Job not found: {job_file}")
        return
    
    parser = JobParser()
    job = parser.load_job(job_file)
    
    tracker = ApplicationTracker()
    
    application = Application(
        id=None,
        job_id=job_id,
        job_title=job.title,
        company=job.company,
        status=status,
        applied_date=None,
        last_updated=datetime.now().isoformat(),
    )
    
    app_id = tracker.create_application(application)
    console.print(f"[green]✓[/green] Application tracked (ID: {app_id})")


@track.command('list')
@click.option('--status', help='Filter by status')
def track_list(status):
    """List tracked applications"""
    tracker = ApplicationTracker()
    applications = tracker.list_applications(status=status)
    
    if not applications:
        console.print("[yellow]No applications found.[/yellow]")
        return
    
    table = Table(title="Job Applications")
    table.add_column("ID", style="dim")
    table.add_column("Company", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Last Updated", style="dim")
    
    for app in applications:
        table.add_row(
            str(app.id),
            app.company[:20],
            app.job_title[:30],
            app.status,
            app.last_updated[:10]
        )
    
    console.print(table)


@track.command('stats')
def track_stats():
    """Show application statistics"""
    tracker = ApplicationTracker()
    stats = tracker.get_statistics()
    
    console.print(Panel(f"[bold]Total Applications: {stats['total_applications']}[/bold]"))
    
    console.print("\n[bold]By Status:[/bold]")
    for status, count in stats['by_status'].items():
        console.print(f"  {status}: {count}")
    
    if stats['avg_match_score']:
        console.print(f"\n[bold]Avg Match Score:[/bold] {stats['avg_match_score']:.1f}%")
    if stats['avg_ats_score']:
        console.print(f"[bold]Avg ATS Score:[/bold] {stats['avg_ats_score']:.1f}%")
    
    console.print(f"\n[bold]Last 30 Days:[/bold] {stats['applications_last_30_days']} applications")


if __name__ == '__main__':
    main()
