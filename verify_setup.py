#!/usr/bin/env python3
"""
Verification script for Python Classroom setup
Checks that all necessary files and directories exist
"""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✓ {description}: {filepath} ({size} bytes)")
        return True
    else:
        print(f"✗ MISSING {description}: {filepath}")
        return False

def check_dir(dirpath, description):
    """Check if a directory exists."""
    if os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ MISSING {description}: {dirpath}")
        return False

def main():
    print("=" * 60)
    print("Python Classroom - Setup Verification")
    print("=" * 60)
    print()

    all_good = True

    # Check main files
    print("Checking main files...")
    all_good &= check_file("app.py", "Flask application")
    all_good &= check_file("requirements.txt", "Dependencies file")
    all_good &= check_file("README.md", "Documentation")
    all_good &= check_file("run.sh", "Start script")
    print()

    # Check testers
    print("Checking testers...")
    all_good &= check_file("testers/module1_tester.py", "Module 1 tester")
    all_good &= check_file("testers/module2_tester.py", "Module 2 tester")
    all_good &= check_file("testers/module3_tester.py", "Module 3 tester")
    print()

    # Check templates
    print("Checking templates...")
    all_good &= check_file("templates/base.html", "Base template")
    all_good &= check_file("templates/home.html", "Home page")
    all_good &= check_file("templates/module.html", "Module page")
    all_good &= check_file("templates/quiz.html", "Quiz page")
    all_good &= check_file("templates/submission.html", "Submission page")
    all_good &= check_file("templates/results.html", "Results page")
    all_good &= check_file("templates/progress.html", "Progress page")
    print()

    # Check static files
    print("Checking static files...")
    all_good &= check_file("static/css/style.css", "CSS stylesheet")
    all_good &= check_file("static/js/app.js", "JavaScript file")
    print()

    # Check directories
    print("Checking directories...")
    all_good &= check_dir("data", "Data directory")
    all_good &= check_dir("data/submissions", "Submissions directory")
    all_good &= check_dir("data/submissions/module1", "Module 1 submissions")
    all_good &= check_dir("data/submissions/module2", "Module 2 submissions")
    all_good &= check_dir("data/submissions/module3", "Module 3 submissions")
    print()

    # Check Python imports
    print("Checking Python dependencies...")
    try:
        import flask
        print(f"✓ Flask installed (version {flask.__version__})")
    except ImportError:
        print("✗ Flask not installed - run: pip install -r requirements.txt")
        all_good = False

    try:
        import requests
        print(f"✓ Requests installed (version {requests.__version__})")
    except ImportError:
        print("✗ Requests not installed - run: pip install -r requirements.txt")
        all_good = False

    try:
        import bs4
        print(f"✓ BeautifulSoup4 installed (version {bs4.__version__})")
    except ImportError:
        print("✗ BeautifulSoup4 not installed - run: pip install -r requirements.txt")
        all_good = False
    print()

    # Summary
    print("=" * 60)
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Your Python Classroom is ready to use!")
        print()
        print("To start the application:")
        print("  ./run.sh")
        print()
        print("Or manually:")
        print("  python app.py")
        print()
        print("Then open: http://localhost:5000")
    else:
        print("❌ SOME CHECKS FAILED")
        print()
        print("Please review the errors above and fix missing files.")
        print("Run this script again after fixing issues.")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
