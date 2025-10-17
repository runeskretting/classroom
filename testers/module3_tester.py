"""
Module 3 Tester: Web Scraper
Tests student submissions for the Module 3 capstone project.
"""

import subprocess
import sys
import os
import tempfile
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time


class TestHTTPHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for testing."""

    def do_GET(self):
        """Handle GET requests."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page for Web Scraper</title>
        </head>
        <body>
            <h1>Welcome to the Test Page</h1>
            <p>This is a test page for the Python Classroom web scraper project.</p>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())

    def log_message(self, format, *args):
        """Suppress log messages."""
        pass


class Module3Tester:
    def __init__(self, submission_path):
        self.submission_path = submission_path
        self.test_results = []
        self.passed = False
        self.test_server = None
        self.test_port = 8765

    def start_test_server(self):
        """Start a test HTTP server."""
        try:
            self.test_server = HTTPServer(('localhost', self.test_port), TestHTTPHandler)
            server_thread = threading.Thread(target=self.test_server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            time.sleep(0.5)  # Give server time to start
            return True
        except Exception as e:
            return False

    def stop_test_server(self):
        """Stop the test HTTP server."""
        if self.test_server:
            self.test_server.shutdown()

    def test_imports(self):
        """Test if the code imports required libraries."""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            checks = {
                'requests library': 'import requests' in code,
                'BeautifulSoup': 'from bs4 import BeautifulSoup' in code or 'import bs4' in code
            }

            for check_name, passed in checks.items():
                self.test_results.append({
                    'test': f'Imports {check_name}',
                    'passed': passed,
                    'message': f'Code {"imports" if passed else "does not import"} {check_name}'
                })

            return all(checks.values())

        except Exception as e:
            self.test_results.append({
                'test': 'Import check',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_code_structure(self):
        """Test if the code contains necessary structures."""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            checks = {
                'function definitions': 'def ' in code,
                'try/except blocks': 'try:' in code and 'except' in code,
                'requests.get()': 'requests.get(' in code,
                'soup object creation': 'BeautifulSoup(' in code or 'bs4.BeautifulSoup(' in code,
                'input() for URL': 'input(' in code
            }

            for check_name, passed in checks.items():
                self.test_results.append({
                    'test': f'Contains {check_name}',
                    'passed': passed,
                    'message': f'Code {"contains" if passed else "missing"} {check_name}'
                })

            return sum(checks.values()) >= 4  # At least 4 out of 5

        except Exception as e:
            self.test_results.append({
                'test': 'Code structure check',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_function_definitions(self):
        """Test if functions are properly defined."""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            # Look for function definitions
            has_get_title_func = any(pattern in code for pattern in [
                'def get_page_title',
                'def get_title',
                'def scrape',
                'def fetch_title'
            ])

            has_main_func = 'def main(' in code or 'if __name__' in code

            if has_get_title_func:
                self.test_results.append({
                    'test': 'Title extraction function',
                    'passed': True,
                    'message': 'Has function for extracting page title'
                })
            else:
                self.test_results.append({
                    'test': 'Title extraction function',
                    'passed': False,
                    'message': 'Missing function for title extraction'
                })

            if has_main_func:
                self.test_results.append({
                    'test': 'Main function',
                    'passed': True,
                    'message': 'Has main function or entry point'
                })
            else:
                self.test_results.append({
                    'test': 'Main function',
                    'passed': False,
                    'message': 'Missing main function or __name__ check'
                })

            return has_get_title_func

        except Exception as e:
            self.test_results.append({
                'test': 'Function definitions',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_scraping_functionality(self):
        """Test the actual scraping functionality."""
        try:
            # Start test server
            if not self.start_test_server():
                self.test_results.append({
                    'test': 'Web scraping functionality',
                    'passed': False,
                    'message': 'Could not start test server'
                })
                return False

            test_url = f"http://localhost:{self.test_port}/"

            # Run the scraper with the test URL
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_url + "\n",
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout

            # Check if the title was extracted
            if 'Test Page for Web Scraper' in output:
                self.test_results.append({
                    'test': 'Title extraction',
                    'passed': True,
                    'message': 'Successfully extracts page title'
                })
                success = True
            else:
                self.test_results.append({
                    'test': 'Title extraction',
                    'passed': False,
                    'message': f'Did not extract correct title. Output: {output[:200]}'
                })
                success = False

            # Check if program runs without errors
            if result.returncode == 0:
                self.test_results.append({
                    'test': 'Program execution',
                    'passed': True,
                    'message': 'Program runs without errors'
                })
            else:
                self.test_results.append({
                    'test': 'Program execution',
                    'passed': False,
                    'message': f'Program error: {result.stderr[:200]}'
                })
                success = False

            return success

        except subprocess.TimeoutExpired:
            self.test_results.append({
                'test': 'Web scraping functionality',
                'passed': False,
                'message': 'Program timed out'
            })
            return False
        except Exception as e:
            self.test_results.append({
                'test': 'Web scraping functionality',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False
        finally:
            self.stop_test_server()

    def test_error_handling(self):
        """Test error handling with invalid URL."""
        try:
            # Test with invalid URL
            invalid_url = "http://this-domain-definitely-does-not-exist-12345.com"

            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=invalid_url + "\n",
                capture_output=True,
                text=True,
                timeout=15
            )

            # Program should handle the error gracefully (not crash)
            if result.returncode == 0:
                self.test_results.append({
                    'test': 'Error handling',
                    'passed': True,
                    'message': 'Handles network errors gracefully'
                })
                return True
            else:
                # Check if error message is informative
                if 'error' in result.stdout.lower() or 'error' in result.stderr.lower():
                    self.test_results.append({
                        'test': 'Error handling',
                        'passed': True,
                        'message': 'Provides error feedback'
                    })
                    return True
                else:
                    self.test_results.append({
                        'test': 'Error handling',
                        'passed': False,
                        'message': 'Does not handle errors properly'
                    })
                    return False

        except subprocess.TimeoutExpired:
            self.test_results.append({
                'test': 'Error handling',
                'passed': False,
                'message': 'Program hangs on error'
            })
            return False
        except Exception as e:
            self.test_results.append({
                'test': 'Error handling',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def run_all_tests(self):
        """Run all tests and return results."""
        try:
            imports_ok = self.test_imports()
            structure_ok = self.test_code_structure()
            functions_ok = self.test_function_definitions()
            scraping_ok = self.test_scraping_functionality()
            error_ok = self.test_error_handling()

            # Calculate overall pass/fail
            passed_count = sum(1 for result in self.test_results if result['passed'])
            total_count = len(self.test_results)

            self.passed = passed_count >= total_count * 0.70  # 70% pass rate

            return {
                'passed': self.passed,
                'score': f'{passed_count}/{total_count}',
                'percentage': int((passed_count / total_count) * 100),
                'tests': self.test_results,
                'message': 'All tests passed! Your web scraper works correctly.' if self.passed
                          else 'Some tests failed. Please review the feedback and try again.'
            }

        finally:
            self.stop_test_server()


def test_submission(submission_path):
    """Main function to test a submission."""
    if not os.path.exists(submission_path):
        return {
            'passed': False,
            'score': '0/0',
            'percentage': 0,
            'tests': [],
            'message': 'Submission file not found'
        }

    tester = Module3Tester(submission_path)
    return tester.run_all_tests()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python module3_tester.py <submission_path>")
        sys.exit(1)

    result = test_submission(sys.argv[1])
    print(f"\nTest Results:")
    print(f"Score: {result['score']} ({result['percentage']}%)")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}\n")

    for test in result['tests']:
        status = '✓' if test['passed'] else '✗'
        print(f"{status} {test['test']}: {test['message']}")

    print(f"\n{result['message']}")
