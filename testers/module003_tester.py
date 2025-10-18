"""
Module 3 Tester: Day 3 - Variables and Data Types
Tests student submissions for variables, data types, type conversion, and type checking.
"""

import ast
import subprocess
import sys
import os


class Module003Tester:
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
        """Test that the code contains at least 5 comments."""
        try:
            comment_count = self.code_content.count('#')

            if comment_count >= 5:
                return {
                    'name': 'Code contains at least 5 comments',
                    'passed': True,
                    'message': f'Found {comment_count} comments. Excellent documentation!'
                }
            else:
                return {
                    'name': 'Code contains at least 5 comments',
                    'passed': False,
                    'message': f'Found only {comment_count} comment(s). Need at least 5.'
                }
        except Exception as e:
            return {
                'name': 'Code contains at least 5 comments',
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

            if input_count >= 3:
                return {
                    'name': 'Code uses input() at least 3 times',
                    'passed': True,
                    'message': f'Found {input_count} input() calls. Great!'
                }
            else:
                return {
                    'name': 'Code uses input() at least 3 times',
                    'passed': False,
                    'message': f'Found only {input_count} input() call(s). Need at least 3 (name, age, height, etc.).'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses input() at least 3 times',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses input() at least 3 times',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_type_conversion(self):
        """Test that the code uses type conversion functions (int, float, str)."""
        try:
            tree = ast.parse(self.code_content)
            conversion_functions = {'int', 'float', 'str'}
            found_conversions = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in conversion_functions:
                        found_conversions.add(node.func.id)

            if len(found_conversions) >= 2:
                return {
                    'name': 'Code uses at least 2 type conversion functions',
                    'passed': True,
                    'message': f'Found conversions: {", ".join(found_conversions)}. Excellent!'
                }
            else:
                return {
                    'name': 'Code uses at least 2 type conversion functions',
                    'passed': False,
                    'message': f'Found only {len(found_conversions)} type conversion(s). Use int(), float(), and/or str().'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses at least 2 type conversion functions',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses at least 2 type conversion functions',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_type_function(self):
        """Test that the code uses the type() function."""
        try:
            tree = ast.parse(self.code_content)
            type_count = sum(1 for node in ast.walk(tree)
                           if isinstance(node, ast.Call)
                           and isinstance(node.func, ast.Name)
                           and node.func.id == 'type')

            if type_count >= 2:
                return {
                    'name': 'Code uses type() function at least 2 times',
                    'passed': True,
                    'message': f'Found {type_count} type() call(s). Great!'
                }
            else:
                return {
                    'name': 'Code uses type() function at least 2 times',
                    'passed': False,
                    'message': f'Found only {type_count} type() call(s). Use type() to display data types of at least 2 variables.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses type() function at least 2 times',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses type() function at least 2 times',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_has_proper_variable_names(self):
        """Test that the code uses descriptive variable names with snake_case."""
        try:
            tree = ast.parse(self.code_content)
            variable_names = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variable_names.append(target.id)

            # Filter out single-letter variables and check for snake_case patterns
            descriptive_vars = [v for v in variable_names if len(v) > 2 and '_' in v]

            if len(descriptive_vars) >= 3:
                return {
                    'name': 'Code uses descriptive variable names (snake_case)',
                    'passed': True,
                    'message': f'Found {len(descriptive_vars)} descriptive variables using snake_case. Good practice!'
                }
            else:
                return {
                    'name': 'Code uses descriptive variable names (snake_case)',
                    'passed': False,
                    'message': f'Found only {len(descriptive_vars)} descriptive variable(s). Use snake_case names like user_age, birth_year, etc.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses descriptive variable names (snake_case)',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses descriptive variable names (snake_case)',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_performs_calculations(self):
        """Test that the code performs calculations (addition, subtraction, etc.)."""
        try:
            tree = ast.parse(self.code_content)
            # Look for BinOp operations (arithmetic operations)
            calc_count = sum(1 for node in ast.walk(tree)
                           if isinstance(node, ast.BinOp))

            if calc_count >= 2:
                return {
                    'name': 'Code performs calculations',
                    'passed': True,
                    'message': f'Found {calc_count} calculation(s). Excellent!'
                }
            else:
                return {
                    'name': 'Code performs calculations',
                    'passed': False,
                    'message': f'Found only {calc_count} calculation(s). Calculate age in 5 years and birth year.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code performs calculations',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code performs calculations',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_code_runs_without_errors(self):
        """Test that the code executes without errors."""
        try:
            # Provide test input (name, age, height, student status)
            test_input = "Alice\n25\n1.65\nyes\n"

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
                output_lower = self.output.lower()
                lines = self.output.strip().split('\n')

                # Check for key elements in output
                has_name_output = 'alice' in output_lower or 'name' in output_lower
                has_age_output = '25' in self.output or '30' in self.output  # current age or future age
                has_type_output = 'class' in output_lower or 'type' in output_lower

                checks_passed = sum([has_name_output, has_age_output, has_type_output])

                if checks_passed >= 2 and len(lines) >= 8:
                    return {
                        'name': 'Program produces comprehensive output',
                        'passed': True,
                        'message': f'Program output includes personal info, calculations, and type information. Great job!'
                    }
                else:
                    return {
                        'name': 'Program produces comprehensive output',
                        'passed': False,
                        'message': f'Output needs improvement. Include personal summary, calculations, and type() results. Found {len(lines)} lines, need at least 8.'
                    }
            else:
                return {
                    'name': 'Program produces comprehensive output',
                    'passed': False,
                    'message': 'Program produced no output.'
                }
        except Exception as e:
            return {
                'name': 'Program produces comprehensive output',
                'passed': False,
                'message': f'Error checking output: {str(e)}'
            }

    def run_all_tests(self):
        """Run all tests and return results."""
        test_methods = [
            self.test_file_exists,
            self.test_has_comments,
            self.test_uses_input,
            self.test_uses_type_conversion,
            self.test_uses_type_function,
            self.test_has_proper_variable_names,
            self.test_performs_calculations,
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
            'message': 'All tests passed! Excellent work!' if passed_count == total_count else
                      'Good work! You passed the requirements.' if self.passed else
                      'Some tests failed. Review the feedback and try again.'
        }


def test_submission(filepath):
    """Main entry point for testing a submission."""
    tester = Module003Tester(filepath)
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
