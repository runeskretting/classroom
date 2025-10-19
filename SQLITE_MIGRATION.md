# SQLite Migration Guide

## Overview

The Python Classroom application has been successfully migrated from JSON-based storage to SQLite database for student progress tracking. This provides better portability, data integrity, and concurrent access handling.

## What Changed

### Before (JSON-based)
- Student progress stored in `data/student_progress.json`
- Simple but not ideal for concurrent access
- Manual backup required

### After (SQLite-based)
- Student progress stored in `data/classroom.db`
- ACID-compliant transactions
- Built-in concurrent access handling
- Easy backup/restore functionality
- Import/export capabilities

## Database Structure

### Tables

**students**
- `id` - Primary key
- `name` - Unique student name
- `current_module` - Current module number
- `completed` - Completion status
- `started_at` - Timestamp when student started

**module_progress**
- `id` - Primary key
- `student_id` - Foreign key to students table
- `module_id` - Module number
- `quiz_passed` - Quiz completion status
- `project_passed` - Project completion status
- `quiz_score` - Quiz score percentage
- `attempts` - Number of submission attempts
- `last_submission` - Timestamp of last submission
- `test_results` - JSON blob with test details

## Auto-Migration

The application automatically migrates from JSON to SQLite on first run:

1. If `data/classroom.db` doesn't exist AND `data/student_progress.json` exists
2. Creates backup: `data/student_progress.json.backup_TIMESTAMP`
3. Migrates all student data to SQLite
4. Original JSON file remains untouched

## Student Administration Tool

A CLI tool is provided for managing students:

```bash
./student_admin.py <command> [options]
```

### Commands

**List all students:**
```bash
./student_admin.py list
```

**View student details:**
```bash
./student_admin.py view <student_name>
```

**Delete a student:**
```bash
./student_admin.py delete <student_name>
./student_admin.py delete <student_name> --yes  # Skip confirmation
```

**Export student to JSON:**
```bash
./student_admin.py export <student_name>
./student_admin.py export <student_name> output.json
```

**Import student from JSON:**
```bash
./student_admin.py import backup.json
./student_admin.py import backup.json --overwrite
```

**Backup database:**
```bash
./student_admin.py backup
./student_admin.py backup --dir /path/to/backups
```

**Restore from backup:**
```bash
./student_admin.py restore data/backups/classroom_TIMESTAMP.db
```

## Portability Between Machines

To move student data between machines:

### Option 1: Copy Database File
```bash
# On machine A
cp data/classroom.db /path/to/usb/

# On machine B
cp /path/to/usb/classroom.db data/
```

### Option 2: Export/Import JSON
```bash
# On machine A - export specific student
./student_admin.py export alice alice_backup.json

# On machine B - import student
./student_admin.py import alice_backup.json
```

### Option 3: Database Backup/Restore
```bash
# On machine A - create backup
./student_admin.py backup

# Copy data/backups/classroom_TIMESTAMP.db to machine B
# On machine B - restore
./student_admin.py restore classroom_TIMESTAMP.db
```

## Manual Migration

If you need to manually migrate from JSON to SQLite:

```bash
./migrate_to_sqlite.py
./migrate_to_sqlite.py --json-file /path/to/custom.json
./migrate_to_sqlite.py --no-backup  # Don't create JSON backup
```

## API Reference

For developers, the same functions are available as before:

```python
from db_manager import get_student_progress, update_student_progress

# Get student progress
progress = get_student_progress('student_name')

# Update progress
update_student_progress('student_name', {
    'current_module': 3,
    'modules': {
        2: {
            'quiz_passed': True,
            'quiz_score': 90,
            'project_passed': True,
            'attempts': 2
        }
    }
})
```

## Backup Best Practices

1. **Regular Backups:** Run `./student_admin.py backup` regularly
2. **Before Updates:** Always backup before updating the application
3. **Multiple Locations:** Keep backups in different locations
4. **Test Restores:** Periodically test that restores work

## Troubleshooting

### Database is locked
Multiple processes trying to access the database. Close other instances of the app.

### Migration fails
Check that:
- JSON file exists and is valid
- No permission issues on data/ directory
- Database doesn't already exist (or use `--force`)

### Lost data after migration
Check `data/student_progress.json.backup_*` files - your original data is preserved there.

### Can't see students after migration
Verify database exists:
```bash
ls -la data/classroom.db
./student_admin.py list
```

## File Structure

```
data/
├── classroom.db              # Main SQLite database
├── student_progress.json     # Original JSON (kept for reference)
├── student_progress.json.backup_* # Migration backup
└── backups/                  # Database backups
    └── classroom_TIMESTAMP.db
```

## Benefits of SQLite

✅ **Portable:** Single file, easy to copy between machines
✅ **Reliable:** ACID transactions ensure data integrity
✅ **Concurrent:** Better handling of multiple users
✅ **Fast:** Optimized queries with indexes
✅ **Standard:** No external dependencies (built into Python)
✅ **Manageable:** CLI tools for easy administration

## Questions?

For issues or questions about the SQLite migration, check the main README or create an issue on GitHub.
