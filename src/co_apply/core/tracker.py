"""
Job Application Tracker
Tracks application status and history
"""

import sqlite3
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import os


@dataclass
class Application:
    """Represents a job application"""
    id: Optional[int]
    job_id: str
    job_title: str
    company: str
    status: str  # 'draft', 'submitted', 'interviewing', 'offered', 'rejected', 'accepted', 'withdrawn'
    applied_date: Optional[str]
    last_updated: str
    cv_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None
    match_score: Optional[float] = None
    ats_score: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ApplicationEvent:
    """Represents an event in the application process"""
    id: Optional[int]
    application_id: int
    event_type: str  # 'applied', 'response', 'interview', 'offer', 'rejection', 'note'
    event_date: str
    description: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ApplicationTracker:
    """Manages job applications and their status"""

    def __init__(self, db_path: str = "data/applications.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the database tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                status TEXT NOT NULL,
                applied_date TEXT,
                last_updated TEXT NOT NULL,
                cv_path TEXT,
                cover_letter_path TEXT,
                job_url TEXT,
                notes TEXT,
                match_score REAL,
                ats_score REAL
            )
        ''')
        
        # Application events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS application_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                event_date TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (application_id) REFERENCES applications (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_application(self, application: Application) -> int:
        """Create a new application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        application.last_updated = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO applications 
            (job_id, job_title, company, status, applied_date, last_updated,
             cv_path, cover_letter_path, job_url, notes, match_score, ats_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            application.job_id, application.job_title, application.company,
            application.status, application.applied_date, application.last_updated,
            application.cv_path, application.cover_letter_path, application.job_url,
            application.notes, application.match_score, application.ats_score
        ))
        
        application_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Add initial event
        self.add_event(application_id, 'created', f"Application created for {application.job_title}")
        
        return application_id

    def update_application(self, application_id: int, updates: Dict):
        """Update an existing application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates['last_updated'] = datetime.now().isoformat()
        
        # Build UPDATE query dynamically
        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [application_id]
        
        cursor.execute(f'''
            UPDATE applications
            SET {set_clause}
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
        
        # Add update event
        if 'status' in updates:
            self.add_event(application_id, 'status_change', f"Status changed to {updates['status']}")

    def get_application(self, application_id: int) -> Optional[Application]:
        """Get application by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM applications WHERE id = ?', (application_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Application(**dict(row))
        return None

    def list_applications(self, status: Optional[str] = None,
                         company: Optional[str] = None,
                         limit: int = 100) -> List[Application]:
        """List applications with optional filters"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM applications WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        if company:
            query += ' AND company LIKE ?'
            params.append(f'%{company}%')
        
        query += ' ORDER BY last_updated DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [Application(**dict(row)) for row in rows]

    def delete_application(self, application_id: int):
        """Delete an application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete events first
        cursor.execute('DELETE FROM application_events WHERE application_id = ?', (application_id,))
        
        # Delete application
        cursor.execute('DELETE FROM applications WHERE id = ?', (application_id,))
        
        conn.commit()
        conn.close()

    def add_event(self, application_id: int, event_type: str, description: str):
        """Add an event to an application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        event_date = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO application_events (application_id, event_type, event_date, description)
            VALUES (?, ?, ?, ?)
        ''', (application_id, event_type, event_date, description))
        
        conn.commit()
        conn.close()

    def get_events(self, application_id: int) -> List[ApplicationEvent]:
        """Get all events for an application"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM application_events 
            WHERE application_id = ?
            ORDER BY event_date DESC
        ''', (application_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [ApplicationEvent(**dict(row)) for row in rows]

    def get_statistics(self) -> Dict[str, any]:
        """Get application statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total applications
        cursor.execute('SELECT COUNT(*) FROM applications')
        total = cursor.fetchone()[0]
        
        # By status
        cursor.execute('SELECT status, COUNT(*) FROM applications GROUP BY status')
        by_status = dict(cursor.fetchall())
        
        # Average match score
        cursor.execute('SELECT AVG(match_score) FROM applications WHERE match_score IS NOT NULL')
        avg_match_score = cursor.fetchone()[0]
        
        # Average ATS score
        cursor.execute('SELECT AVG(ats_score) FROM applications WHERE ats_score IS NOT NULL')
        avg_ats_score = cursor.fetchone()[0]
        
        # Recent applications
        cursor.execute('''
            SELECT COUNT(*) FROM applications 
            WHERE applied_date >= date('now', '-30 days')
        ''')
        recent = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_applications': total,
            'by_status': by_status,
            'avg_match_score': round(avg_match_score, 2) if avg_match_score else None,
            'avg_ats_score': round(avg_ats_score, 2) if avg_ats_score else None,
            'applications_last_30_days': recent,
        }

    def search_applications(self, query: str) -> List[Application]:
        """Search applications by job title or company"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM applications 
            WHERE job_title LIKE ? OR company LIKE ?
            ORDER BY last_updated DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Application(**dict(row)) for row in rows]

    def export_to_json(self, filepath: str):
        """Export all applications to JSON"""
        applications = self.list_applications(limit=10000)
        
        export_data = {
            'applications': [app.to_dict() for app in applications],
            'export_date': datetime.now().isoformat(),
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
