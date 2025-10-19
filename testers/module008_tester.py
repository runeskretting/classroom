#!/usr/bin/env python3
"""
Module 8 Tester: Safe Calculator with Logging
Tests student submissions for error handling and exception management.
"""

import subprocess
import sys
import os
import ast
import tempfile
import shutil


class Module8Tester:
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

    def test_try_except_exists(self):
        """Test 2: Check if code contains try/except blocks"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            tree = ast.parse(code)

            # Look for Try nodes in the AST
            try_blocks = [node for node in ast.walk(tree) if isinstance(node, ast.Try)]

            if len(try_blocks) >= 1:
                self.tests.append({
                    "name": "try/except blocks present",
                    "passed": True,
                    "message": f"Found {len(try_blocks)} try/except block(s)"
                })
                return True
            else:
                self.tests.append({
                    "name": "try/except blocks present",
                    "passed": False,
                    "message": "No try/except blocks found - error handling required"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "try/except blocks present",
                "passed": False,
                "message": f"Error parsing code: {e}"
            })
            return False

    def test_valid_addition(self):
        """Test 3: Test valid addition calculation"""
        test_input = "5\n+\n3\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            # Check if output contains the result 8
            if '8' in output and result.returncode == 0:
                self.tests.append({
                    "name": "Valid addition (5 + 3)",
                    "passed": True,
                    "message": "Correctly calculated 5 + 3 = 8"
                })
                return True
            else:
                self.tests.append({
                    "name": "Valid addition (5 + 3)",
                    "passed": False,
                    "message": f"Expected result '8' in output, got: {result.stdout[:100]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Valid addition (5 + 3)",
                "passed": False,
                "message": "Program timed out - check for infinite loops"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Valid addition (5 + 3)",
                "passed": False,
                "message": f"Error running program: {e}"
            })
            return False

    def test_valid_division(self):
        """Test 4: Test valid division calculation"""
        test_input = "10\n/\n2\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()

            # Check if output contains the result 5 or 5.0
            if ('5' in output or '5.0' in output) and result.returncode == 0:
                self.tests.append({
                    "name": "Valid division (10 / 2)",
                    "passed": True,
                    "message": "Correctly calculated 10 / 2 = 5.0"
                })
                return True
            else:
                self.tests.append({
                    "name": "Valid division (10 / 2)",
                    "passed": False,
                    "message": f"Expected result '5' in output, got: {result.stdout[:100]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Valid division (10 / 2)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Valid division (10 / 2)",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_invalid_number_input(self):
        """Test 5: Test handling of invalid number input (ValueError)"""
        test_input = "abc\n+\n5\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            # Program should not crash (returncode should be 0 for graceful handling)
            # Or it might exit with error but shouldn't raise unhandled exception
            if 'traceback' not in result.stderr.lower() or result.returncode == 0:
                self.tests.append({
                    "name": "Handle invalid input (ValueError)",
                    "passed": True,
                    "message": "Program handled invalid input without crashing"
                })
                return True
            else:
                self.tests.append({
                    "name": "Handle invalid input (ValueError)",
                    "passed": False,
                    "message": f"Program crashed with unhandled exception: {result.stderr[:200]}"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Handle invalid input (ValueError)",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Handle invalid input (ValueError)",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_division_by_zero(self):
        """Test 6: Test handling of division by zero (ZeroDivisionError)"""
        test_input = "10\n/\n0\n"
        try:
            result = subprocess.run(
                [sys.executable, self.submission_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.lower()
            error_output = result.stderr.lower()

            # Should not crash with traceback
            # Should show some error message about division by zero
            if 'traceback' not in error_output and ('zero' in output or 'error' in output or 'cannot' in output):
                self.tests.append({
                    "name": "Handle division by zero",
                    "passed": True,
                    "message": "Program handled division by zero gracefully"
                })
                return True
            elif 'traceback' in error_output:
                self.tests.append({
                    "name": "Handle division by zero",
                    "passed": False,
                    "message": "Program crashed - need to catch ZeroDivisionError"
                })
                return False
            else:
                self.tests.append({
                    "name": "Handle division by zero",
                    "passed": False,
                    "message": "Program didn't show clear error message for division by zero"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Handle division by zero",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Handle division by zero",
                "passed": False,
                "message": f"Error: {e}"
            })
            return False

    def test_log_file_creation(self):
        """Test 7: Test that log file is created"""
        # Create a temporary directory for testing
        temp_dir = tempfile.mkdtemp()
        temp_submission = os.path.join(temp_dir, 'test_calc.py')

        try:
            # Copy submission to temp directory
            shutil.copy2(self.submission_path, temp_submission)

            # Run the program from temp directory
            test_input = "5\n+\n3\n"
            result = subprocess.run(
                [sys.executable, temp_submission],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=temp_dir
            )

            # Check if log file was created
            log_file = os.path.join(temp_dir, 'calculator_log.txt')
            if os.path.exists(log_file):
                # Check if log file has content
                with open(log_file, 'r') as f:
                    content = f.read()
                if len(content) > 0:
                    self.tests.append({
                        "name": "Log file creation",
                        "passed": True,
                        "message": "calculator_log.txt created and has content"
                    })
                    return True
                else:
                    self.tests.append({
                        "name": "Log file creation",
                        "passed": False,
                        "message": "Log file created but is empty"
                    })
                    return False
            else:
                self.tests.append({
                    "name": "Log file creation",
                    "passed": False,
                    "message": "calculator_log.txt was not created"
                })
                return False
        except subprocess.TimeoutExpired:
            self.tests.append({
                "name": "Log file creation",
                "passed": False,
                "message": "Program timed out"
            })
            return False
        except Exception as e:
            self.tests.append({
                "name": "Log file creation",
                "passed": False,
                "message": f"Error testing log file: {e}"
            })
            return False
        finally:
            # Cleanup temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_specific_exception_handling(self):
        """Test 8: Check for specific exception types (not bare except)"""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            tree = ast.parse(code)

            # Look for Try nodes
            try_blocks = [node for node in ast.walk(tree) if isinstance(node, ast.Try)]

            has_specific_handler = False
            has_bare_except = False

            for try_node in try_blocks:
                for handler in try_node.handlers:
                    if handler.type is None:
                        # Bare except
                        has_bare_except = True
                    else:
                        # Specific exception
                        has_specific_handler = True

            if has_specific_handler:
                if has_bare_except:
                    self.tests.append({
                        "name": "Specific exception handling",
                        "passed": True,
                        "message": "Uses specific exception types (but also has bare except - consider being more specific)"
                    })
                else:
                    self.tests.append({
                        "name": "Specific exception handling",
                        "passed": True,
                        "message": "Uses specific exception types (good practice!)"
                    })
                return True
            else:
                self.tests.append({
                    "name": "Specific exception handling",
                    "passed": False,
                    "message": "Only uses bare except - use specific exceptions like ValueError, ZeroDivisionError"
                })
                return False
        except Exception as e:
            self.tests.append({
                "name": "Specific exception handling",
                "passed": False,
                "message": f"Error analyzing code: {e}"
            })
            return False

    def test_no_crash_multiple_errors(self):
        """Test 9: Ensure program doesn't crash with various bad inputs"""
        test_cases = [
            ("xyz\n*\n5\n", "invalid first number"),
            ("10\n-\nabc\n", "invalid second number"),
            ("5.5\n+\n2.3\n", "float inputs"),
        ]

        all_passed = True
        messages = []

        for test_input, description in test_cases:
            try:
                result = subprocess.run(
                    [sys.executable, self.submission_path],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if 'traceback' in result.stderr.lower() and result.returncode != 0:
                    all_passed = False
                    messages.append(f"Crashed on {description}")
            except subprocess.TimeoutExpired:
                all_passed = False
                messages.append(f"Timeout on {description}")
            except Exception as e:
                all_passed = False
                messages.append(f"Error on {description}: {e}")

        if all_passed:
            self.tests.append({
                "name": "Robustness (no crashes)",
                "passed": True,
                "message": "Program handles various error conditions without crashing"
            })
            return True
        else:
            self.tests.append({
                "name": "Robustness (no crashes)",
                "passed": False,
                "message": f"Program crashed in some cases: {', '.join(messages)}"
            })
            return False

    def run_all_tests(self):
        """Run all tests and calculate score"""
        print(f"\n{'='*60}")
        print(f"Testing Module 8: Safe Calculator with Logging")
        print(f"{'='*60}\n")

        # Run all tests
        self.test_file_exists()
        self.test_try_except_exists()
        self.test_valid_addition()
        self.test_valid_division()
        self.test_invalid_number_input()
        self.test_division_by_zero()
        self.test_log_file_creation()
        self.test_specific_exception_handling()
        self.test_no_crash_multiple_errors()

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
    tester = Module8Tester(filepath)
    tester.run_all_tests()

    return {
        'passed': tester.passed,
        'score': tester.score,
        'tests': tester.tests,
        'message': 'Great job! Your calculator handles errors gracefully.' if tester.passed
                   else 'Keep working on error handling. Make sure to use try/except blocks and handle different exception types.'
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python module008_tester.py <path_to_submission>")
        sys.exit(1)

    result = test_submission(sys.argv[1])
    print(f"\nFinal Result: {'PASSED' if result['passed'] else 'FAILED'}")
    print(f"Score: {result['score']}")
    print(f"Message: {result['message']}")
