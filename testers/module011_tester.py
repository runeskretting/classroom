#!/usr/bin/env python3
"""
Module 11 Tester: Day 11 - Rollercoaster Ride Checker
Tests student submissions for conditional logic with elif and logical operators.
"""

import subprocess
import sys
import os
import ast


class Module11Tester:
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

    def test_has_elif(self):
        """Test 2: Check if code uses elif statement"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            # Check for elif keyword in code
            if 'elif' in code:
                self.tests.append({
                    "name": "Uses elif statement",
                    "passed": True,
                    "message": "Code uses elif for multiple conditions"
                })
                return True
            else:
                self.tests.append({
                    "name": "Uses elif statement",
                    "passed": False,
                    "message": "No elif statement found - project requires elif for age categories"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "Uses elif statement",
                "passed": False,
                "message": f"Error reading code: {e}"
            })
            return False

    def test_has_logical_operator(self):
        """Test 3: Check if code contains logical operators (and/or) or chained comparison"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            tree = ast.parse(code)

            # Check for 'and' or 'or' operators
            has_and_or = False
            for node in ast.walk(tree):
                if isinstance(node, ast.BoolOp):
                    if isinstance(node.op, (ast.And, ast.Or)):
                        has_and_or = True
                        break

            # Check for chained comparisons (e.g., 45 <= age <= 55)
            has_chained_comparison = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare) and len(node.ops) > 1:
                    has_chained_comparison = True
                    break

            if has_and_or or has_chained_comparison:
                self.tests.append({
                    "name": "Uses logical operator or chained comparison",
                    "passed": True,
                    "message": "Code uses logical operators (and/or) or chained comparisons"
                })
                return True
            else:
                self.tests.append({
                    "name": "Uses logical operator or chained comparison",
                    "passed": False,
                    "message": "No logical operators (and/or) or chained comparisons found"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "Uses logical operator or chained comparison",
                "passed": False,
                "message": f"Error parsing code: {e}"
            })
            return False

    def test_height_rejection(self):
        """Test 4: Test that short height (< 120) is rejected"""
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input="100\n",  # Height too short
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            # Should contain rejection message
            if ('sorry' in output or 'cannot' in output or 'must be' in output or 'too short' in output) and '120' in output:
                # Should NOT ask for age (program should end)
                if 'age' not in output.lower():
                    self.tests.append({
                        "name": "Correctly rejects riders under 120cm",
                        "passed": True,
                        "message": "Program correctly rejects short riders and doesn't ask for age"
                    })
                    return True
                else:
                    self.tests.append({
                        "name": "Correctly rejects riders under 120cm",
                        "passed": False,
                        "message": "Program should not ask for age when height requirement not met"
                    })
                    return False
            else:
                self.tests.append({
                    "name": "Correctly rejects riders under 120cm",
                    "passed": False,
                    "message": "Program should display rejection message for height < 120cm"
                })
                return False

        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Correctly rejects riders under 120cm",
                "passed": False,
                "message": "Program timed out - possible infinite loop or waiting for input"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Correctly rejects riders under 120cm",
                "passed": False,
                "message": f"Error running test: {e}"
            })
            return False

    def test_child_ticket(self):
        """Test 5: Test child ticket (age < 12, price $5)"""
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input="130\n10\nno\n",  # Height 130, age 10, no photo
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout

            # Should show $5 price for child
            if '$5' in output or '5' in output.split('$')[-1].split()[0] if '$' in output else '':
                self.tests.append({
                    "name": "Child ticket pricing (age < 12)",
                    "passed": True,
                    "message": "Correctly charges $5 for children under 12"
                })
                return True
            else:
                self.tests.append({
                    "name": "Child ticket pricing (age < 12)",
                    "passed": False,
                    "message": "Child ticket should cost $5 (found different price)"
                })
                return False

        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Child ticket pricing (age < 12)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Child ticket pricing (age < 12)",
                "passed": False,
                "message": f"Error running test: {e}"
            })
            return False

    def test_youth_ticket(self):
        """Test 6: Test youth ticket (age 12-17, price $7)"""
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input="150\n15\nno\n",  # Height 150, age 15, no photo
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout

            # Should show $7 price for youth
            if '$7' in output or ('$' in output and '7' in output):
                self.tests.append({
                    "name": "Youth ticket pricing (age 12-17)",
                    "passed": True,
                    "message": "Correctly charges $7 for youth (12-17)"
                })
                return True
            else:
                self.tests.append({
                    "name": "Youth ticket pricing (age 12-17)",
                    "passed": False,
                    "message": "Youth ticket should cost $7 (found different price)"
                })
                return False

        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Youth ticket pricing (age 12-17)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Youth ticket pricing (age 12-17)",
                "passed": False,
                "message": f"Error running test: {e}"
            })
            return False

    def test_midlife_discount(self):
        """Test 7: Test midlife crisis discount (age 45-55, FREE)"""
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input="170\n50\nno\n",  # Height 170, age 50, no photo
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            # Should show free or $0
            if ('free' in output or '$0' in output or 'total bill is: $0' in output.lower()):
                self.tests.append({
                    "name": "Midlife crisis discount (age 45-55)",
                    "passed": True,
                    "message": "Correctly applies FREE ticket for ages 45-55"
                })
                return True
            else:
                self.tests.append({
                    "name": "Midlife crisis discount (age 45-55)",
                    "passed": False,
                    "message": "Ages 45-55 should ride for FREE (found different price)"
                })
                return False

        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Midlife crisis discount (age 45-55)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Midlife crisis discount (age 45-55)",
                "passed": False,
                "message": f"Error running test: {e}"
            })
            return False

    def test_adult_ticket(self):
        """Test 8: Test adult ticket (age 18+, not 45-55, price $12)"""
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input="175\n30\nno\n",  # Height 175, age 30, no photo
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout

            # Should show $12 price for adult
            if '$12' in output:
                self.tests.append({
                    "name": "Adult ticket pricing (age 18+)",
                    "passed": True,
                    "message": "Correctly charges $12 for adults"
                })
                return True
            else:
                self.tests.append({
                    "name": "Adult ticket pricing (age 18+)",
                    "passed": False,
                    "message": "Adult ticket should cost $12 (found different price)"
                })
                return False

        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Adult ticket pricing (age 18+)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Adult ticket pricing (age 18+)",
                "passed": False,
                "message": f"Error running test: {e}"
            })
            return False

    def test_photo_addon(self):
        """Test 9: Test photo add-on (+$3)"""
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input="140\n10\nyes\n",  # Height 140, age 10 (child $5), photo yes
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout

            # Should show total of $8 (child $5 + photo $3)
            if '$8' in output:
                self.tests.append({
                    "name": "Photo add-on (+$3)",
                    "passed": True,
                    "message": "Correctly adds $3 for photo (child $5 + photo $3 = $8)"
                })
                return True
            else:
                self.tests.append({
                    "name": "Photo add-on (+$3)",
                    "passed": False,
                    "message": "Photo should add $3 to ticket price (expected $8 total for child with photo)"
                })
                return False

        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Photo add-on (+$3)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Photo add-on (+$3)",
                "passed": False,
                "message": f"Error running test: {e}"
            })
            return False

    def test_case_insensitive_photo(self):
        """Test 10: Test photo input is case-insensitive"""
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input="140\n10\nYES\n",  # Height 140, age 10, photo "YES" in caps
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout

            # Should still show $8 (handles "YES" same as "yes")
            if '$8' in output:
                self.tests.append({
                    "name": "Case-insensitive photo input",
                    "passed": True,
                    "message": "Correctly handles 'YES', 'yes', etc. (case-insensitive)"
                })
                return True
            else:
                self.tests.append({
                    "name": "Case-insensitive photo input",
                    "passed": False,
                    "message": "Should handle photo input case-insensitively ('YES', 'yes', 'Yes')"
                })
                return False

        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Case-insensitive photo input",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Case-insensitive photo input",
                "passed": False,
                "message": f"Error running test: {e}"
            })
            return False

    def run_all_tests(self):
        """Run all tests and calculate score."""
        # Run all test methods
        self.test_file_exists()
        self.test_has_elif()
        self.test_has_logical_operator()
        self.test_height_rejection()
        self.test_child_ticket()
        self.test_youth_ticket()
        self.test_midlife_discount()
        self.test_adult_ticket()
        self.test_photo_addon()
        self.test_case_insensitive_photo()

        # Calculate score
        passed_count = sum(1 for test in self.tests if test['passed'])
        total_count = len(self.tests)

        self.passed = passed_count >= total_count * 0.75  # 75% to pass
        self.score = f"{passed_count}/{total_count} ({int(passed_count/total_count*100)}%)"

        message = "Excellent work! All tests passed!" if passed_count == total_count else \
                  "Good job! Most tests passed." if self.passed else \
                  "Keep working on it. Review the failed tests and try again."

        return {
            'passed': self.passed,
            'score': self.score,
            'tests': self.tests,
            'message': message
        }


def test_submission(filepath):
    """Main entry point for testing submissions."""
    tester = Module11Tester(filepath)
    return tester.run_all_tests()


if __name__ == '__main__':
    # For testing the tester itself
    if len(sys.argv) > 1:
        result = test_submission(sys.argv[1])
        print(f"Passed: {result['passed']}")
        print(f"Score: {result['score']}")
        print(f"Message: {result['message']}")
        print("\nDetailed Results:")
        for test in result['tests']:
            status = '✓' if test['passed'] else '✗'
            print(f"  {status} {test['name']}: {test['message']}")
    else:
        print("Usage: python module011_tester.py <submission_file.py>")
