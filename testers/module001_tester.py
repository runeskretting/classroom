"""
Module 1 Tester: Day 1 - Your First Program: Hello, World!
Tests student submissions for basic print() statements and comments.
"""

import ast
import subprocess
import sys
import os


class Module001Tester:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tests = []
        self.passed = False

    def test_file_exists(self):
        """Test that the file exists and is readable."""
        try:
            with open(self.filepath, 'r') as f:
                self.code_content = f.read()
            return {
                'name': 'File exists and is readable',
                'passed': True,
                'message': 'Successfully loaded the Python file.'
            }
        except Exception as e:
            return {
                'name': 'File exists and is readable',
                'passed': False,
                'message': f'Could not read file: {str(e)}'
            }

    def test_has_comments(self):
        """Test that the code contains at least 2 comments."""
        try:
            comment_count = self.code_content.count('#')

            if comment_count >= 2:
                return {
                    'name': 'Code contains at least 2 comments',
                    'passed': True,
                    'message': f'Found {comment_count} comments. Good documentation!'
                }
            else:
                return {
                    'name': 'Code contains at least 2 comments',
                    'passed': False,
                    'message': f'Found only {comment_count} comment(s). Need at least 2.'
                }
        except Exception as e:
            return {
                'name': 'Code contains at least 2 comments',
                'passed': False,
                'message': f'Error checking comments: {str(e)}'
            }

    def test_has_print_statements(self):
        """Test that the code contains at least 3 print() statements."""
        try:
            tree = ast.parse(self.code_content)
            print_count = sum(1 for node in ast.walk(tree)
                            if isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)
                            and node.func.id == 'print')

            if print_count >= 3:
                return {
                    'name': 'Code contains at least 3 print statements',
                    'passed': True,
                    'message': f'Found {print_count} print() statements. Well done!'
                }
            else:
                return {
                    'name': 'Code contains at least 3 print statements',
                    'passed': False,
                    'message': f'Found only {print_count} print() statement(s). Need at least 3.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code contains at least 3 print statements',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code contains at least 3 print statements',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_code_runs_without_errors(self):
        """Test that the code executes without errors."""
        try:
            result = subprocess.run(
                [sys.executable, self.filepath],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                self.output = result.stdout
                return {
                    'name': 'Code runs without errors',
                    'passed': True,
                    'message': 'Program executed successfully!'
                }
            else:
                return {
                    'name': 'Code runs without errors',
                    'passed': False,
                    'message': f'Program error: {result.stderr}'
                }
        except subprocess.TimeoutExpired:
            return {
                'name': 'Code runs without errors',
                'passed': False,
                'message': 'Program took too long to run (timeout).'
            }
        except Exception as e:
            return {
                'name': 'Code runs without errors',
                'passed': False,
                'message': f'Error running program: {str(e)}'
            }

    def test_produces_output(self):
        """Test that the code produces some output."""
        try:
            if hasattr(self, 'output') and self.output.strip():
                lines = self.output.strip().split('\n')
                if len(lines) >= 3:
                    return {
                        'name': 'Program produces at least 3 lines of output',
                        'passed': True,
                        'message': f'Program output has {len(lines)} lines. Great!'
                    }
                else:
                    return {
                        'name': 'Program produces at least 3 lines of output',
                        'passed': False,
                        'message': f'Program output has only {len(lines)} line(s). Need at least 3.'
                    }
            else:
                return {
                    'name': 'Program produces at least 3 lines of output',
                    'passed': False,
                    'message': 'Program produced no output.'
                }
        except Exception as e:
            return {
                'name': 'Program produces at least 3 lines of output',
                'passed': False,
                'message': f'Error checking output: {str(e)}'
            }

    def run_all_tests(self):
        """Run all tests and return results."""
        test_methods = [
            self.test_file_exists,
            self.test_has_comments,
            self.test_has_print_statements,
            self.test_code_runs_without_errors,
            self.test_produces_output
        ]

        for test_method in test_methods:
            result = test_method()
            self.tests.append(result)
            # If a critical test fails, stop testing
            if not result['passed'] and test_method in [self.test_file_exists, self.test_code_runs_without_errors]:
                break

        passed_count = sum(1 for test in self.tests if test['passed'])
        total_count = len(self.tests)

        self.passed = passed_count == total_count

        return {
            'passed': self.passed,
            'score': f'{passed_count}/{total_count} ({int(passed_count/total_count*100)}%)',
            'tests': self.tests,
            'message': 'All tests passed! Great job!' if self.passed else 'Some tests failed. Review the feedback and try again.'
        }


def test_submission(filepath):
    """Main entry point for testing a submission."""
    tester = Module001Tester(filepath)
    return tester.run_all_tests()


if __name__ == '__main__':
    # For testing the tester itself
    if len(sys.argv) > 1:
        result = test_submission(sys.argv[1])
        print(f"Passed: {result['passed']}")
        print(f"Score: {result['score']}")
        print(f"Message: {result['message']}")
        for test in result['tests']:
            status = '✓' if test['passed'] else '✗'
            print(f"{status} {test['name']}: {test['message']}")
