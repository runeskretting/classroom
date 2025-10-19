"""
Database Manager for Python Classroom
Handles SQLite database operations for student progress tracking.
"""

import sqlite3
import json
import os
from datetime import datetime
from contextlib import contextmanager
from typing import Optional, Dict, List, Any


class DatabaseManager:
    """Manages SQLite database for student progress."""

    def __init__(self, db_path='data/classroom.db'):
        self.db_path = db_path
        self.ensure_database_exists()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def ensure_database_exists(self):
        """Create database and tables if they don't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    current_module INTEGER NOT NULL DEFAULT 1,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    started_at TEXT NOT NULL
                )
            ''')

            # Create module_progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS module_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    module_id INTEGER NOT NULL,
                    quiz_passed BOOLEAN NOT NULL DEFAULT 0,
                    project_passed BOOLEAN NOT NULL DEFAULT 0,
                    quiz_score INTEGER NOT NULL DEFAULT 0,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    last_submission TEXT,
                    test_results TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    UNIQUE(student_id, module_id)
                )
            ''')

            # Create indexes for better query performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_student_name
                ON students(name)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_module_progress_student
                ON module_progress(student_id, module_id)
            ''')

    def create_student(self, name: str, current_module: int = 1,
                      started_at: str = None) -> int:
        """
        Create a new student record.
        Returns the student ID.
        """
        if started_at is None:
            started_at = datetime.now().isoformat()

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (name, current_module, completed, started_at)
                VALUES (?, ?, 0, ?)
            ''', (name, current_module, started_at))
            return cursor.lastrowid

    def get_student_by_name(self, name: str) -> Optional[Dict]:
        """Get student record by name."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM students WHERE name = ?
            ''', (name,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def get_student_by_id(self, student_id: int) -> Optional[Dict]:
        """Get student record by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM students WHERE id = ?
            ''', (student_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def get_all_students(self) -> List[Dict]:
        """Get all student records."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM students ORDER BY name
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def update_student(self, name: str, **updates):
        """Update student record."""
        if not updates:
            return

        # Build update query dynamically
        fields = []
        values = []
        for key, value in updates.items():
            if key in ['current_module', 'completed']:
                fields.append(f"{key} = ?")
                values.append(value)

        if not fields:
            return

        values.append(name)
        query = f"UPDATE students SET {', '.join(fields)} WHERE name = ?"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)

    def delete_student(self, name: str) -> bool:
        """Delete student and all associated progress. Returns True if deleted."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE name = ?', (name,))
            return cursor.rowcount > 0

    def get_module_progress(self, student_id: int, module_id: int) -> Optional[Dict]:
        """Get progress for a specific module."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM module_progress
                WHERE student_id = ? AND module_id = ?
            ''', (student_id, module_id))
            row = cursor.fetchone()
            if row:
                data = dict(row)
                # Parse test_results JSON if present
                if data.get('test_results'):
                    try:
                        data['test_results'] = json.loads(data['test_results'])
                    except json.JSONDecodeError:
                        data['test_results'] = None
                return data
            return None

    def get_all_module_progress(self, student_id: int) -> Dict[int, Dict]:
        """Get all module progress for a student."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM module_progress
                WHERE student_id = ?
                ORDER BY module_id
            ''', (student_id,))

            progress = {}
            for row in cursor.fetchall():
                data = dict(row)
                module_id = data.pop('module_id')
                data.pop('student_id')
                data.pop('id')

                # Parse test_results JSON
                if data.get('test_results'):
                    try:
                        data['test_results'] = json.loads(data['test_results'])
                    except json.JSONDecodeError:
                        data['test_results'] = None

                progress[module_id] = data

            return progress

    def save_module_progress(self, student_id: int, module_id: int,
                            progress_data: Dict):
        """Save or update module progress."""
        # Extract fields
        quiz_passed = progress_data.get('quiz_passed', False)
        project_passed = progress_data.get('project_passed', False)
        quiz_score = progress_data.get('quiz_score', 0)
        attempts = progress_data.get('attempts', 0)
        last_submission = progress_data.get('last_submission')
        test_results = progress_data.get('test_results')

        # Convert test_results to JSON string if it's a dict
        if test_results and isinstance(test_results, dict):
            test_results = json.dumps(test_results)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO module_progress
                (student_id, module_id, quiz_passed, project_passed,
                 quiz_score, attempts, last_submission, test_results)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id, module_id) DO UPDATE SET
                    quiz_passed = excluded.quiz_passed,
                    project_passed = excluded.project_passed,
                    quiz_score = excluded.quiz_score,
                    attempts = excluded.attempts,
                    last_submission = excluded.last_submission,
                    test_results = excluded.test_results
            ''', (student_id, module_id, quiz_passed, project_passed,
                  quiz_score, attempts, last_submission, test_results))

    def initialize_student_modules(self, student_id: int, module_count: int):
        """Initialize empty progress for all modules."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for module_id in range(1, module_count + 1):
                cursor.execute('''
                    INSERT OR IGNORE INTO module_progress
                    (student_id, module_id, quiz_passed, project_passed,
                     quiz_score, attempts)
                    VALUES (?, ?, 0, 0, 0, 0)
                ''', (student_id, module_id))


# Global database manager instance
_db_manager = DatabaseManager()


# API functions that mirror the old JSON interface
def get_student_progress(student_name: str) -> Dict:
    """
    Get progress for a specific student.
    Returns progress dict in the same format as the old JSON system.
    """
    # Import here to avoid circular dependency
    from module_loader import get_module_count

    student = _db_manager.get_student_by_name(student_name)

    if not student:
        # Create new student
        module_count = get_module_count()
        student_id = _db_manager.create_student(student_name)
        _db_manager.initialize_student_modules(student_id, module_count)
        student = _db_manager.get_student_by_id(student_id)

    # Get all module progress
    modules = _db_manager.get_all_module_progress(student['id'])

    # If no modules exist yet (fresh student), initialize them
    if not modules:
        module_count = get_module_count()
        _db_manager.initialize_student_modules(student['id'], module_count)
        modules = _db_manager.get_all_module_progress(student['id'])

    # Return in old format
    return {
        'current_module': student['current_module'],
        'modules': modules,
        'completed': bool(student['completed']),
        'started_at': student['started_at']
    }


def update_student_progress(student_name: str, updates: Dict):
    """
    Update and save student progress.
    Accepts updates dict in the same format as the old JSON system.
    """
    student = _db_manager.get_student_by_name(student_name)
    if not student:
        return

    student_id = student['id']

    # Update student-level fields
    student_updates = {}
    if 'current_module' in updates:
        student_updates['current_module'] = updates['current_module']
    if 'completed' in updates:
        student_updates['completed'] = updates['completed']

    if student_updates:
        _db_manager.update_student(student_name, **student_updates)

    # Update module-level fields
    if 'modules' in updates:
        for module_id, module_data in updates['modules'].items():
            _db_manager.save_module_progress(student_id, module_id, module_data)


def get_all_students_progress() -> Dict[str, Dict]:
    """
    Get progress for all students.
    Returns dict in same format as old load_progress().
    """
    all_progress = {}
    students = _db_manager.get_all_students()

    for student in students:
        modules = _db_manager.get_all_module_progress(student['id'])
        all_progress[student['name']] = {
            'current_module': student['current_module'],
            'modules': modules,
            'completed': bool(student['completed']),
            'started_at': student['started_at']
        }

    return all_progress


def export_student_to_json(student_name: str, output_file: str):
    """Export a student's progress to JSON file."""
    progress = get_student_progress(student_name)
    with open(output_file, 'w') as f:
        json.dump({student_name: progress}, f, indent=2)


def import_student_from_json(input_file: str, overwrite: bool = False):
    """Import a student's progress from JSON file."""
    with open(input_file, 'r') as f:
        data = json.load(f)

    for student_name, progress in data.items():
        existing = _db_manager.get_student_by_name(student_name)

        if existing and not overwrite:
            print(f"Student '{student_name}' already exists. Use overwrite=True to replace.")
            continue

        if existing:
            # Delete existing student
            _db_manager.delete_student(student_name)

        # Create new student
        student_id = _db_manager.create_student(
            student_name,
            current_module=progress.get('current_module', 1),
            started_at=progress.get('started_at')
        )

        # Import module progress
        modules = progress.get('modules', {})
        for module_id, module_data in modules.items():
            _db_manager.save_module_progress(student_id, int(module_id), module_data)

        # Update completed status
        if progress.get('completed'):
            _db_manager.update_student(student_name, completed=True)

        print(f"Imported student: {student_name}")


# For backward compatibility
load_progress = get_all_students_progress
save_progress = lambda progress: None  # No-op, updates happen via update_student_progress


# Export database manager for admin tools
def get_db_manager():
    """Get the global database manager instance."""
    return _db_manager
