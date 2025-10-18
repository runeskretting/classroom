"""
Module 2 Tester: Day 2 - Strings and Manipulation
Tests student submissions for string operations: concatenation, len(), indexing, and slicing.
"""

import ast
import subprocess
import sys
import os


class Module002Tester:
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
        """Test that the code contains at least 3 comments."""
        try:
            comment_count = self.code_content.count('#')

            if comment_count >= 3:
                return {
                    'name': 'Code contains at least 3 comments',
                    'passed': True,
                    'message': f'Found {comment_count} comments. Good documentation!'
                }
            else:
                return {
                    'name': 'Code contains at least 3 comments',
                    'passed': False,
                    'message': f'Found only {comment_count} comment(s). Need at least 3.'
                }
        except Exception as e:
            return {
                'name': 'Code contains at least 3 comments',
                'passed': False,
                'message': f'Error checking comments: {str(e)}'
            }

    def test_uses_input(self):
        """Test that the code uses input() to get user input."""
        try:
            tree = ast.parse(self.code_content)
            input_count = sum(1 for node in ast.walk(tree)
                            if isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)
                            and node.func.id == 'input')

            if input_count >= 2:
                return {
                    'name': 'Code uses input() at least 2 times',
                    'passed': True,
                    'message': f'Found {input_count} input() calls. Great!'
                }
            else:
                return {
                    'name': 'Code uses input() at least 2 times',
                    'passed': False,
                    'message': f'Found only {input_count} input() call(s). Need at least 2 to get user strings.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses input() at least 2 times',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses input() at least 2 times',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_len_function(self):
        """Test that the code uses the len() function."""
        try:
            tree = ast.parse(self.code_content)
            len_count = sum(1 for node in ast.walk(tree)
                          if isinstance(node, ast.Call)
                          and isinstance(node.func, ast.Name)
                          and node.func.id == 'len')

            if len_count >= 1:
                return {
                    'name': 'Code uses len() function',
                    'passed': True,
                    'message': f'Found {len_count} len() call(s). Well done!'
                }
            else:
                return {
                    'name': 'Code uses len() function',
                    'passed': False,
                    'message': 'No len() function found. You need to use len() to get string length.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses len() function',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses len() function',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_concatenation(self):
        """Test that the code uses string concatenation with + operator."""
        try:
            tree = ast.parse(self.code_content)
            # Look for BinOp with Add operator (the + operator)
            concat_count = sum(1 for node in ast.walk(tree)
                             if isinstance(node, ast.BinOp)
                             and isinstance(node.op, ast.Add))

            if concat_count >= 1:
                return {
                    'name': 'Code uses string concatenation (+)',
                    'passed': True,
                    'message': f'Found {concat_count} concatenation(s). Excellent!'
                }
            else:
                return {
                    'name': 'Code uses string concatenation (+)',
                    'passed': False,
                    'message': 'No string concatenation found. Use + to combine strings.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses string concatenation (+)',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses string concatenation (+)',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_indexing(self):
        """Test that the code uses string indexing to access characters."""
        try:
            tree = ast.parse(self.code_content)
            # Look for Subscript nodes (string[index])
            # We need to filter out slices, so check that the slice is just an Index or Constant
            indexing_count = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.Subscript):
                    # In Python 3.9+, simple indexing uses node.slice directly
                    # In older versions, it's wrapped in ast.Index
                    if isinstance(node.slice, (ast.Constant, ast.Name, ast.UnaryOp)):
                        indexing_count += 1
                    elif isinstance(node.slice, ast.Index):  # Python 3.8 and earlier
                        indexing_count += 1

            if indexing_count >= 1:
                return {
                    'name': 'Code uses string indexing',
                    'passed': True,
                    'message': f'Found {indexing_count} indexing operation(s). Great!'
                }
            else:
                return {
                    'name': 'Code uses string indexing',
                    'passed': False,
                    'message': 'No string indexing found. Use string[index] to access characters.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses string indexing',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses string indexing',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_slicing(self):
        """Test that the code uses string slicing."""
        try:
            tree = ast.parse(self.code_content)
            # Look for Subscript nodes with Slice
            slicing_count = sum(1 for node in ast.walk(tree)
                              if isinstance(node, ast.Subscript)
                              and isinstance(node.slice, ast.Slice))

            if slicing_count >= 1:
                return {
                    'name': 'Code uses string slicing',
                    'passed': True,
                    'message': f'Found {slicing_count} slicing operation(s). Excellent!'
                }
            else:
                return {
                    'name': 'Code uses string slicing',
                    'passed': False,
                    'message': 'No string slicing found. Use string[start:end] to extract substrings.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses string slicing',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses string slicing',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_code_runs_without_errors(self):
        """Test that the code executes without errors."""
        try:
            # Provide test input (2 strings as required)
            test_input = "Alice\nBoston\n"

            result = subprocess.run(
                [sys.executable, self.filepath],
                input=test_input,
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
        """Test that the code produces meaningful output."""
        try:
            if hasattr(self, 'output') and self.output.strip():
                lines = self.output.strip().split('\n')
                # Should have multiple lines showing different operations
                if len(lines) >= 5:
                    return {
                        'name': 'Program produces meaningful output (5+ lines)',
                        'passed': True,
                        'message': f'Program output has {len(lines)} lines showing string operations. Great!'
                    }
                else:
                    return {
                        'name': 'Program produces meaningful output (5+ lines)',
                        'passed': False,
                        'message': f'Program output has only {len(lines)} line(s). Show more string operations (concatenation, len, indexing, slicing).'
                    }
            else:
                return {
                    'name': 'Program produces meaningful output (5+ lines)',
                    'passed': False,
                    'message': 'Program produced no output.'
                }
        except Exception as e:
            return {
                'name': 'Program produces meaningful output (5+ lines)',
                'passed': False,
                'message': f'Error checking output: {str(e)}'
            }

    def run_all_tests(self):
        """Run all tests and return results."""
        test_methods = [
            self.test_file_exists,
            self.test_has_comments,
            self.test_uses_input,
            self.test_uses_len_function,
            self.test_uses_concatenation,
            self.test_uses_indexing,
            self.test_uses_slicing,
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

        # Require at least 7/9 tests to pass (approximately 75%)
        self.passed = passed_count >= 7

        return {
            'passed': self.passed,
            'score': f'{passed_count}/{total_count} ({int(passed_count/total_count*100)}%)',
            'tests': self.tests,
            'message': 'All tests passed! Great job!' if passed_count == total_count else
                      'Good work! You passed the requirements.' if self.passed else
                      'Some tests failed. Review the feedback and try again.'
        }


def test_submission(filepath):
    """Main entry point for testing a submission."""
    tester = Module002Tester(filepath)
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
