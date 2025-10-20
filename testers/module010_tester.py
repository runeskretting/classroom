#!/usr/bin/env python3
"""
Module 10 Tester: Loan Eligibility System
Tests student submissions for logical operators (and, or, not).
"""

import subprocess
import sys
import os
import ast


class Module10Tester:
    def __init__(self, submission_path):
        self.submission_path = submission_path
        self.tests = []
        self.passed = False
        self.score = "0/0"

    def test_file_exists(self):
        """Test 1: Check if submission file exists"""
        if os.path.exists(self.submission_path):
            self.tests.append({
                "name": "File exists",
                "passed": True,
                "message": "Submission file found"
            })
            return True
        else:
            self.tests.append({
                "name": "File exists",
                "passed": False,
                "message": "Submission file not found"
            })
            return False

    def test_has_and_operator(self):
        """Test 2: Check if code contains 'and' operator"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            tree = ast.parse(code)

            # Look for BoolOp nodes with And operator
            and_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
                    and_found = True
                    break

            if and_found:
                self.tests.append({
                    "name": "'and' operator present",
                    "passed": True,
                    "message": "Code uses the 'and' logical operator"
                })
                return True
            else:
                self.tests.append({
                    "name": "'and' operator present",
                    "passed": False,
                    "message": "No 'and' operator found - project requires using 'and' for combining conditions"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "'and' operator present",
                "passed": False,
                "message": f"Error parsing code: {e}"
            })
            return False

    def test_has_or_operator(self):
        """Test 3: Check if code contains 'or' operator"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            tree = ast.parse(code)

            # Look for BoolOp nodes with Or operator
            or_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
                    or_found = True
                    break

            if or_found:
                self.tests.append({
                    "name": "'or' operator present",
                    "passed": True,
                    "message": "Code uses the 'or' logical operator"
                })
                return True
            else:
                self.tests.append({
                    "name": "'or' operator present",
                    "passed": False,
                    "message": "No 'or' operator found - project requires using 'or' for alternative conditions"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "'or' operator present",
                "passed": False,
                "message": f"Error parsing code: {e}"
            })
            return False

    def test_has_not_operator(self):
        """Test 4: Check if code contains 'not' operator"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            tree = ast.parse(code)

            # Look for UnaryOp nodes with Not operator
            not_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                    not_found = True
                    break

            if not_found:
                self.tests.append({
                    "name": "'not' operator present",
                    "passed": True,
                    "message": "Code uses the 'not' logical operator"
                })
                return True
            else:
                self.tests.append({
                    "name": "'not' operator present",
                    "passed": False,
                    "message": "No 'not' operator found - project requires using 'not' for negation"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "'not' operator present",
                "passed": False,
                "message": f"Error parsing code: {e}"
            })
            return False

    def test_standard_approval(self):
        """Test 5: Standard path - should approve (age=30, income=45000, credit=700, employed, no cosigner)"""
        test_input = "30\n45000\n700\nemployed\nno\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            # Check if output contains approval indication
            if ('approved' in output or 'approve' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Standard approval case",
                    "passed": True,
                    "message": "Correctly approved qualified applicant (standard path)"
                })
                return True
            else:
                self.tests.append({
                    "name": "Standard approval case",
                    "passed": False,
                    "message": f"Should approve: age=30, income=$45k, credit=700, employed. Output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Standard approval case",
                "passed": False,
                "message": "Program timed out - check for infinite loops"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Standard approval case",
                "passed": False,
                "message": f"Error running program: {e}"
            })
            return False

    def test_cosigner_approval(self):
        """Test 6: Alternative path with cosigner - should approve (age=25, income=25000, credit=620, employed, yes cosigner)"""
        test_input = "25\n25000\n620\nemployed\nyes\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('approved' in output or 'approve' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Cosigner approval case",
                    "passed": True,
                    "message": "Correctly approved with cosigner (alternative path)"
                })
                return True
            else:
                self.tests.append({
                    "name": "Cosigner approval case",
                    "passed": False,
                    "message": f"Should approve with cosigner: income=$25k, credit=620, cosigner=yes. Output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Cosigner approval case",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Cosigner approval case",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_age_denial(self):
        """Test 7: Should deny for age < 21 (age=20, income=50000, credit=750, employed, no cosigner)"""
        test_input = "20\n50000\n750\nemployed\nno\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('denied' in output or 'deny' in output or 'not approved' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Age denial case",
                    "passed": True,
                    "message": "Correctly denied applicant under 21"
                })
                return True
            else:
                self.tests.append({
                    "name": "Age denial case",
                    "passed": False,
                    "message": f"Should deny for age=20 (under 21). Output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Age denial case",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Age denial case",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_unemployment_denial(self):
        """Test 8: Should deny for unemployed without cosigner (age=30, income=25000, credit=680, unemployed, no cosigner)"""
        test_input = "30\n25000\n680\nunemployed\nno\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('denied' in output or 'deny' in output or 'not approved' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Unemployment denial case",
                    "passed": True,
                    "message": "Correctly denied unemployed applicant without cosigner"
                })
                return True
            else:
                self.tests.append({
                    "name": "Unemployment denial case",
                    "passed": False,
                    "message": f"Should deny unemployed without cosigner. Output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Unemployment denial case",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Unemployment denial case",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_low_income_denial(self):
        """Test 9: Should deny for income too low (age=30, income=29000, credit=700, employed, no cosigner)"""
        test_input = "30\n29000\n700\nemployed\nno\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('denied' in output or 'deny' in output or 'not approved' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Low income denial case",
                    "passed": True,
                    "message": "Correctly denied for insufficient income ($29k < $30k required)"
                })
                return True
            else:
                self.tests.append({
                    "name": "Low income denial case",
                    "passed": False,
                    "message": f"Should deny for income=$29k (below $30k requirement). Output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Low income denial case",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Low income denial case",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_case_insensitive(self):
        """Test 10: Check that inputs are case-insensitive"""
        test_cases = [
            ("30\n45000\n700\nEMPLOYED\nNO\n", "approved", "uppercase input"),
            ("30\n45000\n700\nEmployed\nNo\n", "approved", "mixed case input"),
        ]

        all_passed = True
        messages = []

        for test_input, expected, description in test_cases:
            try:
                result = subprocess.run(
                    [sys.executable, self.submission_path],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if expected not in result.stdout.lower():
                    all_passed = False
                    messages.append(f"Failed {description}")
            except Exception as e:
                all_passed = False
                messages.append(f"Error on {description}: {e}")

        if all_passed:
            self.tests.append({
                "name": "Case insensitive input",
                "passed": True,
                "message": "Program correctly handles uppercase/lowercase input"
            })
            return True
        else:
            self.tests.append({
                "name": "Case insensitive input",
                "passed": False,
                "message": f"Input should be case-insensitive. Issues: {', '.join(messages)}"
            })
            return False

    def run_all_tests(self):
        """Run all tests and calculate score"""
        print(f"\n{'='*60}")
        print(f"Testing Module 10: Loan Eligibility System")
        print(f"{'='*60}\n")

        # Run all tests
        self.test_file_exists()
        self.test_has_and_operator()
        self.test_has_or_operator()
        self.test_has_not_operator()
        self.test_standard_approval()
        self.test_cosigner_approval()
        self.test_age_denial()
        self.test_unemployment_denial()
        self.test_low_income_denial()
        self.test_case_insensitive()

        # Calculate score
        total_tests = len(self.tests)
        passed_tests = sum(1 for test in self.tests if test['passed'])

        self.score = f"{passed_tests}/{total_tests} ({int(passed_tests/total_tests*100)}%)"
        self.passed = passed_tests >= total_tests * 0.75  # 75% to pass

        # Print results
        for test in self.tests:
            status = "✓ PASS" if test['passed'] else "✗ FAIL"
            print(f"{status}: {test['name']}")
            print(f"   {test['message']}\n")

        print(f"{'='*60}")
        print(f"Score: {self.score}")
        print(f"Status: {'PASSED' if self.passed else 'FAILED'}")
        print(f"{'='*60}\n")


def test_submission(filepath):
    """Main testing function called by the web app"""
    tester = Module10Tester(filepath)
    tester.run_all_tests()

    return {
        'passed': tester.passed,
        'score': tester.score,
        'tests': tester.tests,
        'message': 'Excellent work! Your logical operators work perfectly!' if tester.passed
                   else 'Keep working on your logical operators. Make sure to use and, or, and not operators correctly.'
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python module010_tester.py <path_to_submission>")
        sys.exit(1)

    result = test_submission(sys.argv[1])
    print(f"\nFinal Result: {'PASSED' if result['passed'] else 'FAILED'}")
    print(f"Score: {result['score']}")
    print(f"Message: {result['message']}")
