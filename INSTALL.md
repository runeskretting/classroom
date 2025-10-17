# Installation and Usage Guide

## Prerequisites
- Python 3.7 or higher
- Git (to clone the repository)

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd classroom
```

### 2. Create Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages** (from `requirements.txt`):
- Flask
- requests
- beautifulsoup4

### 4. Verify Directory Structure
The application will auto-create these on first run, but you can create them manually:
```bash
mkdir -p data/submissions/module1
mkdir -p data/submissions/module2
mkdir -p data/submissions/module3
```

### 5. Run the Application
```bash
python app.py
```

**Quick start alternative** (handles venv creation automatically):
```bash
./run.sh
```

### 6. Access the Application
Open your browser to: **http://localhost:5000**

## Usage Flow

1. **Start**: Enter your name on the welcome page
2. **Learn**: Work through Module 1 content
3. **Quiz**: Complete the module quiz (need 75% to pass)
4. **Project**: Download project requirements, write your Python code
5. **Submit**: Upload your `.py` file for automated testing
6. **Progress**: Pass the project to unlock the next module
7. **Repeat**: Continue through Modules 2 and 3

## Notes

- Student progress is saved in `data/student_progress.json`
- Submissions are stored in `data/submissions/module{1,2,3}/`
- Maximum file size: 1MB
- Only `.py` files accepted
- Each project must pass automated tests to proceed

## Troubleshooting

**Port already in use**: Change port in `app.py` line 436:
```python
app.run(debug=True, port=5001)  # Change to different port
```

**Module unlocked unexpectedly**: Delete `data/student_progress.json` to reset all progress.

**Permission denied on run.sh**: Make the script executable:
```bash
chmod +x run.sh
```

**ModuleNotFoundError**: Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

## System Requirements

- Python 3.7 or higher
- 50MB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for downloading dependencies)

## Development Mode

The application runs in debug mode by default:
- Auto-reloads on code changes
- Detailed error messages
- Interactive debugger

For production, edit `app.py` line 436:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Getting Help

- Read `README.md` for detailed documentation
- Check `CLAUDE.md` for architecture details
- Review Flask logs in the terminal for errors
- Verify Python version: `python --version`
