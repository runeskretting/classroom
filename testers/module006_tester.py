"""
Module 6 Tester: Day 6 - Conditional Logic (if/elif/else)
Tests student submissions for the Adventure Game Decision Maker project.
"""

import ast
import subprocess
import sys
import os
import re


class Module006Tester:
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

            if comment_count >= 8:
                return {
                    'name': 'Code contains sufficient comments',
                    'passed': True,
                    'message': f'Found {comment_count} comments. Great documentation!'
                }
            else:
                return {
                    'name': 'Code contains sufficient comments',
                    'passed': False,
                    'message': f'Found only {comment_count} comment(s). Need at least 8 to explain your conditional logic.'
                }
        except Exception as e:
            return {
                'name': 'Code contains sufficient comments',
                'passed': False,
                'message': f'Error checking comments: {str(e)}'
            }

    def test_uses_input(self):
        """Test that the code uses input() for user choices."""
        try:
            tree = ast.parse(self.code_content)
            input_count = sum(1 for node in ast.walk(tree)
                            if isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)
                            and node.func.id == 'input')

            if input_count >= 3:
                return {
                    'name': 'Code uses input() for choices',
                    'passed': True,
                    'message': f'Found {input_count} input() calls. Good interactivity!'
                }
            else:
                return {
                    'name': 'Code uses input() for choices',
                    'passed': False,
                    'message': f'Found only {input_count} input() call(s). Need at least 3: name + 2 decision points.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses input() for choices',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses input() for choices',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_has_if_statements(self):
        """Test that the code uses if statements."""
        try:
            tree = ast.parse(self.code_content)
            if_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.If))

            if if_count >= 6:
                return {
                    'name': 'Code uses if/elif/else statements',
                    'passed': True,
                    'message': f'Found {if_count} if statement(s). Excellent branching logic!'
                }
            else:
                return {
                    'name': 'Code uses if/elif/else statements',
                    'passed': False,
                    'message': f'Found only {if_count} if statement(s). Need at least 6 for proper branching (3 paths × 2 levels).'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses if/elif/else statements',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses if/elif/else statements',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_has_nested_conditionals(self):
        """Test that the code uses nested if statements."""
        try:
            tree = ast.parse(self.code_content)

            # Find if statements that contain other if statements
            nested_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    # Check if this if statement contains another if in its body
                    for child in ast.walk(node):
                        if child != node and isinstance(child, ast.If):
                            nested_found = True
                            break
                if nested_found:
                    break

            if nested_found:
                return {
                    'name': 'Code uses nested conditionals',
                    'passed': True,
                    'message': 'Found nested if statements. Great use of multi-level decision making!'
                }
            else:
                return {
                    'name': 'Code uses nested conditionals',
                    'passed': False,
                    'message': 'No nested if statements found. You need second-level decisions within each path.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses nested conditionals',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses nested conditionals',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_logical_operators(self):
        """Test that the code uses logical operators (and/or)."""
        try:
            tree = ast.parse(self.code_content)

            # Look for BoolOp nodes (and, or)
            has_and = False
            has_or = False

            for node in ast.walk(tree):
                if isinstance(node, ast.BoolOp):
                    if isinstance(node.op, ast.And):
                        has_and = True
                    elif isinstance(node.op, ast.Or):
                        has_or = True

            if has_and or has_or:
                ops_used = []
                if has_and:
                    ops_used.append("'and'")
                if has_or:
                    ops_used.append("'or'")
                return {
                    'name': 'Code uses logical operators',
                    'passed': True,
                    'message': f'Found logical operator(s): {", ".join(ops_used)}. Great use of compound conditions!'
                }
            else:
                return {
                    'name': 'Code uses logical operators',
                    'passed': False,
                    'message': 'No logical operators (and/or) found. Use them to combine conditions.'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses logical operators',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses logical operators',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_uses_fstrings_or_format(self):
        """Test that the code uses f-strings or format for output."""
        try:
            tree = ast.parse(self.code_content)

            # Count f-strings (JoinedStr nodes)
            fstring_count = sum(1 for node in ast.walk(tree)
                              if isinstance(node, ast.JoinedStr))

            # Also check for .format() calls
            format_count = 0
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and
                    isinstance(node.func, ast.Attribute) and
                    node.func.attr == 'format'):
                    format_count += 1

            total_formatting = fstring_count + format_count

            if fstring_count >= 2:
                return {
                    'name': 'Code uses f-strings for name in output',
                    'passed': True,
                    'message': f'Found {fstring_count} f-string(s). Excellent formatting!'
                }
            elif total_formatting >= 2:
                return {
                    'name': 'Code uses f-strings for name in output',
                    'passed': True,
                    'message': f'Found string formatting. Consider using f-strings for cleaner code!'
                }
            else:
                return {
                    'name': 'Code uses f-strings for name in output',
                    'passed': False,
                    'message': 'Need to use character name in outputs. Use f-strings like f"Welcome, {name}!"'
                }
        except SyntaxError as e:
            return {
                'name': 'Code uses f-strings for name in output',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Code uses f-strings for name in output',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def test_code_runs_path1(self):
        """Test that the code runs for first decision path."""
        try:
            # Test first path - will depend on student's implementation
            # Provide generic inputs that should work for most adventure games
            test_input = "TestPlayer\nleft\nopen\n"

            result = subprocess.run(
                [sys.executable, self.filepath],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                self.test_outputs.append(('path1', result.stdout))
                return {
                    'name': 'Code runs successfully (path 1)',
                    'passed': True,
                    'message': 'Program executed successfully for first path!'
                }
            else:
                return {
                    'name': 'Code runs successfully (path 1)',
                    'passed': False,
                    'message': f'Program error on first path: {result.stderr}'
                }
        except subprocess.TimeoutExpired:
            return {
                'name': 'Code runs successfully (path 1)',
                'passed': False,
                'message': 'Program took too long to run (timeout). Check for infinite loops.'
            }
        except Exception as e:
            return {
                'name': 'Code runs successfully (path 1)',
                'passed': False,
                'message': f'Error running program: {str(e)}'
            }

    def test_code_runs_path2(self):
        """Test that the code runs for second decision path."""
        try:
            test_input = "TestPlayer\nright\nyes\n"

            result = subprocess.run(
                [sys.executable, self.filepath],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                self.test_outputs.append(('path2', result.stdout))
                return {
                    'name': 'Code runs successfully (path 2)',
                    'passed': True,
                    'message': 'Program executed successfully for second path!'
                }
            else:
                return {
                    'name': 'Code runs successfully (path 2)',
                    'passed': False,
                    'message': f'Program error on second path: {result.stderr}'
                }
        except subprocess.TimeoutExpired:
            return {
                'name': 'Code runs successfully (path 2)',
                'passed': False,
                'message': 'Program timeout on second path.'
            }
        except Exception as e:
            return {
                'name': 'Code runs successfully (path 2)',
                'passed': False,
                'message': f'Error running program (path 2): {str(e)}'
            }

    def test_different_outputs(self):
        """Test that different paths produce different outputs."""
        try:
            if len(self.test_outputs) < 2:
                return {
                    'name': 'Different paths produce different outputs',
                    'passed': False,
                    'message': 'Cannot test - not enough successful runs.'
                }

            path1_output = self.test_outputs[0][1]
            path2_output = self.test_outputs[1][1]

            # Remove the character name from comparison (since it's the same)
            path1_clean = path1_output.replace('TestPlayer', '').lower()
            path2_clean = path2_output.replace('TestPlayer', '').lower()

            # Check if outputs are meaningfully different (at least 20% different)
            similarity = len(set(path1_clean) & set(path2_clean)) / max(len(path1_clean), len(path2_clean))

            if similarity < 0.8:  # Less than 80% similar = different enough
                return {
                    'name': 'Different paths produce different outputs',
                    'passed': True,
                    'message': 'Different choices lead to different outcomes. Great branching!'
                }
            else:
                return {
                    'name': 'Different paths produce different outputs',
                    'passed': False,
                    'message': 'Outputs are too similar. Make sure each path has unique outcomes.'
                }
        except Exception as e:
            return {
                'name': 'Different paths produce different outputs',
                'passed': False,
                'message': f'Error comparing outputs: {str(e)}'
            }

    def test_uses_character_name(self):
        """Test that character name appears in output."""
        try:
            if not self.test_outputs:
                return {
                    'name': 'Uses character name in output',
                    'passed': False,
                    'message': 'Cannot test - program did not run successfully.'
                }

            output = self.test_outputs[0][1]

            if 'TestPlayer' in output:
                return {
                    'name': 'Uses character name in output',
                    'passed': True,
                    'message': 'Character name appears in output. Good personalization!'
                }
            else:
                return {
                    'name': 'Uses character name in output',
                    'passed': False,
                    'message': 'Character name not found in output. Use the name variable in your messages.'
                }
        except Exception as e:
            return {
                'name': 'Uses character name in output',
                'passed': False,
                'message': f'Error checking for character name: {str(e)}'
            }

    def test_has_numeric_comparison(self):
        """Test that code includes at least one numeric comparison."""
        try:
            tree = ast.parse(self.code_content)

            # Look for comparisons involving numbers or numeric operations
            has_numeric_comparison = False

            for node in ast.walk(tree):
                if isinstance(node, ast.Compare):
                    # Check if left side or any comparator involves a number or numeric variable
                    if isinstance(node.left, (ast.Num, ast.Constant)):
                        has_numeric_comparison = True
                        break
                    for comp in node.comparators:
                        if isinstance(comp, (ast.Num, ast.Constant)):
                            has_numeric_comparison = True
                            break
                if has_numeric_comparison:
                    break

            if has_numeric_comparison:
                return {
                    'name': 'Includes numeric comparison',
                    'passed': True,
                    'message': 'Found numeric comparison. Good use of numbers in conditions!'
                }
            else:
                return {
                    'name': 'Includes numeric comparison',
                    'passed': False,
                    'message': 'No numeric comparison found. Add a check like "if gold > 50" or "if health >= 100".'
                }
        except SyntaxError as e:
            return {
                'name': 'Includes numeric comparison',
                'passed': False,
                'message': f'Syntax error in code: {str(e)}'
            }
        except Exception as e:
            return {
                'name': 'Includes numeric comparison',
                'passed': False,
                'message': f'Error analyzing code: {str(e)}'
            }

    def run_all_tests(self):
        """Run all tests and return results."""
        test_methods = [
            self.test_file_exists,
            self.test_has_comments,
            self.test_uses_input,
            self.test_has_if_statements,
            self.test_has_nested_conditionals,
            self.test_uses_logical_operators,
            self.test_uses_fstrings_or_format,
            self.test_code_runs_path1,
            self.test_code_runs_path2,
            self.test_different_outputs,
            self.test_uses_character_name,
            self.test_has_numeric_comparison
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
            'message': 'All tests passed! Excellent adventure game!' if passed_count == total_count else
                      'Good work! Your adventure game meets the requirements.' if self.passed else
                      'Some tests failed. Review the feedback and enhance your game.'
        }


def test_submission(filepath):
    """Main entry point for testing a submission."""
    tester = Module006Tester(filepath)
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
