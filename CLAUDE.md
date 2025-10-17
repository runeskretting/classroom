# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Flask-based Python learning platform called "Python Classroom". Students progress through 3 comprehensive modules, taking quizzes and submitting Python projects that are automatically tested. The curriculum is based on the `classroom.md` document - a "Zero-to-Hero" Python programming guide.

## Key Architecture Components

### 1. Flask Application (`app.py`)

**Core Pattern**: Single-file Flask app (~500 lines) with route handlers for each page type.

**MODULES Dictionary**: Central data structure (lines 27-191) containing all module content:
- Module objectives and topics
- Quiz questions with correct answers (4 per module)
- Project requirements and descriptions

**Progress System**: JSON-based student tracking (`data/student_progress.json`)
- `get_student_progress(student_name)`: Retrieves/initializes student progress
- `update_student_progress(student_name, updates)`: Saves progress
- Progress structure tracks: current_module, quiz_passed, project_passed, quiz_score, attempts

**Critical Flow**: Module unlocking is enforced in `module()` route (lines 261-286):
```python
if module_id > progress['current_module']:
    # Redirect to current module - prevents skipping
```

### 2. Automated Testing System (`testers/`)

Each module has a dedicated tester that runs student submissions in isolated subprocesses.

**Common Pattern Across All Testers**:
```python
def test_submission(filepath):
    tester = ModuleXTester(filepath)
    tester.run_all_tests()
    return {
        'passed': bool,
        'score': str,
        'tests': [list of test results],
        'message': str
    }
```

**Module 1 Tester** (`module1_tester.py`):
- Tests Number Guessing Game
- Checks: imports, code structure (while loop, if/elif), game logic
- Simulates gameplay with test input to verify feedback

**Module 2 Tester** (`module2_tester.py`):
- Tests Contact Book Application (most complex tester)
- Creates temporary copies to test file persistence
- Runs multiple subprocess calls to verify data persists between runs
- Tests: function definitions, add/search/list operations, menu system

**Module 3 Tester** (`module3_tester.py`):
- Tests Web Scraper
- **Unique feature**: Includes built-in HTTP test server (TestHTTPHandler)
- Starts local server on port 8765 during tests
- Tests: library imports, HTTP requests, HTML parsing, error handling

**Subprocess Execution Pattern**:
```python
result = subprocess.run(
    [sys.executable, submission_path],
    input=test_input,
    capture_output=True,
    text=True,
    timeout=5  # Prevents infinite loops
)
```

### 3. Student Workflow & Route Architecture

**Sequential Flow**:
1. `/` (index) → Welcome page
2. `/start` POST → Sets session['student_name']
3. `/module/<id>` → Display module content
4. `/quiz/<id>` → Quiz (need 75% to pass)
5. `/submission/<id>` → Upload .py file
6. Results rendered immediately after testing
7. `/progress` → Dashboard showing all modules

**Session Management**: Flask sessions track current student via `session['student_name']`

**File Upload Security** (lines 194-196, 342-360):
- 1MB max file size
- `.py` extension only
- `secure_filename()` prevents path traversal
- Files saved as: `{student}_module{id}_{timestamp}.py`

## Common Development Tasks

### Running the Application

**Quick Start**:
```bash
./run.sh  # Handles venv creation, dependencies, directory setup
```

**Manual Start**:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

Access at: `http://localhost:5000`

### Testing Without Web Interface

Test individual module testers directly:
```bash
python3 -c "
import sys; sys.path.append('testers')
import module1_tester
result = module1_tester.test_submission('path/to/student_code.py')
print(result)
"
```

### Adding a New Module

1. Update `MODULES` dict in `app.py` with new module data
2. Create `testers/module4_tester.py` following existing pattern
3. Create directory: `data/submissions/module4/`
4. Update line 432-434 in `app.py` to create module4 directory
5. Add module4 test import and conditional in `/submission/<id>` route

### Modifying Test Criteria

Each tester has adjustable pass thresholds:
```python
# In tester's run_all_tests() method
self.passed = passed_count >= total_count * 0.75  # Change percentage here
```

## Important Implementation Details

### Progress Data Structure
```python
{
  "student_name": {
    "current_module": 1,  # Controls which modules are unlocked
    "modules": {
      1: {
        "quiz_passed": False,
        "project_passed": False,
        "quiz_score": 0,
        "attempts": 0,
        "test_results": {...}  # Last test run details
      }
    },
    "completed": False,
    "started_at": "ISO timestamp"
  }
}
```

### Test Result Structure
Returned by all testers:
```python
{
  "passed": bool,           # Overall pass/fail
  "score": "8/10 (80%)",   # Formatted score string
  "tests": [                # Individual test results
    {"name": "Test Name", "passed": True/False, "message": "..."}
  ],
  "message": "Overall feedback"
}
```

### Module 3 Special Consideration

The web scraper tester starts a test HTTP server. If tests fail with connection errors, check:
- Port 8765 availability
- The server properly starts/stops in `start_test_server()` and `stop_test_server()`
- Student code should accept URL via `input()` and handle the test URL `http://localhost:8765/`

## Template Architecture

**Base Template** (`templates/base.html`): All pages extend this
- Navbar with conditional links based on `session.get('student_name')`
- Flash message display with auto-hide (via `static/js/app.js`)
- Footer with curriculum credit

**Key Jinja2 Patterns Used**:
- `url_for()` for all route links
- `session.get('student_name')` for auth checks
- Module/progress data passed as template variables

## Security Notes

**Session Secret**: Line 21 in `app.py` has placeholder secret key:
```python
app.secret_key = 'python_classroom_secret_key_2024'  # Change in production
```
For production, use: `python -c 'import secrets; print(secrets.token_hex())'`

**Code Execution Safety**:
- All student code runs in subprocess with timeout (5-15 seconds)
- File size limited to 1MB
- No shell=True used (prevents injection)
- Tests run in isolated temp directories (Module 2)

## Configuration

**Port**: Default 5000 (line 436)
**Debug Mode**: Enabled by default (line 436) - disable for production
**File Upload Limits**: Lines 22-24
**Pass Thresholds**: Line 312 (quiz), varies in testers (project)

## Curriculum Content

The original curriculum document (`classroom.md`) contains:
- **Part I**: 3 modules with detailed explanations and project solutions
- **Part II**: 100-day roadmap (not implemented in the app)

When adding new content to the app, extract from `classroom.md` to maintain consistency with the original curriculum design.
