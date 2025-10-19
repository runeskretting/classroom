#!/usr/bin/env python3
"""
Student Administration CLI Tool
Manage students and their progress in Python Classroom.
"""

import sys
import argparse
import os
from datetime import datetime
from db_manager import (
    get_db_manager,
    get_student_progress,
    export_student_to_json,
    import_student_from_json
)


def list_students():
    """List all students with their progress."""
    db = get_db_manager()
    students = db.get_all_students()

    if not students:
        print("No students found.")
        return

    print(f"\n{'Name':<20} {'Current Module':<15} {'Completed':<10} {'Started':<20}")
    print("=" * 70)

    for student in students:
        name = student['name']
        current = student['current_module']
        completed = "Yes" if student['completed'] else "No"
        started = student['started_at'][:19]  # Trim microseconds

        print(f"{name:<20} {current:<15} {completed:<10} {started:<20}")

    print(f"\nTotal students: {len(students)}\n")


def view_student(student_name):
    """View detailed progress for a specific student."""
    db = get_db_manager()
    student = db.get_student_by_name(student_name)

    if not student:
        print(f"Student '{student_name}' not found.")
        return

    print(f"\n{'='*60}")
    print(f" Student: {student['name']}")
    print(f"{'='*60}")
    print(f"Started: {student['started_at'][:19]}")
    print(f"Current Module: {student['current_module']}")
    print(f"Completed: {'Yes' if student['completed'] else 'No'}")
    print()

    # Get module progress
    modules = db.get_all_module_progress(student['id'])

    if not modules:
        print("No module progress found.")
        return

    print(f"{'Module':<8} {'Quiz':<10} {'Project':<10} {'Score':<8} {'Attempts':<10}")
    print("-" * 60)

    for module_id in sorted(modules.keys()):
        data = modules[module_id]
        quiz = "✓ Passed" if data['quiz_passed'] else "✗ Not passed"
        project = "✓ Passed" if data['project_passed'] else "✗ Not passed"
        score = f"{data['quiz_score']}%"
        attempts = data['attempts']

        print(f"{module_id:<8} {quiz:<10} {project:<10} {score:<8} {attempts:<10}")

    print()


def delete_student(student_name, confirm=False):
    """Delete a student and all their progress."""
    db = get_db_manager()
    student = db.get_student_by_name(student_name)

    if not student:
        print(f"Student '{student_name}' not found.")
        return

    if not confirm:
        response = input(f"Are you sure you want to delete '{student_name}'? This cannot be undone. (yes/no): ")
        if response.lower() != 'yes':
            print("Deletion cancelled.")
            return

    if db.delete_student(student_name):
        print(f"Student '{student_name}' has been deleted.")
    else:
        print(f"Failed to delete student '{student_name}'.")


def export_student(student_name, output_file=None):
    """Export student progress to JSON file."""
    db = get_db_manager()
    student = db.get_student_by_name(student_name)

    if not student:
        print(f"Student '{student_name}' not found.")
        return

    if not output_file:
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"{student_name}_progress_{timestamp}.json"

    try:
        export_student_to_json(student_name, output_file)
        print(f"Student progress exported to: {output_file}")
    except Exception as e:
        print(f"Error exporting student: {e}")


def import_student(input_file, overwrite=False):
    """Import student progress from JSON file."""
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    try:
        import_student_from_json(input_file, overwrite=overwrite)
        print("Import completed successfully.")
    except Exception as e:
        print(f"Error importing student: {e}")


def backup_database(backup_dir='data/backups'):
    """Create a timestamped backup of the database."""
    import shutil

    db = get_db_manager()
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'classroom_{timestamp}.db')

    try:
        shutil.copy2(db.db_path, backup_file)
        print(f"Database backed up to: {backup_file}")
    except Exception as e:
        print(f"Error creating backup: {e}")


def restore_database(backup_file):
    """Restore database from a backup file."""
    import shutil

    if not os.path.exists(backup_file):
        print(f"Backup file not found: {backup_file}")
        return

    db = get_db_manager()

    response = input("This will overwrite the current database. Are you sure? (yes/no): ")
    if response.lower() != 'yes':
        print("Restore cancelled.")
        return

    try:
        # Create a backup of current database first
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safety_backup = f"{db.db_path}.before_restore_{timestamp}"
        shutil.copy2(db.db_path, safety_backup)
        print(f"Current database backed up to: {safety_backup}")

        # Restore from backup
        shutil.copy2(backup_file, db.db_path)
        print(f"Database restored from: {backup_file}")
    except Exception as e:
        print(f"Error restoring database: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Python Classroom Student Administration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          # List all students
  %(prog)s view alice                    # View detailed progress for alice
  %(prog)s delete bob                    # Delete student bob
  %(prog)s export alice output.json     # Export alice's progress
  %(prog)s import backup.json           # Import student from file
  %(prog)s backup                       # Create database backup
  %(prog)s restore backups/file.db      # Restore from backup
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    subparsers.add_parser('list', help='List all students')

    # View command
    view_parser = subparsers.add_parser('view', help='View student details')
    view_parser.add_argument('student_name', help='Name of the student')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a student')
    delete_parser.add_argument('student_name', help='Name of the student')
    delete_parser.add_argument('--yes', action='store_true', help='Skip confirmation')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export student to JSON')
    export_parser.add_argument('student_name', help='Name of the student')
    export_parser.add_argument('output_file', nargs='?', help='Output JSON file (optional)')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import student from JSON')
    import_parser.add_argument('input_file', help='Input JSON file')
    import_parser.add_argument('--overwrite', action='store_true',
                              help='Overwrite if student exists')

    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup database')
    backup_parser.add_argument('--dir', default='data/backups',
                              help='Backup directory (default: data/backups)')

    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore database from backup')
    restore_parser.add_argument('backup_file', help='Backup file to restore from')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute command
    if args.command == 'list':
        list_students()
    elif args.command == 'view':
        view_student(args.student_name)
    elif args.command == 'delete':
        delete_student(args.student_name, confirm=args.yes)
    elif args.command == 'export':
        export_student(args.student_name, args.output_file)
    elif args.command == 'import':
        import_student(args.input_file, overwrite=args.overwrite)
    elif args.command == 'backup':
        backup_database(args.dir)
    elif args.command == 'restore':
        restore_database(args.backup_file)


if __name__ == '__main__':
    main()
