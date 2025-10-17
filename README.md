# Python Classroom 🐍

An interactive Python learning platform that guides students through a comprehensive Python curriculum with automated project testing and progress tracking.

## Overview

Python Classroom is a Flask-based web application that implements the "Python Protocol: Zero-to-Hero" curriculum. Students progress through three modules, taking quizzes and submitting projects that are automatically tested for correctness.

## Features

- **3 Comprehensive Modules**
  - Module 1: Python Fundamentals
  - Module 2: Structured Programming
  - Module 3: Advanced Concepts & Tools

- **Interactive Learning**
  - Detailed module content and objectives
  - Multiple-choice quizzes (75% required to pass)
  - Hands-on capstone projects for each module

- **Automated Testing**
  - Submit Python files for automated grading
  - Detailed test results with specific feedback
  - Multiple submission attempts allowed

- **Progress Tracking**
  - Personal dashboard showing completion status
  - Quiz scores and submission attempts
  - Module unlocking system (complete previous to access next)

- **Projects**
  1. **Module 1**: Number Guessing Game
  2. **Module 2**: Contact Book Application
  3. **Module 3**: Simple Web Scraper

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or navigate to the repository**
   ```bash
   cd /home/rune/Development/Python/classroom
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`

## Project Structure

```
classroom/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── classroom.md                # Original curriculum document
├── CLAUDE.md                   # Claude Code guidance
├── .gitignore                  # Git ignore rules
│
├── data/
│   ├── .gitkeep
│   ├── student_progress.json  # Student progress (auto-generated)
│   └── submissions/           # Student submissions (auto-generated)
│       ├── module1/
│       ├── module2/
│       └── module3/
│
├── testers/
│   ├── module1_tester.py      # Number Guessing Game tester
│   ├── module2_tester.py      # Contact Book tester
│   └── module3_tester.py      # Web Scraper tester
│
├── templates/
│   ├── base.html              # Base template
│   ├── home.html              # Landing page
│   ├── module.html            # Module content page
│   ├── quiz.html              # Quiz page
│   ├── submission.html        # Project submission page
│   ├── results.html           # Test results page
│   └── progress.html          # Progress dashboard
│
└── static/
    ├── css/
    │   └── style.css          # Application styles
    └── js/
        └── app.js             # Frontend JavaScript (optional)
```

## How It Works

### For Students

1. **Start Learning**
   - Enter your name on the home page
   - Begin with Module 1

2. **Complete Each Module**
   - Read the module objectives and topics
   - Take the quiz (need 75% to pass)
   - Build the capstone project
   - Submit your Python file for testing

3. **Automated Testing**
   - Your code is tested against multiple criteria
   - Receive detailed feedback on what passed/failed
   - Revise and resubmit until you pass

4. **Progress Through Modules**
   - Complete all requirements to unlock the next module
   - Track your progress on the dashboard
   - Earn completion when all 3 modules are done

### Module Requirements

#### Module 1: Number Guessing Game
- Use `random` module
- Implement `input()` for user guesses
- Use `while` loop for gameplay
- Provide "Too high"/"Too low" feedback
- Congratulate on correct guess

#### Module 2: Contact Book
- Define functions for each operation
- Store contacts in a file (CSV format)
- Load contacts on startup
- Handle `FileNotFoundError`
- Implement menu system with while loop

#### Module 3: Web Scraper
- Use `requests` library
- Parse HTML with `BeautifulSoup`
- Extract page title from `<title>` tag
- Handle network errors gracefully
- Use functions to organize code

## Testing System

Each module has a dedicated tester that checks:

- **Code Structure**: Required imports, functions, control structures
- **Functionality**: Program runs correctly with expected behavior
- **Requirements**: All project requirements are met
- **Error Handling**: Code handles edge cases gracefully

Students receive:
- Overall pass/fail status
- Detailed test-by-test results
- Specific feedback for failed tests
- Success percentage score

## Configuration

### Security Note

The `app.secret_key` in `app.py` is set to a default value. For production use, change it to a secure random string:

```python
app.secret_key = 'your-secure-random-secret-key-here'
```

### File Upload Limits

- Maximum file size: 1MB
- Allowed extensions: `.py`

Modify in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB
app.config['ALLOWED_EXTENSIONS'] = {'py'}
```

### Port Configuration

Default port is 5000. Change in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Development

### Running in Development Mode

The application runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error pages
- Interactive debugger

For production, set `debug=False` in `app.py`.

### Adding New Modules

To add a new module:

1. Update the `MODULES` dictionary in `app.py`
2. Create a new tester in `testers/module4_tester.py`
3. Add the module directory: `data/submissions/module4/`
4. Update templates if needed

### Customizing Tests

Each tester (`module1_tester.py`, etc.) can be customized:
- Modify test criteria
- Adjust passing threshold (default 70-75%)
- Add new test cases
- Change feedback messages

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
- **Solution**: Install requirements: `pip install -r requirements.txt`

**Issue**: Port 5000 already in use
- **Solution**: Change port in `app.py` or stop other application using port 5000

**Issue**: File upload fails
- **Solution**: Ensure `data/submissions/` directories exist (created automatically on first run)

**Issue**: Tests timeout
- **Solution**: Check for infinite loops in submitted code; timeout is set to 5-15 seconds

### Logs

Flask logs appear in the terminal where you ran `python app.py`. Check for:
- Request errors
- File upload issues
- Test execution problems

## License

This educational project is based on "The Python Protocol" curriculum.

## Contributing

To contribute:
1. Test the application thoroughly
2. Report bugs with detailed reproduction steps
3. Suggest improvements to curriculum or testing
4. Submit pull requests with clear descriptions

## Credits

- **Curriculum**: Based on "The Python Protocol: A Zero-to-Hero Developer's Roadmap"
- **Framework**: Flask web framework
- **Testing**: Custom Python testers for automated grading
- **Design**: Clean, educational-focused UI

## Support

For issues or questions:
1. Check this README thoroughly
2. Review error messages carefully
3. Check Flask logs in the terminal
4. Ensure all requirements are installed
5. Verify Python version (3.8+)

---

**Happy Learning! 🎓**

Start your journey from zero to Python hero!
