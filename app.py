"""
Python Classroom Application
Main Flask application for the Python learning platform.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
import os
import json
import sys
from datetime import datetime

# Add testers directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'testers'))

import module1_tester
import module2_tester
import module3_tester

app = Flask(__name__)
app.secret_key = 'python_classroom_secret_key_2024'  # Change in production
app.config['UPLOAD_FOLDER'] = 'data/submissions'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'py'}

# Module data extracted from classroom.md
MODULES = {
    1: {
        'title': 'Module 1: Python Fundamentals',
        'objective': 'To build an unshakable foundation in the core components of programming.',
        'topics': [
            'Variables and Data Types',
            'Operators and Input',
            'Control Flow (if/elif/else)',
            'Loops (for and while)',
            'Data Structures (lists, tuples, dictionaries, sets)'
        ],
        'quiz': [
            {
                'question': 'What is the difference between an integer and a float?',
                'options': [
                    'An integer is text, a float is a number',
                    'An integer is a whole number, a float has a decimal point',
                    'An integer is always positive, a float can be negative',
                    'There is no difference'
                ],
                'correct': 1
            },
            {
                'question': 'What will the following code print? print(5 == "5")',
                'options': ['True', 'False', 'Error', '5'],
                'correct': 1
            },
            {
                'question': 'Which data structure would be best for storing a user\'s profile?',
                'options': ['List', 'Set', 'Dictionary', 'Tuple'],
                'correct': 2
            },
            {
                'question': 'What is the primary purpose of a for loop?',
                'options': [
                    'To make decisions',
                    'To iterate over a sequence of items',
                    'To define functions',
                    'To handle errors'
                ],
                'correct': 1
            }
        ],
        'project': {
            'name': 'Number Guessing Game',
            'description': 'Build a number guessing game that generates a random number between 1 and 100. The user guesses, and the program provides "Too high!" or "Too low!" feedback until they guess correctly.',
            'requirements': [
                'Use the random module to generate the secret number',
                'Use input() to get user guesses',
                'Use a while loop for repeated guessing',
                'Use if/elif/else for feedback',
                'Congratulate the player on winning'
            ]
        }
    },
    2: {
        'title': 'Module 2: Structured Programming',
        'objective': 'To write organized, reusable, and robust programs with functions and file handling.',
        'topics': [
            'Functions (def, parameters, return)',
            'Scope (local vs. global variables)',
            'Error and Exception Handling (try/except)',
            'File I/O (reading and writing files)',
            'Working with CSV data'
        ],
        'quiz': [
            {
                'question': 'What is the main benefit of using a function?',
                'options': [
                    'To make the code run faster',
                    'To make the code reusable and organized',
                    'To store variables',
                    'To handle errors'
                ],
                'correct': 1
            },
            {
                'question': 'A variable defined inside a function has what kind of scope?',
                'options': ['Global Scope', 'Universal Scope', 'Functional Scope', 'Local Scope'],
                'correct': 3
            },
            {
                'question': 'What is the purpose of a try...except block?',
                'options': [
                    'To try code and see if it is efficient',
                    'To handle potential errors gracefully',
                    'To create a loop',
                    'To define a function'
                ],
                'correct': 1
            },
            {
                'question': 'Which file mode adds content to the end of a file?',
                'options': ["'r'", "'w'", "'a'", "'x'"],
                'correct': 2
            }
        ],
        'project': {
            'name': 'Contact Book Application',
            'description': 'Create a command-line contact book with menu options to add, search, and list contacts. Contacts should be stored in a text file and persist between runs.',
            'requirements': [
                'Use functions for each menu option',
                'Store contacts in a dictionary in memory',
                'Save contacts to a file (CSV format recommended)',
                'Load contacts when program starts',
                'Handle FileNotFoundError gracefully',
                'Use a while loop for the main menu'
            ]
        }
    },
    3: {
        'title': 'Module 3: Advanced Concepts and Tools',
        'objective': 'To learn Object-Oriented Programming and leverage third-party libraries.',
        'topics': [
            'Object-Oriented Programming (classes and objects)',
            'Installing packages with pip',
            'Using third-party libraries (requests, BeautifulSoup)',
            'Introduction to debugging',
            'Introduction to Git'
        ],
        'quiz': [
            {
                'question': 'In OOP, what is the relationship between a class and an object?',
                'options': [
                    'They are the same thing',
                    'An object is a blueprint for a class',
                    'A class is a blueprint for an object',
                    'A class is a variable, an object is a function'
                ],
                'correct': 2
            },
            {
                'question': 'What tool is used to install Python packages from PyPI?',
                'options': ['python install', 'py', 'install', 'pip'],
                'correct': 3
            },
            {
                'question': 'What is the primary purpose of Git?',
                'options': [
                    'To make code run faster',
                    'To fix bugs automatically',
                    'To track changes and enable collaboration',
                    'To install libraries'
                ],
                'correct': 2
            },
            {
                'question': 'In a class, what is a function called?',
                'options': ['A method', 'An attribute', 'A parameter', 'An instance'],
                'correct': 0
            }
        ],
        'project': {
            'name': 'Simple Web Scraper',
            'description': 'Build a web scraper that prompts for a URL, fetches the webpage, and extracts and displays the page title.',
            'requirements': [
                'Use requests library to fetch webpages',
                'Use BeautifulSoup to parse HTML',
                'Extract the <title> tag content',
                'Handle network errors gracefully',
                'Use functions to organize code'
            ]
        }
    }
}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_progress():
    """Load student progress from JSON file."""
    progress_file = 'data/student_progress.json'
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {}


def save_progress(progress):
    """Save student progress to JSON file."""
    progress_file = 'data/student_progress.json'
    os.makedirs('data', exist_ok=True)
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)


def get_student_progress(student_name):
    """Get progress for a specific student."""
    all_progress = load_progress()
    if student_name not in all_progress:
        all_progress[student_name] = {
            'current_module': 1,
            'modules': {
                1: {'quiz_passed': False, 'project_passed': False, 'quiz_score': 0, 'attempts': 0},
                2: {'quiz_passed': False, 'project_passed': False, 'quiz_score': 0, 'attempts': 0},
                3: {'quiz_passed': False, 'project_passed': False, 'quiz_score': 0, 'attempts': 0}
            },
            'completed': False,
            'started_at': datetime.now().isoformat()
        }
        save_progress(all_progress)
    return all_progress[student_name]


def update_student_progress(student_name, updates):
    """Update and save student progress."""
    all_progress = load_progress()
    if student_name in all_progress:
        all_progress[student_name].update(updates)
        save_progress(all_progress)


@app.route('/')
def index():
    """Home page."""
    return render_template('home.html')


@app.route('/start', methods=['GET', 'POST'])
def start():
    """Start learning - get student name."""
    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        if student_name:
            session['student_name'] = student_name
            progress = get_student_progress(student_name)
            return redirect(url_for('module', module_id=progress['current_module']))
        flash('Please enter your name', 'error')
    return render_template('home.html')


@app.route('/module/<int:module_id>')
def module(module_id):
    """Display module content."""
    if 'student_name' not in session:
        return redirect(url_for('index'))

    if module_id not in MODULES:
        flash('Invalid module', 'error')
        return redirect(url_for('progress_page'))

    student_name = session['student_name']
    progress = get_student_progress(student_name)

    # Check if student can access this module
    if module_id > progress['current_module']:
        flash(f'Complete Module {progress["current_module"]} first', 'warning')
        return redirect(url_for('module', module_id=progress['current_module']))

    module_data = MODULES[module_id]
    module_progress = progress['modules'][module_id]

    return render_template('module.html',
                         module_id=module_id,
                         module=module_data,
                         progress=module_progress)


@app.route('/quiz/<int:module_id>', methods=['GET', 'POST'])
def quiz(module_id):
    """Quiz page."""
    if 'student_name' not in session:
        return redirect(url_for('index'))

    if module_id not in MODULES:
        return redirect(url_for('progress_page'))

    student_name = session['student_name']
    progress = get_student_progress(student_name)

    if request.method == 'POST':
        # Grade quiz
        answers = request.form
        module_quiz = MODULES[module_id]['quiz']
        correct_count = 0

        for i, question in enumerate(module_quiz):
            student_answer = int(answers.get(f'q{i}', -1))
            if student_answer == question['correct']:
                correct_count += 1

        percentage = int((correct_count / len(module_quiz)) * 100)
        passed = percentage >= 75  # 75% to pass

        # Update progress
        progress['modules'][module_id]['quiz_score'] = percentage
        progress['modules'][module_id]['quiz_passed'] = passed
        update_student_progress(student_name, progress)

        if passed:
            flash(f'Quiz passed with {percentage}%! You can now submit your project.', 'success')
            return redirect(url_for('submission', module_id=module_id))
        else:
            flash(f'Quiz score: {percentage}%. You need 75% to pass. Try again!', 'warning')

    module_data = MODULES[module_id]
    return render_template('quiz.html', module_id=module_id, module=module_data)


@app.route('/submission/<int:module_id>', methods=['GET', 'POST'])
def submission(module_id):
    """Project submission page."""
    if 'student_name' not in session:
        return redirect(url_for('index'))

    student_name = session['student_name']
    progress = get_student_progress(student_name)

    # Check if quiz is passed
    if not progress['modules'][module_id]['quiz_passed']:
        flash('Complete the quiz first', 'warning')
        return redirect(url_for('quiz', module_id=module_id))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save file
            filename = secure_filename(f"{student_name}_module{module_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
            module_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'module{module_id}')
            os.makedirs(module_dir, exist_ok=True)
            filepath = os.path.join(module_dir, filename)
            file.save(filepath)

            # Test submission
            progress['modules'][module_id]['attempts'] += 1

            if module_id == 1:
                test_result = module1_tester.test_submission(filepath)
            elif module_id == 2:
                test_result = module2_tester.test_submission(filepath)
            elif module_id == 3:
                test_result = module3_tester.test_submission(filepath)
            else:
                test_result = {'passed': False, 'message': 'Invalid module'}

            # Update progress
            progress['modules'][module_id]['project_passed'] = test_result['passed']
            progress['modules'][module_id]['last_submission'] = datetime.now().isoformat()
            progress['modules'][module_id]['test_results'] = test_result

            if test_result['passed']:
                # Unlock next module
                if module_id < 3:
                    progress['current_module'] = module_id + 1
                    flash(f'Congratulations! Module {module_id} completed. Module {module_id + 1} unlocked!', 'success')
                else:
                    progress['completed'] = True
                    progress['completed_at'] = datetime.now().isoformat()
                    flash('Congratulations! You have completed all modules!', 'success')
            else:
                flash(f'Tests failed. Score: {test_result["score"]}. Please review and try again.', 'warning')

            update_student_progress(student_name, progress)

            return render_template('results.html',
                                 module_id=module_id,
                                 module=MODULES[module_id],
                                 results=test_result)

        flash('Invalid file type. Please upload a .py file', 'error')

    module_data = MODULES[module_id]
    module_progress = progress['modules'][module_id]
    return render_template('submission.html',
                         module_id=module_id,
                         module=module_data,
                         progress=module_progress)


@app.route('/progress')
def progress_page():
    """Student progress dashboard."""
    if 'student_name' not in session:
        return redirect(url_for('index'))

    student_name = session['student_name']
    progress = get_student_progress(student_name)

    return render_template('progress.html',
                         student_name=student_name,
                         progress=progress,
                         modules=MODULES)


@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data/submissions/module1', exist_ok=True)
    os.makedirs('data/submissions/module2', exist_ok=True)
    os.makedirs('data/submissions/module3', exist_ok=True)

    app.run(debug=True, host='0.0.0.0', port=5000)
