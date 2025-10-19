"""
Python Classroom Application
Main Flask application for the Python learning platform.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
import os
import json
import sys
import importlib
from datetime import datetime

# Add testers directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'testers'))

# Import module loader
from module_loader import get_all_modules, get_module, get_module_count

# Import database manager (replaces JSON-based progress storage)
from db_manager import get_student_progress, update_student_progress
from migrate_to_sqlite import auto_migrate

app = Flask(__name__)
app.secret_key = 'python_classroom_secret_key_2024'  # Change in production
app.config['UPLOAD_FOLDER'] = 'data/submissions'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'py'}

# Load modules dynamically from JSON files
# Old hardcoded MODULES dictionary has been replaced with dynamic loading
# Modules are now stored in modules/module_XXX.json files
MODULES = get_all_modules()

# Auto-migrate from JSON to SQLite on first run
auto_migrate()

# Legacy MODULES dictionary (kept for reference, not used)
# MODULES_OLD = {
#     1: {
#         'title': 'Module 1: Python Fundamentals',
#         'objective': 'To build an unshakable foundation in the core components of programming.',
#         'topics': [
#             'Variables and Data Types',
#             'Operators and Input',
#             'Control Flow (if/elif/else)',
#             'Loops (for and while)',
#             'Data Structures (lists, tuples, dictionaries, sets)'
#         ],
#         'instructional_content': {
#             'intro': 'The sequence of topics in this module is not arbitrary. It mirrors the fundamental cognitive process of building a logical solution. First, a program needs to handle information, so we learn how to store it. Once stored, that information needs to be manipulated or compared. Then, based on those comparisons, the program must decide what to do. Often, these actions need to be done repeatedly. Finally, to handle more than one piece of information at a time, we must learn how to organize it. This is the narrative of computation itself.',
#             'sections': [
#                 {
#                     'title': 'Your First Program: print() and Comments',
#                     'content': '''Tradition dictates that the first program in any new language should display the message "Hello, World!". This simple act provides an immediate sense of accomplishment and confirms that your setup is working correctly. In Python, this is incredibly straightforward.
# 
# The print() function is a built-in Python command that outputs whatever you put inside the parentheses to the console. The text "Hello, World!" is called a **string**, which is simply a sequence of characters. Comments, marked by the # symbol, are notes that the interpreter ignores; they are for you and other programmers to understand the code.''',
#                     'code': '''# This is a comment. The computer ignores it. It's for humans to read.
# print("Hello, World!")'''
#                 },
#                 {
#                     'title': 'Storing Information: Variables and Data Types',
#                     'content': '''To do anything useful, a program needs to store and manage information. We do this using **variables**. Think of a variable as a labeled box where you can store a piece of data. You give the box a name (the variable name) and put something inside it (the value).
# 
# The type of data you store determines what you can do with it. Python has several fundamental **data types**:
# 
# - **String (str):** Textual data, enclosed in quotes (e.g., "Hello", 'Python').
# - **Integer (int):** Whole numbers, positive or negative (e.g., 10, -5, 0).
# - **Float (float):** Numbers with a decimal point (e.g., 3.14, -0.001).
# - **Boolean (bool):** Represents truth values. It can only be True or False.''',
#                     'code': '''# 'name' is the variable, "Alice" is the value.
# name = "Alice"
# age = 30
# You can then use the variable name to access the value.
# print(name)
# print(age)'''
#                 },
#                 {
#                     'title': 'Working with Data: Operators and Input',
#                     'content': '''Once you have data in variables, you can work with it using **operators**.
# 
# - **Arithmetic Operators:** Perform mathematical calculations: + (addition), - (subtraction), * (multiplication), / (division).
# - **Comparison Operators:** Compare two values and result in a Boolean (True or False): == (equal to), != (not equal to), > (greater than), < (less than), >= (greater than or equal to), <= (less than or equal to).
# - **Logical Operators:** Combine Boolean values: and (both must be true), or (at least one must be true), not (inverts the value).
# 
# To make programs interactive, you can get input from the user with the input() function. This function prompts the user for text and returns it as a string.''',
#                     'code': '''user_name = input("What is your name? ")
# print("Hello, " + user_name)
# 
# input() always returns a string, so you might need to convert it.
# age_str = input("How old are you? ")
# age_int = int(age_str)  # This is called type casting
# print("Next year you will be", age_int + 1)'''
#                 },
#                 {
#                     'title': 'Making Decisions: Control Flow with if, elif, else',
#                     'content': '''Programs become powerful when they can make decisions. **Control flow** statements allow you to execute different blocks of code based on certain conditions. The primary tool for this is the if, elif (else if), and else structure. Imagine a flowchart: if a condition is true, follow one path; otherwise, follow another.''',
#                     'code': '''age = 19
# 
# if age >= 18:
#     print("You are eligible to vote.")
# else:
#     print("You are not yet eligible to vote.")
# 
# score = 85
# 
# if score >= 90:
#     print("Grade: A")
# elif score >= 80:
#     print("Grade: B")
# elif score >= 70:
#     print("Grade: C")
# else:
#     print("Grade: F")'''
#                 },
#                 {
#                     'title': 'Repeating Actions: The Power of Loops (for and while)',
#                     'content': '''Loops allow you to execute a block of code multiple times without rewriting it. There are two main types of loops in Python.
# 
# A **while loop** repeats a block of code as long as a certain condition remains true. It is essential to ensure the condition will eventually become false, or you will create an infinite loop.
# 
# A **for loop** iterates over a sequence of items (like the characters in a string or the elements in a list) and executes a block of code for each item.''',
#                     'code': '''count = 1
# while count <= 5:
#     print("Count is:", count)
#     count = count + 1  # This line prevents an infinite loop
# 
# for character in "Python":
#     print(character)
# 
# The range() function is often used with for loops to repeat a specific number of times.
# for i in range(5):  # This will loop for i = 0, 1, 2, 3, 4
#     print("Loop number", i)'''
#                 },
#                 {
#                     'title': 'Organizing Data: Introduction to Data Structures',
#                     'content': '''When you need to work with collections of data, you use **data structures**. Python provides several powerful, built-in options.
# 
# - **Lists (list):** An ordered, mutable (changeable) collection of items. Think of a shopping list where you can add, remove, or change items.
# - **Tuples (tuple):** An ordered, immutable (unchangeable) collection. Once a tuple is created, you cannot alter it. This is useful for data that should not be modified, like a set of geographic coordinates.
# - **Dictionaries (dict):** An unordered collection of key-value pairs. Think of a real-world dictionary or a phone book, where you look up a word (the key) to find its definition (the value).
# - **Sets (set):** An unordered collection of unique items. If you add a duplicate item to a set, it will be ignored. This is useful for tasks like finding the unique attendees at an event.''',
#                     'code': '''# Lists
# fruits = ["apple", "banana", "cherry"]
# fruits.append("orange")  # Add an item
# print(fruits[0])  # Access by index (starts at 0)
# 
# Tuples
# coordinates = (10.0, 20.0)
# 
# Dictionaries
# student = {"name": "Bob", "age": 25, "major": "Physics"}
# print(student["name"])  # Access value by key
# 
# Sets
# unique_numbers = {1, 2, 3, 2, 1}
# print(unique_numbers)  # Output will be {1, 2, 3}'''
#                 }
#             ]
#         },
#         'quiz': [
#             {
#                 'question': 'What is the difference between an integer and a float?',
#                 'options': [
#                     'An integer is text, a float is a number',
#                     'An integer is a whole number, a float has a decimal point',
#                     'An integer is always positive, a float can be negative',
#                     'There is no difference'
#                 ],
#                 'correct': 1
#             },
#             {
#                 'question': 'What will the following code print? print(5 == "5")',
#                 'options': ['True', 'False', 'Error', '5'],
#                 'correct': 1
#             },
#             {
#                 'question': 'Which data structure would be best for storing a user\'s profile?',
#                 'options': ['List', 'Set', 'Dictionary', 'Tuple'],
#                 'correct': 2
#             },
#             {
#                 'question': 'What is the primary purpose of a for loop?',
#                 'options': [
#                     'To make decisions',
#                     'To iterate over a sequence of items',
#                     'To define functions',
#                     'To handle errors'
#                 ],
#                 'correct': 1
#             }
#         ],
#         'project': {
#             'name': 'Number Guessing Game',
#             'description': 'Build a number guessing game that generates a random number between 1 and 100. The user guesses, and the program provides "Too high!" or "Too low!" feedback until they guess correctly.',
#             'requirements': [
#                 'Use the random module to generate the secret number',
#                 'Use input() to get user guesses',
#                 'Use a while loop for repeated guessing',
#                 'Use if/elif/else for feedback',
#                 'Congratulate the player on winning'
#             ]
#         }
#     },
#     2: {
#         'title': 'Module 2: Structured Programming',
#         'objective': 'To write organized, reusable, and robust programs with functions and file handling.',
#         'topics': [
#             'Functions (def, parameters, return)',
#             'Scope (local vs. global variables)',
#             'Error and Exception Handling (try/except)',
#             'File I/O (reading and writing files)',
#             'Working with CSV data'
#         ],
#         'instructional_content': {
#             'intro': 'As your programs grow, you will find yourself needing better ways to organize code, handle errors gracefully, and persist data between runs. This module teaches you the essential skills for writing professional, maintainable programs.',
#             'sections': [
#                 {
#                     'title': 'Organizing Your Code: Functions',
#                     'content': '''As your programs grow, you will find yourself writing the same blocks of code repeatedly. **Functions** are the solution to this problem. A function is a named, reusable block of code that performs a specific task. Think of it like a recipe: it has a name (e.g., "Bake a Cake"), it takes ingredients (**parameters**), it has a set of steps to follow, and it produces a result (a **return value**).
# 
# Using functions makes your code more organized (easier to read), more efficient (no repeated code), and easier to debug (you only need to fix the logic in one place).''',
#                     'code': '''# Defining a function called 'greet' that takes one parameter, 'name'.
# def greet(name):
#     print(f"Hello, {name}!")
# 
# Calling the function multiple times with different arguments.
# greet("Alice")
# greet("Bob")
# 
# A function that takes two numbers, adds them, and returns the result.
# def add_numbers(num1, num2):
#     result = num1 + num2
#     return result
# 
# Call the function and store its return value in a variable.
# sum_result = add_numbers(5, 3)
# print(sum_result)  # Output: 8'''
#                 },
#                 {
#                     'title': 'Understanding Scope: Local vs. Global Variables',
#                     'content': '''A critical concept when working with functions is **scope**. Scope refers to the region of the code where a variable is accessible.
# 
# - **Local Scope:** A variable created inside a function is a **local variable**. It only exists within that function and cannot be accessed from outside.
# - **Global Scope:** A variable created outside of any function is a **global variable**. It can be accessed from anywhere in your script, including inside functions.
# 
# Understanding scope is crucial for avoiding bugs where variables seem to "disappear" or have unexpected values. It is generally good practice to limit the use of global variables and instead pass data into functions as parameters and get data out using return statements.''',
#                     'code': '''global_variable = "I am global"
# 
# def my_function():
#     local_variable = "I am local"
#     print(global_variable)  # This works, can access global variables
#     print(local_variable)
# 
# my_function()
# print(local_variable)  # This would cause an error because local_variable is out of scope.'''
#                 },
#                 {
#                     'title': 'Handling the Unexpected: Error and Exception Handling',
#                     'content': '''What happens if your program asks the user for a number, but they type "hello" instead? The int() function will fail, and your program will crash with an error. Professional programs do not crash; they anticipate potential problems and handle them gracefully. This is called **exception handling**.
# 
# In Python, you use a try...except block. You put the code that might cause an error (an "exception") inside the try block. If an error occurs, the code in the except block is executed, and the program continues running instead of crashing.''',
#                     'code': '''try:
#     age_str = input("Enter your age: ")
#     age_int = int(age_str)
#     print(f"You are {age_int} years old.")
# except ValueError:
    # This block only runs if the int() conversion fails.
#     print("Invalid input. Please enter a number.")'''
#                 },
#                 {
#                     'title': 'Working with the Real World: Reading from and Writing to Files',
#                     'content': '''So far, all the data your programs have used (like the user's name or the contacts in a list) disappears when the program ends. To make data **persistent**, you need to save it to a file. Python makes file input/output (I/O) straightforward.
# 
# The basic process involves opening a file, performing an operation (read or write), and then closing the file. The 'with' statement automatically closes the file for you.
# 
# File I/O is a fundamental skill that allows your programs to save user data, load configurations, process large datasets, and much more.''',
#                     'code': '''# Writing to a file. 'w' mode overwrites the file if it exists.
# The 'with' statement automatically closes the file for you.
# with open("greeting.txt", "w") as file:
#     file.write("Hello, file world!")
# 
# Appending to a file. 'a' mode adds to the end of the file.
# with open("greeting.txt", "a") as file:
#     file.write("\\nThis is a new line.")
# 
# Reading from a file. 'r' mode is the default.
# with open("greeting.txt", "r") as file:
#     content = file.read()
#     print(content)'''
#                 }
#             ]
#         },
#         'quiz': [
#             {
#                 'question': 'What is the main benefit of using a function?',
#                 'options': [
#                     'To make the code run faster',
#                     'To make the code reusable and organized',
#                     'To store variables',
#                     'To handle errors'
#                 ],
#                 'correct': 1
#             },
#             {
#                 'question': 'A variable defined inside a function has what kind of scope?',
#                 'options': ['Global Scope', 'Universal Scope', 'Functional Scope', 'Local Scope'],
#                 'correct': 3
#             },
#             {
#                 'question': 'What is the purpose of a try...except block?',
#                 'options': [
#                     'To try code and see if it is efficient',
#                     'To handle potential errors gracefully',
#                     'To create a loop',
#                     'To define a function'
#                 ],
#                 'correct': 1
#             },
#             {
#                 'question': 'Which file mode adds content to the end of a file?',
#                 'options': ["'r'", "'w'", "'a'", "'x'"],
#                 'correct': 2
#             }
#         ],
#         'project': {
#             'name': 'Contact Book Application',
#             'description': 'Create a command-line contact book with menu options to add, search, and list contacts. Contacts should be stored in a text file and persist between runs.',
#             'requirements': [
#                 'Use functions for each menu option',
#                 'Store contacts in a dictionary in memory',
#                 'Save contacts to a file (CSV format recommended)',
#                 'Load contacts when program starts',
#                 'Handle FileNotFoundError gracefully',
#                 'Use a while loop for the main menu'
#             ]
#         }
#     },
#     3: {
#         'title': 'Module 3: Advanced Concepts and Tools',
#         'objective': 'To learn Object-Oriented Programming and leverage third-party libraries.',
#         'topics': [
#             'Object-Oriented Programming (classes and objects)',
#             'Installing packages with pip',
#             'Using third-party libraries (requests, BeautifulSoup)',
#             'Introduction to debugging',
#             'Introduction to Git'
#         ],
#         'instructional_content': {
#             'intro': 'This module introduces concepts and tools that are essential for building large-scale applications and working in a professional development environment. You will learn to think in objects, leverage the vast Python ecosystem, and use professional development tools.',
#             'sections': [
#                 {
#                     'title': 'A New Way of Thinking: Introduction to Object-Oriented Programming (OOP)',
#                     'content': '''So far, we have been writing code in a **procedural** style: a series of steps (often organized into functions) that operate on data. **Object-Oriented Programming (OOP)** is a different paradigm, or way of thinking about programming. It focuses on creating "objects" that bundle together both data and the functions that operate on that data.
# 
# The blueprint for an object is called a **class**. A class defines the properties (**attributes**) and behaviors (**methods**) that all objects of that type will have. An individual object created from a class is called an **instance**.
# 
# Let's use a simple analogy. A Car class is a blueprint. It defines that all cars will have attributes like color and max_speed, and methods (behaviors) like start_engine() and accelerate(). You can then create many individual car *objects* (instances) from this one blueprint: a red car, a blue car, etc., each with its own specific color but sharing the same fundamental behaviors.
# 
# OOP is a powerful way to model real-world entities, organize complex systems, and create code that is more modular and reusable.''',
#                     'code': '''# Define the 'Car' class (the blueprint).
# class Car:
    # The __init__ method is a special method called a constructor.
    # It runs when a new object is created to set up its initial attributes.
#     def __init__(self, color, max_speed):
#         self.color = color
#         self.max_speed = max_speed
#         self.current_speed = 0
#         self.is_engine_on = False
# 
    # A method (a function that belongs to the class).
#     def start_engine(self):
#         self.is_engine_on = True
#         print("Engine started.")
# 
#     def accelerate(self, amount):
#         if self.is_engine_on:
#             self.current_speed = min(self.current_speed + amount, self.max_speed)
#             print(f"Accelerating. Current speed: {self.current_speed} km/h.")
#         else:
#             print("Cannot accelerate, engine is off.")
# 
# Create two instances (objects) of the Car class.
# my_car = Car("Red", 200)
# friends_car = Car("Blue", 180)
# 
# Interact with the objects.
# print(f"My car is {my_car.color}.")
# my_car.start_engine()
# my_car.accelerate(50)'''
#                 },
#                 {
#                     'title': 'Leveraging the Ecosystem: Installing and Using Third-Party Libraries',
#                     'content': '''One of Python's most significant advantages is its vast collection of third-party libraries. These are toolkits created by the community that you can easily add to your projects. The standard tool for installing these packages is called **pip**, the Python Package Installer.
# 
# The main repository of Python packages is the Python Package Index (PyPI). You can search it for libraries to solve almost any problem. Let's say you want to make HTTP requests to get data from a website. A very popular library for this is requests.
# 
# To install it, you open your command line or terminal and run:
# ```
# pip install requests
# ```
# 
# Once installed, you can **import** it into your Python script and use its functionality.
# 
# Learning to find, install, and read the documentation for third-party libraries is a superpower. It allows you to stand on the shoulders of giants and build incredibly powerful applications quickly.''',
#                     'code': '''# Import the 'requests' library after installing it with pip.
# import requests
# 
# Use the library to make a GET request to a URL.
# response = requests.get("https://api.github.com")
# 
# The 'response' object contains the server's response.
# if response.status_code == 200:
#     print("Successfully connected to the GitHub API.")
#     print(response.json())  # .json() is a helpful method from the requests library.
# else:
#     print(f"Failed to connect. Status code: {response.status_code}")'''
#                 },
#                 {
#                     'title': 'The Professional\'s Toolkit: An Introduction to Debugging and Version Control (Git)',
#                     'content': '''Writing code is only part of a developer's job. Finding and fixing bugs (**debugging**) is another major part. While print() statements can help you see what your code is doing, a more systematic approach involves using a **debugger**. A debugger is a tool that lets you pause your program's execution at specific points (called breakpoints), inspect the values of variables at that moment, and step through your code line by line. Most modern code editors (like VS Code) have excellent built-in debuggers. Learning to use one will save you countless hours of frustration.
# 
# Another non-negotiable skill for any serious developer is **version control**. Version control is a system that records changes to a file or set of files over time so that you can recall specific versions later. It is like an unlimited "undo" button for your entire project. It also allows multiple developers to collaborate on the same codebase without overwriting each other's work.
# 
# The industry-standard version control system is **Git**. Platforms like GitHub, GitLab, and Bitbucket provide hosting for Git repositories, making it easy to store your code remotely and collaborate. Learning the basics of Git (git add, git commit, git push, git pull) is an essential step in your journey toward becoming a professional developer.''',
#                     'code': '''# Basic Git commands (run in terminal):
# 
# Initialize a new Git repository
# git init
# 
# Check the status of your repository
# git status
# 
# Add files to staging area
# git add filename.py
# or add all files
# git add .
# 
# Commit changes with a message
# git commit -m "Add new feature"
# 
# Push changes to remote repository
# git push origin main'''
#                 }
#             ]
#         },
#         'quiz': [
#             {
#                 'question': 'In OOP, what is the relationship between a class and an object?',
#                 'options': [
#                     'They are the same thing',
#                     'An object is a blueprint for a class',
#                     'A class is a blueprint for an object',
#                     'A class is a variable, an object is a function'
#                 ],
#                 'correct': 2
#             },
#             {
#                 'question': 'What tool is used to install Python packages from PyPI?',
#                 'options': ['python install', 'py', 'install', 'pip'],
#                 'correct': 3
#             },
#             {
#                 'question': 'What is the primary purpose of Git?',
#                 'options': [
#                     'To make code run faster',
#                     'To fix bugs automatically',
#                     'To track changes and enable collaboration',
#                     'To install libraries'
#                 ],
#                 'correct': 2
#             },
#             {
#                 'question': 'In a class, what is a function called?',
#                 'options': ['A method', 'An attribute', 'A parameter', 'An instance'],
#                 'correct': 0
#             }
#         ],
#         'project': {
#             'name': 'Simple Web Scraper',
#             'description': 'Build a web scraper that prompts for a URL, fetches the webpage, and extracts and displays the page title.',
#             'requirements': [
#                 'Use requests library to fetch webpages',
#                 'Use BeautifulSoup to parse HTML',
#                 'Extract the <title> tag content',
#                 'Handle network errors gracefully',
#                 'Use functions to organize code'
#             ]
#         }
#     }
# }


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Progress management functions are now imported from db_manager.py
# get_student_progress() and update_student_progress() are available


@app.route('/')
def index():
    """Home page."""
    # Check if student is logged in and get their current module
    current_module_id = 1
    student_name = session.get('student_name')

    if student_name:
        progress = get_student_progress(student_name)
        current_module_id = progress['current_module']

    # Get the current module data to display
    current_module = MODULES[current_module_id]

    return render_template('home.html',
                         current_module=current_module,
                         current_module_id=current_module_id,
                         student_name=student_name)


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
            if student_answer == question['correct_answer']:
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
            filename = secure_filename(f"{student_name}_module{module_id:03d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
            module_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'module{module_id:03d}')
            os.makedirs(module_dir, exist_ok=True)
            filepath = os.path.join(module_dir, filename)
            file.save(filepath)

            # Test submission - dynamically import the correct tester
            progress['modules'][module_id]['attempts'] += 1

            try:
                # Import tester module dynamically (e.g., module001_tester, module002_tester, etc.)
                tester_module_name = f'module{module_id:03d}_tester'
                tester_module = importlib.import_module(tester_module_name)
                test_result = tester_module.test_submission(filepath)
            except ModuleNotFoundError:
                test_result = {
                    'passed': False,
                    'score': '0/0 (0%)',
                    'tests': [],
                    'message': f'Tester for module {module_id} not found. Please contact administrator.'
                }
            except Exception as e:
                test_result = {
                    'passed': False,
                    'score': '0/0 (0%)',
                    'tests': [],
                    'message': f'Error running tests: {str(e)}'
                }

            # Update progress
            progress['modules'][module_id]['project_passed'] = test_result['passed']
            progress['modules'][module_id]['last_submission'] = datetime.now().isoformat()
            progress['modules'][module_id]['test_results'] = test_result

            if test_result['passed']:
                # Check if BOTH quiz and project are now passed
                quiz_passed = progress['modules'][module_id]['quiz_passed']
                project_passed = progress['modules'][module_id]['project_passed']

                if quiz_passed and project_passed:
                    # Unlock next module only when both requirements are met
                    total_modules = get_module_count()
                    if module_id < total_modules:
                        progress['current_module'] = module_id + 1
                        flash(f'Congratulations! Day {module_id} completed. Day {module_id + 1} unlocked!', 'success')
                    else:
                        progress['completed'] = True
                        progress['completed_at'] = datetime.now().isoformat()
                        flash('Congratulations! You have completed all 100 days of Python!', 'success')
                else:
                    flash(f'Project passed! Great work on the {MODULES[module_id]["project"]["name"]}!', 'success')
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
