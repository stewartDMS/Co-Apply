"""
Document Diff Reviewer
Compare different versions of CVs and cover letters
"""

import difflib
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class DiffResult:
    """Result of comparing two documents"""
    similarity_score: float  # 0-100
    added_lines: List[str]
    removed_lines: List[str]
    modified_lines: List[Tuple[str, str]]  # (old, new)
    unified_diff: str
    html_diff: str
    statistics: Dict[str, int]


class DiffReviewer:
    """Review and compare different versions of documents"""

    def __init__(self):
        pass

    def compare(self, original: str, updated: str, 
                context_lines: int = 3) -> DiffResult:
        """
        Compare two versions of a document
        
        Args:
            original: Original document text
            updated: Updated document text
            context_lines: Number of context lines in diff
            
        Returns:
            DiffResult with comparison details
        """
        # Split into lines
        original_lines = original.splitlines(keepends=True)
        updated_lines = updated.splitlines(keepends=True)
        
        # Calculate similarity
        similarity = self._calculate_similarity(original, updated)
        
        # Get diff
        diff = list(difflib.unified_diff(
            original_lines, updated_lines,
            fromfile='original', tofile='updated',
            lineterm='', n=context_lines
        ))
        
        # Parse changes
        added, removed, modified = self._parse_changes(original_lines, updated_lines)
        
        # Generate HTML diff
        html_diff = self._generate_html_diff(original_lines, updated_lines)
        
        # Calculate statistics
        stats = {
            'lines_added': len(added),
            'lines_removed': len(removed),
            'lines_modified': len(modified),
            'total_changes': len(added) + len(removed) + len(modified),
        }
        
        return DiffResult(
            similarity_score=similarity,
            added_lines=added,
            removed_lines=removed,
            modified_lines=modified,
            unified_diff='\n'.join(diff),
            html_diff=html_diff,
            statistics=stats
        )

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (0-100)"""
        matcher = difflib.SequenceMatcher(None, text1, text2)
        return round(matcher.ratio() * 100, 2)

    def _parse_changes(self, original_lines: List[str], 
                      updated_lines: List[str]) -> Tuple[List[str], List[str], List[Tuple[str, str]]]:
        """Parse line-by-line changes"""
        added = []
        removed = []
        modified = []
        
        # Use SequenceMatcher to find changes
        matcher = difflib.SequenceMatcher(None, original_lines, updated_lines)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'insert':
                added.extend([line.rstrip() for line in updated_lines[j1:j2]])
            elif tag == 'delete':
                removed.extend([line.rstrip() for line in original_lines[i1:i2]])
            elif tag == 'replace':
                # Lines that changed
                for orig, upd in zip(original_lines[i1:i2], updated_lines[j1:j2]):
                    modified.append((orig.rstrip(), upd.rstrip()))
                # Handle unequal lengths
                if i2 - i1 < j2 - j1:
                    added.extend([line.rstrip() for line in updated_lines[j1 + (i2-i1):j2]])
                elif i2 - i1 > j2 - j1:
                    removed.extend([line.rstrip() for line in original_lines[i1 + (j2-j1):i2]])
        
        return added, removed, modified

    def _generate_html_diff(self, original_lines: List[str], 
                           updated_lines: List[str]) -> str:
        """Generate HTML diff for visualization"""
        differ = difflib.HtmlDiff(wrapcolumn=80)
        html = differ.make_file(
            original_lines, updated_lines,
            fromdesc='Original', todesc='Updated',
            context=True, numlines=3
        )
        return html

    def highlight_keyword_changes(self, original: str, updated: str, 
                                 keywords: List[str]) -> Dict[str, List[str]]:
        """Highlight changes related to specific keywords"""
        keywords_lower = [k.lower() for k in keywords]
        
        added_keywords = []
        removed_keywords = []
        
        original_lower = original.lower()
        updated_lower = updated.lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            was_present = keyword_lower in original_lower
            is_present = keyword_lower in updated_lower
            
            if is_present and not was_present:
                added_keywords.append(keyword)
            elif was_present and not is_present:
                removed_keywords.append(keyword)
        
        return {
            'keywords_added': added_keywords,
            'keywords_removed': removed_keywords,
            'keyword_improvement': len(added_keywords) - len(removed_keywords)
        }

    def generate_change_summary(self, diff_result: DiffResult) -> str:
        """Generate a human-readable summary of changes"""
        stats = diff_result.statistics
        
        summary_lines = []
        summary_lines.append("📊 Document Comparison Summary")
        summary_lines.append("=" * 50)
        summary_lines.append(f"Similarity Score: {diff_result.similarity_score}%")
        summary_lines.append("")
        
        summary_lines.append("Changes:")
        summary_lines.append(f"  ✅ Lines Added: {stats['lines_added']}")
        summary_lines.append(f"  ❌ Lines Removed: {stats['lines_removed']}")
        summary_lines.append(f"  ✏️  Lines Modified: {stats['lines_modified']}")
        summary_lines.append(f"  📝 Total Changes: {stats['total_changes']}")
        summary_lines.append("")
        
        if diff_result.added_lines:
            summary_lines.append("New Content (sample):")
            for line in diff_result.added_lines[:3]:
                summary_lines.append(f"  + {line[:80]}")
            if len(diff_result.added_lines) > 3:
                summary_lines.append(f"  ... and {len(diff_result.added_lines) - 3} more")
            summary_lines.append("")
        
        if diff_result.removed_lines:
            summary_lines.append("Removed Content (sample):")
            for line in diff_result.removed_lines[:3]:
                summary_lines.append(f"  - {line[:80]}")
            if len(diff_result.removed_lines) > 3:
                summary_lines.append(f"  ... and {len(diff_result.removed_lines) - 3} more")
        
        return "\n".join(summary_lines)

    def compare_multiple_versions(self, versions: Dict[str, str]) -> Dict[str, DiffResult]:
        """Compare multiple versions against each other"""
        results = {}
        version_names = list(versions.keys())
        
        for i in range(len(version_names) - 1):
            v1 = version_names[i]
            v2 = version_names[i + 1]
            
            key = f"{v1}_vs_{v2}"
            results[key] = self.compare(versions[v1], versions[v2])
        
        return results

    def get_word_count_change(self, original: str, updated: str) -> Dict[str, int]:
        """Get word count statistics"""
        original_words = len(original.split())
        updated_words = len(updated.split())
        
        return {
            'original_word_count': original_words,
            'updated_word_count': updated_words,
            'word_count_change': updated_words - original_words,
            'change_percentage': round((updated_words - original_words) / max(original_words, 1) * 100, 2)
        }

    def identify_significant_changes(self, diff_result: DiffResult, 
                                    threshold: int = 10) -> List[str]:
        """Identify significant changes (lines longer than threshold characters)"""
        significant = []
        
        for line in diff_result.added_lines:
            if len(line) > threshold:
                significant.append(f"Added: {line[:100]}...")
        
        for line in diff_result.removed_lines:
            if len(line) > threshold:
                significant.append(f"Removed: {line[:100]}...")
        
        return significant

    def save_diff_report(self, diff_result: DiffResult, filepath: str):
        """Save diff report to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        report = []
        report.append(self.generate_change_summary(diff_result))
        report.append("\n\n")
        report.append("=" * 50)
        report.append("\nUnified Diff:\n")
        report.append("=" * 50)
        report.append("\n")
        report.append(diff_result.unified_diff)
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(report))

    def save_html_diff(self, diff_result: DiffResult, filepath: str):
        """Save HTML diff to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(diff_result.html_diff)
