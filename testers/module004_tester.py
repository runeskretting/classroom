"""
Module 4 Tester: Day 4 - Operators and Expressions
Tests student submissions for arithmetic, comparison, logical, and assignment operators.
"""

import ast
import subprocess
import sys
import os


class Module004Tester:
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
                    'message': f'Found only {input_count} input() call(s). Need at least 2 to get two numbers.'
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

    def test_uses_arithmetic_operators(self):
        """Test that the code uses multiple arithmetic operators."""
        try:
            tree = ast.parse(self.code_content)
            operators_found = set()

            # Look for binary operations
            for node in ast.walk(tree):
                if isinstance(node, ast.BinOp):
                    op_type = type(node.op).__name__
                    operators_found.add(op_type)

            # Check for various operators: Add, Sub, Mult, Div, FloorDiv, Mod, Pow
            required_operators = {'Add', 'Sub', 'Mult', 'Div'}
            found_required = operators_found & required_operators

            if len(found_required) >= 4:
                return {
                    'name': 'Code uses multiple arithmetic operators',
                    'passed': True,
                    'message': f'Found operators: {", ".join(operators_found)}. Excellent!'
                }
            else:
                return {
                    'name': 'Code uses multiple arithmetic operators',
                    'passed': False,
                    'message': f'Found only {len(found_required)} basic operators. Use +, -, *, / and more.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses multiple arithmetic operators',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses multiple arithmetic operators',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_comparison_operators(self):
        """Test that the code uses comparison operators."""
        try:
            tree = ast.parse(self.code_content)
            comparison_count = 0

            for node in ast.walk(tree):
                if isinstance(node, ast.Compare):
                    comparison_count += 1

            if comparison_count >= 2:
                return {
                    'name': 'Code uses comparison operators',
                    'passed': True,
                    'message': f'Found {comparison_count} comparison(s). Great!'
                }
            else:
                return {
                    'name': 'Code uses comparison operators',
                    'passed': False,
                    'message': f'Found only {comparison_count} comparison(s). Use operators like >, <, ==, etc.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses comparison operators',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses comparison operators',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_modulus_operator(self):
        """Test that the code uses the modulus (%) operator."""
        try:
            tree = ast.parse(self.code_content)
            mod_count = sum(1 for node in ast.walk(tree)
                          if isinstance(node, ast.BinOp)
                          and isinstance(node.op, ast.Mod))

            if mod_count >= 1:
                return {
                    'name': 'Code uses modulus (%) operator',
                    'passed': True,
                    'message': f'Found {mod_count} modulus operation(s). Well done!'
                }
            else:
                return {
                    'name': 'Code uses modulus (%) operator',
                    'passed': False,
                    'message': 'No modulus operator found. Use % to calculate remainders.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses modulus (%) operator',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses modulus (%) operator',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_floor_division(self):
        """Test that the code uses floor division (//) operator."""
        try:
            tree = ast.parse(self.code_content)
            floordiv_count = sum(1 for node in ast.walk(tree)
                                if isinstance(node, ast.BinOp)
                                and isinstance(node.op, ast.FloorDiv))

            if floordiv_count >= 1:
                return {
                    'name': 'Code uses floor division (//)',
                    'passed': True,
                    'message': f'Found {floordiv_count} floor division(s). Excellent!'
                }
            else:
                return {
                    'name': 'Code uses floor division (//)',
                    'passed': False,
                    'message': 'No floor division found. Use // for integer division.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses floor division (//)',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses floor division (//)',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_compound_assignment(self):
        """Test that the code uses compound assignment operators (+=, -=, etc.)."""
        try:
            tree = ast.parse(self.code_content)
            aug_assign_count = sum(1 for node in ast.walk(tree)
                                 if isinstance(node, ast.AugAssign))

            if aug_assign_count >= 2:
                return {
                    'name': 'Code uses compound assignment operators',
                    'passed': True,
                    'message': f'Found {aug_assign_count} compound assignment(s). Great!'
                }
            else:
                return {
                    'name': 'Code uses compound assignment operators',
                    'passed': False,
                    'message': f'Found only {aug_assign_count} compound assignment(s). Use operators like +=, -=, *=, etc.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses compound assignment operators',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses compound assignment operators',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_code_runs_without_errors(self):
        """Test that the code executes without errors."""
        try:
            # Provide test input (two numbers)
            test_input = "10\n5\n"

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

    def test_produces_comprehensive_output(self):
        """Test that the code produces comprehensive output showing operations."""
        try:
            if hasattr(self, 'output') and self.output.strip():
                output_lower = self.output.lower()
                lines = self.output.strip().split('\n')

                # Check for various operations in output
                has_addition = any('+' in line for line in lines)
                has_subtraction = any('-' in line for line in lines)
                has_multiplication = any('*' in line for line in lines)
                has_division = any('/' in line for line in lines)

                # Should have multiple calculations shown
                checks_passed = sum([has_addition, has_subtraction, has_multiplication, has_division])

                if checks_passed >= 3 and len(lines) >= 10:
                    return {
                        'name': 'Program produces comprehensive output',
                        'passed': True,
                        'message': f'Program shows {checks_passed} operation types across {len(lines)} lines. Excellent!'
                    }
                else:
                    return {
                        'name': 'Program produces comprehensive output',
                        'passed': False,
                        'message': f'Output needs improvement. Show all arithmetic operations, comparisons, and logical checks. Found {len(lines)} lines, need at least 10.'
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
            self.test_uses_arithmetic_operators,
            self.test_uses_comparison_operators,
            self.test_uses_modulus_operator,
            self.test_uses_floor_division,
            self.test_uses_compound_assignment,
            self.test_code_runs_without_errors,
            self.test_produces_comprehensive_output
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
    tester = Module004Tester(filepath)
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
