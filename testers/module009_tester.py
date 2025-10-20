#!/usr/bin/env python3
"""
Module 9 Tester: Amusement Park Ticket System
Tests student submissions for nested if/elif/else statements.
"""

import subprocess
import sys
import os
import ast


class Module9Tester:
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

    def test_has_nested_if(self):
        """Test 2: Check if code contains nested if statements"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            tree = ast.parse(code)

            # Look for nested If nodes in the AST
            def has_nested_if_in_node(node, depth=0):
                if isinstance(node, ast.If):
                    # Check if this If has another If in its body or orelse
                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, ast.If):
                            return True
                        for grandchild in ast.walk(child):
                            if isinstance(grandchild, ast.If) and grandchild != node:
                                return True
                return False

            # Walk through all nodes to find nested ifs
            nested_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    if has_nested_if_in_node(node):
                        nested_found = True
                        break

            if nested_found:
                self.tests.append({
                    "name": "Nested if statements present",
                    "passed": True,
                    "message": "Code contains nested if/elif/else statements"
                })
                return True
            else:
                self.tests.append({
                    "name": "Nested if statements present",
                    "passed": False,
                    "message": "No nested if statements found - project requires nested conditionals"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "Nested if statements present",
                "passed": False,
                "message": f"Error parsing code: {e}"
            })
            return False

    def test_vip_child_weekend(self):
        """Test 3: VIP child on weekend should be $40"""
        test_input = "vip\n8\nweekend\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            # Check if output contains $40
            if ('40' in output or 'forty' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "VIP child weekend ($40)",
                    "passed": True,
                    "message": "Correctly calculated VIP child weekend ticket: $40"
                })
                return True
            else:
                self.tests.append({
                    "name": "VIP child weekend ($40)",
                    "passed": False,
                    "message": f"Expected $40 for VIP child on weekend, output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "VIP child weekend ($40)",
                "passed": False,
                "message": "Program timed out - check for infinite loops"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "VIP child weekend ($40)",
                "passed": False,
                "message": f"Error running program: {e}"
            })
            return False

    def test_vip_adult_weekday(self):
        """Test 4: VIP adult on weekday should be $60"""
        test_input = "VIP\n30\nweekday\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('60' in output or 'sixty' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "VIP adult weekday ($60)",
                    "passed": True,
                    "message": "Correctly calculated VIP adult weekday ticket: $60"
                })
                return True
            else:
                self.tests.append({
                    "name": "VIP adult weekday ($60)",
                    "passed": False,
                    "message": f"Expected $60 for VIP adult on weekday, output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "VIP adult weekday ($60)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "VIP adult weekday ($60)",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_vip_senior_weekend(self):
        """Test 5: VIP senior on weekend should be $40"""
        test_input = "vip\n70\nweekend\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('40' in output or 'forty' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "VIP senior weekend ($40)",
                    "passed": True,
                    "message": "Correctly calculated VIP senior weekend ticket: $40"
                })
                return True
            else:
                self.tests.append({
                    "name": "VIP senior weekend ($40)",
                    "passed": False,
                    "message": f"Expected $40 for VIP senior on weekend, output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "VIP senior weekend ($40)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "VIP senior weekend ($40)",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_regular_child_weekday(self):
        """Test 6: Regular child on weekday should be $15"""
        test_input = "regular\n10\nweekday\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('15' in output or 'fifteen' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Regular child weekday ($15)",
                    "passed": True,
                    "message": "Correctly calculated Regular child weekday ticket: $15"
                })
                return True
            else:
                self.tests.append({
                    "name": "Regular child weekday ($15)",
                    "passed": False,
                    "message": f"Expected $15 for Regular child on weekday, output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Regular child weekday ($15)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Regular child weekday ($15)",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_regular_adult_weekend(self):
        """Test 7: Regular adult on weekend should be $40"""
        test_input = "REGULAR\n25\nWEEKEND\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('40' in output or 'forty' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Regular adult weekend ($40)",
                    "passed": True,
                    "message": "Correctly calculated Regular adult weekend ticket: $40"
                })
                return True
            else:
                self.tests.append({
                    "name": "Regular adult weekend ($40)",
                    "passed": False,
                    "message": f"Expected $40 for Regular adult on weekend, output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Regular adult weekend ($40)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Regular adult weekend ($40)",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_regular_senior_weekday(self):
        """Test 8: Regular senior on weekday should be $15"""
        test_input = "regular\n65\nweekday\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            if ('15' in output or 'fifteen' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Regular senior weekday ($15)",
                    "passed": True,
                    "message": "Correctly calculated Regular senior weekday ticket: $15"
                })
                return True
            else:
                self.tests.append({
                    "name": "Regular senior weekday ($15)",
                    "passed": False,
                    "message": f"Expected $15 for Regular senior (65+) on weekday, output: {result.stdout[:150]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Regular senior weekday ($15)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Regular senior weekday ($15)",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_case_insensitive(self):
        """Test 9: Check that inputs are case-insensitive"""
        test_cases = [
            ("VIP\n12\nWEEKEND\n", "80", "VIP adult weekend uppercase"),
            ("Vip\n50\nWeekday\n", "60", "VIP adult weekday mixed case"),
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

                if expected not in result.stdout:
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

    def test_edge_cases(self):
        """Test 10: Test edge cases (age boundaries)"""
        test_cases = [
            ("vip\n11\nweekday\n", "30", "VIP child age 11 (< 12)"),
            ("vip\n12\nweekday\n", "60", "VIP adult age 12 (>= 12)"),
            ("regular\n64\nweekend\n", "40", "Regular adult age 64 (< 65)"),
            ("regular\n65\nweekend\n", "20", "Regular senior age 65 (>= 65)"),
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

                if expected not in result.stdout:
                    all_passed = False
                    messages.append(f"Failed {description} (expected ${expected})")
            except Exception as e:
                all_passed = False
                messages.append(f"Error on {description}")

        if all_passed:
            self.tests.append({
                "name": "Edge cases (age boundaries)",
                "passed": True,
                "message": "Correctly handles age boundaries (12 and 65)"
            })
            return True
        else:
            self.tests.append({
                "name": "Edge cases (age boundaries)",
                "passed": False,
                "message": f"Age boundary issues: {', '.join(messages)}"
            })
            return False

    def run_all_tests(self):
        """Run all tests and calculate score"""
        print(f"\n{'='*60}")
        print(f"Testing Module 9: Amusement Park Ticket System")
        print(f"{'='*60}\n")

        # Run all tests
        self.test_file_exists()
        self.test_has_nested_if()
        self.test_vip_child_weekend()
        self.test_vip_adult_weekday()
        self.test_vip_senior_weekend()
        self.test_regular_child_weekday()
        self.test_regular_adult_weekend()
        self.test_regular_senior_weekday()
        self.test_case_insensitive()
        self.test_edge_cases()

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
        print(f"Status: {'PASSED' if self.passed else 'PASSED' if self.passed else 'FAILED'}")
        print(f"{'='*60}\n")


def test_submission(filepath):
    """Main testing function called by the web app"""
    tester = Module9Tester(filepath)
    tester.run_all_tests()

    return {
        'passed': tester.passed,
        'score': tester.score,
        'tests': tester.tests,
        'message': 'Excellent work! Your nested conditionals work perfectly!' if tester.passed
                   else 'Keep working on your nested if/elif/else logic. Make sure to handle all age categories and visitor types correctly.'
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python module009_tester.py <path_to_submission>")
        sys.exit(1)

    result = test_submission(sys.argv[1])
    print(f"\nFinal Result: {'PASSED' if result['passed'] else 'FAILED'}")
    print(f"Score: {result['score']}")
    print(f"Message: {result['message']}")
