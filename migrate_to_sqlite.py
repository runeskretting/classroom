#!/usr/bin/env python3
"""
Migration Script: JSON to SQLite
Migrates student progress from student_progress.json to SQLite database.
"""

import json
import os
import shutil
from datetime import datetime
from db_manager import get_db_manager


def migrate_from_json(json_file='data/student_progress.json',
                     create_backup=True):
    """
    Migrate student progress from JSON file to SQLite database.

    Args:
        json_file: Path to the JSON progress file
        create_backup: If True, creates a backup of the JSON file

    Returns:
        tuple: (success: bool, message: str, students_migrated: int)
    """
    # Check if JSON file exists
    if not os.path.exists(json_file):
        return False, "JSON file not found. Nothing to migrate.", 0

    # Check if database already exists
    db = get_db_manager()
    existing_students = db.get_all_students()
    if existing_students:
        return False, f"Database already contains {len(existing_students)} student(s). Migration skipped.", 0

    # Create backup if requested
    if create_backup:
        backup_file = f"{json_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            shutil.copy2(json_file, backup_file)
            print(f"Created backup: {backup_file}")
        except Exception as e:
            return False, f"Failed to create backup: {e}", 0

    # Load JSON data
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON file: {e}", 0
    except Exception as e:
        return False, f"Error reading JSON file: {e}", 0

    if not data:
        return True, "JSON file is empty. No students to migrate.", 0

    # Migrate each student
    students_migrated = 0
    errors = []

    for student_name, progress in data.items():
        try:
            # Create student record
            current_module = progress.get('current_module', 1)
            started_at = progress.get('started_at', datetime.now().isoformat())
            completed = progress.get('completed', False)

            student_id = db.create_student(
                name=student_name,
                current_module=current_module,
                started_at=started_at
            )

            # Update completed status if needed
            if completed:
                db.update_student(student_name, completed=True)

            # Migrate module progress
            modules = progress.get('modules', {})
            for module_id_str, module_data in modules.items():
                try:
                    module_id = int(module_id_str)
                    db.save_module_progress(student_id, module_id, module_data)
                except ValueError:
                    errors.append(f"Invalid module ID '{module_id_str}' for student '{student_name}'")
                except Exception as e:
                    errors.append(f"Error migrating module {module_id_str} for '{student_name}': {e}")

            students_migrated += 1
            print(f"✓ Migrated: {student_name}")

        except Exception as e:
            errors.append(f"Error migrating student '{student_name}': {e}")
            continue

    # Build result message
    if students_migrated == len(data):
        message = f"Successfully migrated all {students_migrated} student(s) to SQLite."
    else:
        message = f"Migrated {students_migrated}/{len(data)} student(s). "
        if errors:
            message += f"Errors: {'; '.join(errors[:3])}"  # Show first 3 errors

    success = students_migrated > 0
    return success, message, students_migrated


def auto_migrate():
    """
    Automatically migrate from JSON to SQLite if conditions are met.
    Called by app.py on startup.

    Returns:
        bool: True if migration was performed, False otherwise
    """
    db_path = 'data/classroom.db'
    json_path = 'data/student_progress.json'

    # If database doesn't exist and JSON file exists, migrate
    if not os.path.exists(db_path) and os.path.exists(json_path):
        print("\n" + "="*60)
        print("MIGRATION: JSON to SQLite")
        print("="*60)
        print("Detecting first run with existing JSON data...")
        print("Migrating student progress to SQLite database...\n")

        success, message, count = migrate_from_json(json_path, create_backup=True)

        if success:
            print(f"\n✓ {message}")
            print("="*60 + "\n")
            return True
        else:
            print(f"\n✗ Migration failed: {message}")
            print("="*60 + "\n")
            return False

    return False


def main():
    """CLI entry point for manual migration."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Migrate Python Classroom student progress from JSON to SQLite'
    )
    parser.add_argument(
        '--json-file',
        default='data/student_progress.json',
        help='Path to JSON progress file (default: data/student_progress.json)'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup of JSON file'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force migration even if database already has students'
    )

    args = parser.parse_args()

    # Check database
    db = get_db_manager()
    existing_students = db.get_all_students()

    if existing_students and not args.force:
        print(f"Database already contains {len(existing_students)} student(s).")
        response = input("Continue with migration anyway? This may create duplicates. (yes/no): ")
        if response.lower() != 'yes':
            print("Migration cancelled.")
            return

    # Perform migration
    print("\nMigrating student progress from JSON to SQLite...")
    print(f"Source: {args.json_file}")
    print(f"Target: {db.db_path}\n")

    success, message, count = migrate_from_json(
        args.json_file,
        create_backup=not args.no_backup
    )

    if success:
        print(f"\n✓ SUCCESS: {message}")
    else:
        print(f"\n✗ FAILED: {message}")

    if count > 0:
        print(f"\nYou can verify the migration using:")
        print(f"  python student_admin.py list")


if __name__ == '__main__':
    main()
