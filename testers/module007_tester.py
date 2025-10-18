"""
Module 7 Tester: Day 7 - Loops (while and for)
Tests student submissions for the Interactive Number Game project.
"""

import ast
import subprocess
import sys
import os
import re


class Module007Tester:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tests = []
        self.passed = False
        self.test_outputs = []

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
        """Test that the code contains sufficient comments."""
        try:
            comment_count = self.code_content.count('#')

            if comment_count >= 5:
                return {
                    'name': 'Code contains sufficient comments',
                    'passed': True,
                    'message': f'Found {comment_count} comments. Great documentation!'
                }
            else:
                return {
                    'name': 'Code contains sufficient comments',
                    'passed': False,
                    'message': f'Found only {comment_count} comment(s). Need at least 5 to explain your loop logic.'
                }
        except Exception as e:
            return {
                'name': 'Code contains sufficient comments',
                'passed': False,
                'message': f'Error checking comments: {str(e)}'
            }

    def test_has_while_loop(self):
        """Test that the code uses a while loop."""
        try:
            tree = ast.parse(self.code_content)
            while_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.While))

            if while_count >= 1:
                return {
                    'name': 'Code uses while loop',
                    'passed': True,
                    'message': f'Found {while_count} while loop(s). Great use of repetition!'
                }
            else:
                return {
                    'name': 'Code uses while loop',
                    'passed': False,
                    'message': 'No while loop found. Use a while loop for the main game loop (play multiple rounds).'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses while loop',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses while loop',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_has_for_loop_or_range(self):
        """Test that the code uses a for loop or range()."""
        try:
            tree = ast.parse(self.code_content)

            # Check for for loops
            for_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.For))

            # Check for range() calls
            range_count = sum(1 for node in ast.walk(tree)
                            if isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)
                            and node.func.id == 'range')

            if for_count >= 1 or range_count >= 1:
                return {
                    'name': 'Code uses for loop with range()',
                    'passed': True,
                    'message': f'Found for loop or range(). Great for counting attempts!'
                }
            else:
                return {
                    'name': 'Code uses for loop with range()',
                    'passed': False,
                    'message': 'No for loop or range() found. Use a for loop to limit attempts per round.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses for loop with range()',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses for loop with range()',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_has_break_statement(self):
        """Test that the code uses break statement."""
        try:
            tree = ast.parse(self.code_content)
            break_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Break))

            if break_count >= 1:
                return {
                    'name': 'Code uses break statement',
                    'passed': True,
                    'message': f'Found {break_count} break statement(s). Good loop control!'
                }
            else:
                return {
                    'name': 'Code uses break statement',
                    'passed': False,
                    'message': 'No break statement found. Use break to exit early when guess is correct.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses break statement',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses break statement',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_has_score_tracking(self):
        """Test that the code tracks scores with variables."""
        try:
            tree = ast.parse(self.code_content)

            # Look for variable assignments that might be score tracking
            score_related_vars = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    var_name = node.id.lower()
                    if any(keyword in var_name for keyword in ['score', 'round', 'won', 'win', 'count', 'played']):
                        if var_name not in score_related_vars:
                            score_related_vars.append(var_name)

            if len(score_related_vars) >= 2:
                return {
                    'name': 'Code tracks game statistics',
                    'passed': True,
                    'message': f'Found score tracking variables. Good game stats management!'
                }
            else:
                return {
                    'name': 'Code tracks game statistics',
                    'passed': False,
                    'message': 'Need variables to track rounds played and rounds won.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code tracks game statistics',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code tracks game statistics',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_input_validation(self):
        """Test that the code validates user input."""
        try:
            # Check for input validation patterns: isdigit(), try/except, range checks
            has_isdigit = 'isdigit' in self.code_content or 'isnumeric' in self.code_content
            has_try_except = 'try:' in self.code_content and 'except' in self.code_content
            has_range_check = re.search(r'(if|elif|while).*(<|>|<=|>=|\s1\s|\s100\s)', self.code_content)

            if has_isdigit or has_try_except or has_range_check:
                return {
                    'name': 'Code validates user input',
                    'passed': True,
                    'message': 'Found input validation. Great error handling!'
                }
            else:
                return {
                    'name': 'Code validates user input',
                    'passed': False,
                    'message': 'No clear input validation found. Check if guess is valid (1-100, is a number).'
                }
        except Exception as e:
            return {
                'name': 'Code validates user input',
                'passed': False,
                'message': f'Error checking validation: {str(e)}'
            }

    def test_has_comparison_operators(self):
        """Test that the code uses comparison operators for guessing logic."""
        try:
            tree = ast.parse(self.code_content)

            # Count comparison operators
            comparison_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Compare))

            if comparison_count >= 5:
                return {
                    'name': 'Code uses comparison operators',
                    'passed': True,
                    'message': f'Found {comparison_count} comparisons. Good guessing logic!'
                }
            else:
                return {
                    'name': 'Code uses comparison operators',
                    'passed': False,
                    'message': f'Found only {comparison_count} comparison(s). Need comparisons for: too high, too low, correct, validation, etc.'
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

    def test_code_runs_basic(self):
        """Test that the code runs with basic input."""
        try:
            # Simulate: entering invalid input once, then quitting
            # This avoids needing to guess correctly
            test_input = "50\nno\n"

            result = subprocess.run(
                [sys.executable, self.filepath],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                self.test_outputs.append(('basic', result.stdout))
                return {
                    'name': 'Code runs successfully',
                    'passed': True,
                    'message': 'Program executed without errors!'
                }
            else:
                # Check if error is due to missing random import
                if 'random' in result.stderr:
                    return {
                        'name': 'Code runs successfully',
                        'passed': False,
                        'message': 'Missing: import random. Add "import random" at the top of your file.'
                    }
                return {
                    'name': 'Code runs successfully',
                    'passed': False,
                    'message': f'Program error: {result.stderr[:200]}'
                }
        except subprocess.TimeoutExpired:
            return {
                'name': 'Code runs successfully',
                'passed': False,
                'message': 'Program timeout. Check for infinite loops or missing input handling.'
            }
        except Exception as e:
            return {
                'name': 'Code runs successfully',
                'passed': False,
                'message': f'Error running program: {str(e)}'
            }

    def test_provides_feedback(self):
        """Test that the code provides feedback (too high/too low)."""
        try:
            if not self.test_outputs:
                return {
                    'name': 'Provides feedback on guesses',
                    'passed': False,
                    'message': 'Cannot test - program did not run successfully.'
                }

            output = self.test_outputs[0][1].lower()

            # Check for common feedback phrases
            has_feedback = any(phrase in output for phrase in
                             ['too high', 'too low', 'higher', 'lower', 'correct', 'guessed'])

            if has_feedback:
                return {
                    'name': 'Provides feedback on guesses',
                    'passed': True,
                    'message': 'Program provides feedback to player. Great user experience!'
                }
            else:
                return {
                    'name': 'Provides feedback on guesses',
                    'passed': False,
                    'message': 'No clear feedback found. Tell player if guess is too high, too low, or correct.'
                }
        except Exception as e:
            return {
                'name': 'Provides feedback on guesses',
                'passed': False,
                'message': f'Error checking feedback: {str(e)}'
            }

    def test_shows_final_stats(self):
        """Test that the code displays final statistics."""
        try:
            if not self.test_outputs:
                return {
                    'name': 'Displays final statistics',
                    'passed': False,
                    'message': 'Cannot test - program did not run successfully.'
                }

            output = self.test_outputs[0][1].lower()

            # Check for statistics-related keywords
            has_stats = any(phrase in output for phrase in
                          ['round', 'score', 'won', 'played', 'total', 'statistics', 'final'])

            if has_stats:
                return {
                    'name': 'Displays final statistics',
                    'passed': True,
                    'message': 'Program shows final statistics. Excellent!'
                }
            else:
                return {
                    'name': 'Displays final statistics',
                    'passed': False,
                    'message': 'No final statistics found. Show rounds played and rounds won at the end.'
                }
        except Exception as e:
            return {
                'name': 'Displays final statistics',
                'passed': False,
                'message': f'Error checking statistics: {str(e)}'
            }

    def test_has_proper_structure(self):
        """Test that code has proper structure with variables and loops."""
        try:
            tree = ast.parse(self.code_content)

            # Count assignments (for variables)
            assignment_count = sum(1 for node in ast.walk(tree)
                                 if isinstance(node, (ast.Assign, ast.AugAssign)))

            # Count loops
            loop_count = sum(1 for node in ast.walk(tree)
                           if isinstance(node, (ast.While, ast.For)))

            if assignment_count >= 5 and loop_count >= 2:
                return {
                    'name': 'Has proper program structure',
                    'passed': True,
                    'message': 'Good structure with variables and loops!'
                }
            else:
                return {
                    'name': 'Has proper program structure',
                    'passed': False,
                    'message': f'Structure needs work. Found {assignment_count} assignments and {loop_count} loops. Need more variables and both while/for loops.'
                }
        except SyntaxError as e:
            return {
                'name': 'Has proper program structure',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Has proper program structure',
                'passed': False,
                'message': f'Error analyzing structure: {str(e)}'
            }

    def run_all_tests(self):
        """Run all tests and return results."""
        test_methods = [
            self.test_file_exists,
            self.test_has_comments,
            self.test_has_while_loop,
            self.test_has_for_loop_or_range,
            self.test_has_break_statement,
            self.test_has_score_tracking,
            self.test_uses_input_validation,
            self.test_has_comparison_operators,
            self.test_has_proper_structure,
            self.test_code_runs_basic,
            self.test_provides_feedback,
            self.test_shows_final_stats
        ]

        for test_method in test_methods:
            result = test_method()
            self.tests.append(result)
            # If file doesn't exist, stop testing
            if not result['passed'] and test_method == self.test_file_exists:
                break

        passed_count = sum(1 for test in self.tests if test['passed'])
        total_count = len(self.tests)

        # Require at least 9/12 tests to pass (75%)
        self.passed = passed_count >= 9

        return {
            'passed': self.passed,
            'score': f'{passed_count}/{total_count} ({int(passed_count/total_count*100)}%)',
            'tests': self.tests,
            'message': 'Perfect! All tests passed. Excellent number game!' if passed_count == total_count else
                      'Great work! Your number game meets the requirements.' if self.passed else
                      'Some tests failed. Review the feedback and improve your game.'
        }


def test_submission(filepath):
    """Main entry point for testing a submission."""
    tester = Module007Tester(filepath)
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
