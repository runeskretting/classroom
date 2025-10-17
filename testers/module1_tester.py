"""
Module 1 Tester: Number Guessing Game
Tests student submissions for the Module 1 capstone project.
"""

import subprocess
import sys
import os
import random
import tempfile
from io import StringIO


class Module1Tester:
    def __init__(self, submission_path):
        self.submission_path = submission_path
        self.test_results = []
        self.passed = False

    def test_imports(self):
        """Test if the code imports the random module."""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            if 'import random' in code:
                self.test_results.append({
                    'test': 'Imports random module',
                    'passed': True,
                    'message': 'Successfully imports random module'
                })
                return True
            else:
                self.test_results.append({
                    'test': 'Imports random module',
                    'passed': False,
                    'message': 'Code does not import random module'
                })
                return False
        except Exception as e:
            self.test_results.append({
                'test': 'Imports random module',
                'passed': False,
                'message': f'Error reading file: {str(e)}'
            })
            return False

    def test_code_structure(self):
        """Test if the code contains necessary structures."""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            checks = {
                'while loop': 'while' in code,
                'input() function': 'input(' in code,
                'if/elif/else': all(keyword in code for keyword in ['if ', 'else']),
                'comparison operators': any(op in code for op in ['<', '>', '==', '!=']),
                'print statements': 'print(' in code
            }

            for check_name, passed in checks.items():
                self.test_results.append({
                    'test': f'Contains {check_name}',
                    'passed': passed,
                    'message': f'Code {"contains" if passed else "missing"} {check_name}'
                })

            return all(checks.values())
        except Exception as e:
            self.test_results.append({
                'test': 'Code structure check',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_game_logic(self):
        """Test the actual game logic by simulating gameplay."""
        try:
            # Test 1: Too low guess, then correct
            test_input = "50\n75\n"
            expected_patterns = ['Too low', '75']

            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5,
                env={**os.environ, 'PYTHONHASHSEED': '0'}
            )

            output = result.stdout.lower()

            # Check for "too low" or "too high" feedback
            has_feedback = 'too low' in output or 'too high' in output

            # Check for congratulations message
            has_congrats = any(word in output for word in ['congratulat', 'correct', 'got it', 'you win'])

            if has_feedback:
                self.test_results.append({
                    'test': 'Provides feedback (too high/too low)',
                    'passed': True,
                    'message': 'Game provides appropriate feedback'
                })
            else:
                self.test_results.append({
                    'test': 'Provides feedback (too high/too low)',
                    'passed': False,
                    'message': 'Game does not provide clear feedback'
                })

            if has_congrats:
                self.test_results.append({
                    'test': 'Congratulates on correct guess',
                    'passed': True,
                    'message': 'Game congratulates player on winning'
                })
            else:
                self.test_results.append({
                    'test': 'Congratulates on correct guess',
                    'passed': False,
                    'message': 'Game does not congratulate player'
                })

            # Test that game accepts input and runs without errors
            game_runs = result.returncode == 0

            if game_runs:
                self.test_results.append({
                    'test': 'Game runs without errors',
                    'passed': True,
                    'message': 'Game executes successfully'
                })
            else:
                self.test_results.append({
                    'test': 'Game runs without errors',
                    'passed': False,
                    'message': f'Game crashed: {result.stderr}'
                })

            return has_feedback and has_congrats and game_runs

        except subprocess.TimeoutExpired:
            self.test_results.append({
                'test': 'Game logic test',
                'passed': False,
                'message': 'Game timed out - possible infinite loop'
            })
            return False
        except Exception as e:
            self.test_results.append({
                'test': 'Game logic test',
                'passed': False,
                'message': f'Error running game: {str(e)}'
            })
            return False

    def run_all_tests(self):
        """Run all tests and return results."""
        imports_ok = self.test_imports()
        structure_ok = self.test_code_structure()
        logic_ok = self.test_game_logic()

        # Calculate overall pass/fail
        passed_count = sum(1 for result in self.test_results if result['passed'])
        total_count = len(self.test_results)

        self.passed = passed_count >= total_count * 0.75  # 75% pass rate

        return {
            'passed': self.passed,
            'score': f'{passed_count}/{total_count}',
            'percentage': int((passed_count / total_count) * 100),
            'tests': self.test_results,
            'message': 'All tests passed! Your number guessing game works correctly.' if self.passed
                      else 'Some tests failed. Please review the feedback and try again.'
        }


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

    tester = Module1Tester(submission_path)
    return tester.run_all_tests()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python module1_tester.py <submission_path>")
        sys.exit(1)

    result = test_submission(sys.argv[1])
    print(f"\nTest Results:")
    print(f"Score: {result['score']} ({result['percentage']}%)")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}\n")

    for test in result['tests']:
        status = '✓' if test['passed'] else '✗'
        print(f"{status} {test['test']}: {test['message']}")

    print(f"\n{result['message']}")
