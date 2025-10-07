"""
ATS (Applicant Tracking System) Keyword Analyzer
Analyzes job descriptions and documents for ATS compatibility
"""

from typing import List, Dict, Set, Tuple
from collections import Counter
import re
from dataclasses import dataclass


@dataclass
class ATSAnalysisResult:
    """Results of ATS analysis"""
    match_score: float  # 0-100
    matched_keywords: List[str]
    missing_keywords: List[str]
    keyword_frequency: Dict[str, int]
    recommendations: List[str]
    skill_coverage: Dict[str, bool]  # skill -> whether it's covered


class ATSAnalyzer:
    """Analyzes documents for ATS compatibility and keyword matching"""

    # Common ATS-unfriendly elements
    ATS_UNFRIENDLY_PATTERNS = [
        r'[^\x00-\x7F]+',  # Non-ASCII characters
        r'\t',  # Tabs
    ]

    # Stop words to filter out
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    }

    def __init__(self):
        pass

    def analyze(self, job_keywords: List[str], document_text: str, 
                job_skills: List[str] = None) -> ATSAnalysisResult:
        """
        Analyze how well a document matches job requirements
        
        Args:
            job_keywords: Keywords from job description
            document_text: CV or cover letter text
            job_skills: Required skills from job description
            
        Returns:
            ATSAnalysisResult with match score and recommendations
        """
        # Normalize inputs
        job_keywords_lower = [k.lower().strip() for k in job_keywords]
        document_lower = document_text.lower()
        
        # Extract keywords from document
        document_keywords = self._extract_keywords(document_text)
        document_keywords_lower = [k.lower() for k in document_keywords]

        # Find matches
        matched = []
        missing = []
        keyword_freq = {}

        for keyword in job_keywords:
            keyword_lower = keyword.lower()
            # Check for exact match or partial match
            if keyword_lower in document_lower:
                matched.append(keyword)
                # Count frequency
                keyword_freq[keyword] = document_lower.count(keyword_lower)
            else:
                missing.append(keyword)

        # Calculate match score
        if job_keywords:
            match_score = (len(matched) / len(job_keywords)) * 100
        else:
            match_score = 0

        # Skill coverage
        skill_coverage = {}
        if job_skills:
            for skill in job_skills:
                skill_lower = skill.lower()
                skill_coverage[skill] = skill_lower in document_lower

        # Generate recommendations
        recommendations = self._generate_recommendations(
            match_score, matched, missing, keyword_freq, skill_coverage
        )

        return ATSAnalysisResult(
            match_score=round(match_score, 2),
            matched_keywords=matched,
            missing_keywords=missing,
            keyword_frequency=keyword_freq,
            recommendations=recommendations,
            skill_coverage=skill_coverage
        )

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential keywords from text"""
        # Split into words
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]*\b', text)
        
        # Filter stop words and short words
        keywords = [
            word for word in words 
            if len(word) > 2 and word.lower() not in self.STOP_WORDS
        ]
        
        # Get most common
        counter = Counter(keywords)
        return [word for word, count in counter.most_common(100)]

    def _generate_recommendations(self, score: float, matched: List[str], 
                                 missing: List[str], freq: Dict[str, int],
                                 skill_coverage: Dict[str, bool]) -> List[str]:
        """Generate recommendations to improve ATS score"""
        recommendations = []

        if score < 50:
            recommendations.append(
                "⚠️ Low match score. Consider adding more relevant keywords from the job description."
            )
        elif score < 70:
            recommendations.append(
                "⚡ Moderate match. Adding missing keywords could improve your chances."
            )
        else:
            recommendations.append(
                "✅ Good keyword match! Your document aligns well with the job requirements."
            )

        # Missing critical keywords
        if missing:
            top_missing = missing[:5]
            recommendations.append(
                f"📝 Missing important keywords: {', '.join(top_missing)}"
            )

        # Keyword frequency
        low_freq_keywords = [k for k, v in freq.items() if v == 1]
        if len(low_freq_keywords) > 3:
            recommendations.append(
                "💡 Consider mentioning matched keywords more than once to emphasize expertise."
            )

        # Skill coverage
        if skill_coverage:
            missing_skills = [s for s, covered in skill_coverage.items() if not covered]
            if missing_skills:
                recommendations.append(
                    f"🎯 Missing required skills: {', '.join(missing_skills[:3])}"
                )

        # General ATS tips
        recommendations.append(
            "📄 Use standard section headings (Experience, Education, Skills) for better ATS parsing."
        )
        recommendations.append(
            "🔤 Use standard fonts and avoid tables, text boxes, and images for ATS compatibility."
        )

        return recommendations

    def check_ats_friendly_format(self, text: str) -> Dict[str, any]:
        """Check if document format is ATS-friendly"""
        issues = []
        
        # Check for non-ASCII characters
        if re.search(r'[^\x00-\x7F]', text):
            issues.append("Contains non-ASCII characters (consider using standard characters)")
        
        # Check for excessive special characters
        special_char_count = len(re.findall(r'[^a-zA-Z0-9\s\.,;:\-\(\)]', text))
        if special_char_count > 50:
            issues.append("High number of special characters detected")
        
        # Check for tabs
        if '\t' in text:
            issues.append("Contains tab characters (use spaces instead)")

        # Check for common section headers
        standard_sections = ['experience', 'education', 'skills', 'summary']
        found_sections = []
        text_lower = text.lower()
        for section in standard_sections:
            if section in text_lower:
                found_sections.append(section)

        return {
            'is_ats_friendly': len(issues) == 0,
            'issues': issues,
            'found_standard_sections': found_sections,
            'missing_standard_sections': [s for s in standard_sections if s not in found_sections]
        }

    def suggest_keyword_placement(self, missing_keywords: List[str], 
                                  document_sections: Dict[str, str]) -> Dict[str, List[str]]:
        """Suggest where to place missing keywords in the document"""
        suggestions = {}
        
        for keyword in missing_keywords:
            keyword_lower = keyword.lower()
            best_sections = []
            
            # Determine best section based on keyword type
            if any(tech in keyword_lower for tech in ['python', 'java', 'sql', 'aws', 'docker']):
                best_sections.append('Skills')
                best_sections.append('Experience')
            elif any(soft in keyword_lower for soft in ['leadership', 'communication', 'team']):
                best_sections.append('Summary')
                best_sections.append('Experience')
            elif any(edu in keyword_lower for edu in ['degree', 'bachelor', 'master', 'certification']):
                best_sections.append('Education')
            else:
                best_sections.append('Experience')
            
            suggestions[keyword] = best_sections
        
        return suggestions

    def compare_versions(self, original_text: str, updated_text: str, 
                        job_keywords: List[str]) -> Dict[str, any]:
        """Compare two versions of a document for keyword improvements"""
        original_analysis = self.analyze(job_keywords, original_text)
        updated_analysis = self.analyze(job_keywords, updated_text)
        
        score_improvement = updated_analysis.match_score - original_analysis.match_score
        new_keywords_added = set(updated_analysis.matched_keywords) - set(original_analysis.matched_keywords)
        keywords_removed = set(original_analysis.matched_keywords) - set(updated_analysis.matched_keywords)
        
        return {
            'original_score': original_analysis.match_score,
            'updated_score': updated_analysis.match_score,
            'score_improvement': round(score_improvement, 2),
            'new_keywords_added': list(new_keywords_added),
            'keywords_removed': list(keywords_removed),
            'recommendation': 'Improved' if score_improvement > 0 else 'Needs work'
        }
