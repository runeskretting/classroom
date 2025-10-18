"""
Module 5 Tester: Day 5 - Type Casting and f-Strings
Tests student submissions for the Tip Calculator project.
"""

import ast
import subprocess
import sys
import os
import re


class Module005Tester:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tests = []
        self.passed = False
        self.output = ""

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
                    'message': f'Found {comment_count} comments. Great documentation!'
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
        """Test that the code uses input() at least 3 times."""
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
                    'message': f'Found only {input_count} input() call(s). Need 3 inputs: bill, tip %, and people.'
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
        """Test that the code uses type conversion functions."""
        try:
            tree = ast.parse(self.code_content)
            conversions = {'int': 0, 'float': 0, 'str': 0}

            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in conversions:
                        conversions[node.func.id] += 1

            # Need at least int() and float()
            has_int = conversions['int'] > 0
            has_float = conversions['float'] > 0
            total_conversions = sum(conversions.values())

            if has_int and has_float and total_conversions >= 3:
                return {
                    'name': 'Code uses type conversion functions',
                    'passed': True,
                    'message': f'Found type conversions: int={conversions["int"]}, float={conversions["float"]}, str={conversions["str"]}. Excellent!'
                }
            else:
                return {
                    'name': 'Code uses type conversion functions',
                    'passed': False,
                    'message': f'Need both int() and float() conversions. Found: int={conversions["int"]}, float={conversions["float"]}'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses type conversion functions',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses type conversion functions',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_fstrings(self):
        """Test that the code uses f-strings for formatting."""
        try:
            tree = ast.parse(self.code_content)
            fstring_count = sum(1 for node in ast.walk(tree)
                              if isinstance(node, ast.JoinedStr))

            if fstring_count >= 3:
                return {
                    'name': 'Code uses f-strings for formatting',
                    'passed': True,
                    'message': f'Found {fstring_count} f-string(s). Great modern Python!'
                }
            else:
                return {
                    'name': 'Code uses f-strings for formatting',
                    'passed': False,
                    'message': f'Found only {fstring_count} f-string(s). Use f-strings (f"text {variable}") for output. Need at least 3.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses f-strings for formatting',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses f-strings for formatting',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_code_runs_without_errors(self):
        """Test that the code executes without errors."""
        try:
            # Provide test input: bill=100, tip=15%, people=4
            test_input = "100\n15\n4\n"

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

    def test_calculates_tip_correctly(self):
        """Test that the program calculates tip amount correctly."""
        try:
            if not hasattr(self, 'output'):
                return {
                    'name': 'Calculates tip correctly',
                    'passed': False,
                    'message': 'Cannot test - program did not run.'
                }

            # For input: bill=100, tip=15%, people=4
            # Expected: tip = 15.00, total = 115.00, per person = 28.75
            output_lower = self.output.lower()

            # Look for tip amount (should be $15.00 or 15.00)
            has_tip = re.search(r'15\.0+', self.output)

            # Look for total (should be $115.00 or 115.00)
            has_total = re.search(r'115\.0+', self.output)

            # Look for per person (should be $28.75)
            has_per_person = re.search(r'28\.75', self.output)

            if has_tip and has_total and has_per_person:
                return {
                    'name': 'Calculates tip correctly',
                    'passed': True,
                    'message': 'Tip calculation is correct! Found tip=$15.00, total=$115.00, per person=$28.75'
                }
            else:
                missing = []
                if not has_tip:
                    missing.append('tip amount ($15.00)')
                if not has_total:
                    missing.append('total ($115.00)')
                if not has_per_person:
                    missing.append('per person amount ($28.75)')

                return {
                    'name': 'Calculates tip correctly',
                    'passed': False,
                    'message': f'Calculation error. Missing or incorrect: {", ".join(missing)}. Check your math!'
                }
        except Exception as e:
            return {
                'name': 'Calculates tip correctly',
                'passed': False,
                'message': f'Error checking calculations: {str(e)}'
            }

    def test_formats_money_properly(self):
        """Test that money values are formatted with 2 decimal places."""
        try:
            if not hasattr(self, 'output'):
                return {
                    'name': 'Formats money with 2 decimal places',
                    'passed': False,
                    'message': 'Cannot test - program did not run.'
                }

            # Look for properly formatted money (X.XX pattern)
            money_patterns = re.findall(r'\$?\d+\.\d{2}', self.output)

            if len(money_patterns) >= 3:
                return {
                    'name': 'Formats money with 2 decimal places',
                    'passed': True,
                    'message': f'Found {len(money_patterns)} properly formatted money values. Great formatting!'
                }
            else:
                return {
                    'name': 'Formats money with 2 decimal places',
                    'passed': False,
                    'message': f'Found only {len(money_patterns)} properly formatted money value(s). Use f-string formatting like {{price:.2f}} for 2 decimal places.'
                }
        except Exception as e:
            return {
                'name': 'Formats money with 2 decimal places',
                'passed': False,
                'message': f'Error checking formatting: {str(e)}'
            }

    def test_displays_comprehensive_output(self):
        """Test that the program displays all required information."""
        try:
            if not hasattr(self, 'output') or not self.output.strip():
                return {
                    'name': 'Displays comprehensive output',
                    'passed': False,
                    'message': 'Program produced no output.'
                }

            output_lower = self.output.lower()

            # Check for required elements in output
            has_bill = 'bill' in output_lower or '100' in self.output
            has_tip_label = 'tip' in output_lower
            has_total_label = 'total' in output_lower
            has_person_info = 'person' in output_lower or 'each' in output_lower

            checks_passed = sum([has_bill, has_tip_label, has_total_label, has_person_info])

            if checks_passed >= 3:
                return {
                    'name': 'Displays comprehensive output',
                    'passed': True,
                    'message': 'Output includes all required information. Excellent!'
                }
            else:
                missing = []
                if not has_bill:
                    missing.append('original bill')
                if not has_tip_label:
                    missing.append('tip amount')
                if not has_total_label:
                    missing.append('total')
                if not has_person_info:
                    missing.append('per person amount')

                return {
                    'name': 'Displays comprehensive output',
                    'passed': False,
                    'message': f'Output missing: {", ".join(missing)}. Show bill, tip, total, and per person amount.'
                }
        except Exception as e:
            return {
                'name': 'Displays comprehensive output',
                'passed': False,
                'message': f'Error checking output: {str(e)}'
            }

    def test_handles_different_inputs(self):
        """Test that the program works with different input values."""
        try:
            # Test with different values: bill=50.75, tip=20%, people=2
            test_input = "50.75\n20\n2\n"

            result = subprocess.run(
                [sys.executable, self.filepath],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                output = result.stdout

                # Expected: tip = 10.15, total = 60.90, per person = 30.45
                # Allow for small rounding differences
                has_reasonable_output = (
                    '10.15' in output or '10.2' in output or  # tip
                    '60.90' in output or '60.9' in output or  # total
                    '30.45' in output or '30.5' in output      # per person
                )

                if has_reasonable_output:
                    return {
                        'name': 'Handles different input values',
                        'passed': True,
                        'message': 'Program correctly handles different inputs!'
                    }
                else:
                    return {
                        'name': 'Handles different input values',
                        'passed': False,
                        'message': 'Program runs but calculations seem incorrect for different inputs. Verify your formulas.'
                    }
            else:
                return {
                    'name': 'Handles different input values',
                    'passed': False,
                    'message': f'Program failed with different inputs: {result.stderr}'
                }
        except subprocess.TimeoutExpired:
            return {
                'name': 'Handles different input values',
                'passed': False,
                'message': 'Program timeout with different inputs.'
            }
        except Exception as e:
            return {
                'name': 'Handles different input values',
                'passed': False,
                'message': f'Error testing with different inputs: {str(e)}'
            }

    def run_all_tests(self):
        """Run all tests and return results."""
        test_methods = [
            self.test_file_exists,
            self.test_has_comments,
            self.test_uses_input,
            self.test_uses_type_conversion,
            self.test_uses_fstrings,
            self.test_code_runs_without_errors,
            self.test_calculates_tip_correctly,
            self.test_formats_money_properly,
            self.test_displays_comprehensive_output,
            self.test_handles_different_inputs
        ]

        for test_method in test_methods:
            result = test_method()
            self.tests.append(result)
            # If a critical test fails, stop testing
            if not result['passed'] and test_method in [self.test_file_exists, self.test_code_runs_without_errors]:
                break

        passed_count = sum(1 for test in self.tests if test['passed'])
        total_count = len(self.tests)

        # Require at least 7/10 tests to pass (70%)
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
    tester = Module005Tester(filepath)
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
