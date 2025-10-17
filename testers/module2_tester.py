"""
Module 2 Tester: Contact Book Application
Tests student submissions for the Module 2 capstone project.
"""

import subprocess
import sys
import os
import tempfile
import shutil
import time


class Module2Tester:
    def __init__(self, submission_path):
        self.submission_path = submission_path
        self.test_results = []
        self.passed = False
        self.temp_dir = tempfile.mkdtemp()

    def cleanup(self):
        """Clean up temporary directory."""
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def test_code_structure(self):
        """Test if the code contains necessary structures."""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            checks = {
                'def keyword (functions)': 'def ' in code,
                'with statement (file handling)': 'with open(' in code or 'with open (' in code,
                'try/except blocks': 'try:' in code and 'except' in code,
                'while loop': 'while' in code,
                'dictionary usage': '{' in code and ':' in code,
                'file operations': any(mode in code for mode in ['"r"', '"w"', '"a"', "'r'", "'w'", "'a'"])
            }

            for check_name, passed in checks.items():
                self.test_results.append({
                    'test': f'Contains {check_name}',
                    'passed': passed,
                    'message': f'Code {"contains" if passed else "missing"} {check_name}'
                })

            return sum(checks.values()) >= 5  # At least 5 out of 6

        except Exception as e:
            self.test_results.append({
                'test': 'Code structure check',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_function_definitions(self):
        """Test if required functions are defined."""
        try:
            with open(self.submission_path, 'r') as f:
                code = f.read()

            # Look for common function names from the solution
            expected_functions = ['add_contact', 'search_contact', 'list_contacts', 'load_contacts', 'save_contacts']
            found_functions = []

            for func in expected_functions:
                if f'def {func}' in code:
                    found_functions.append(func)

            if len(found_functions) >= 4:  # At least 4 functions
                self.test_results.append({
                    'test': 'Function definitions',
                    'passed': True,
                    'message': f'Found {len(found_functions)} functions: {", ".join(found_functions)}'
                })
                return True
            else:
                self.test_results.append({
                    'test': 'Function definitions',
                    'passed': False,
                    'message': f'Expected at least 4 functions, found {len(found_functions)}'
                })
                return False

        except Exception as e:
            self.test_results.append({
                'test': 'Function definitions',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_add_contact(self):
        """Test adding a contact."""
        try:
            # Copy the script to temp directory
            temp_script = os.path.join(self.temp_dir, 'contact_book.py')
            shutil.copy(self.submission_path, temp_script)

            # Test adding a contact and exiting
            test_input = "1\nAlice\n555-1234\n4\n"

            result = subprocess.run(
                [sys.executable, temp_script],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.temp_dir
            )

            # Check if a contacts file was created
            possible_files = ['contacts.txt', 'contacts.csv', 'contact_book.txt']
            contact_file = None

            for filename in possible_files:
                filepath = os.path.join(self.temp_dir, filename)
                if os.path.exists(filepath):
                    contact_file = filepath
                    break

            if contact_file and os.path.exists(contact_file):
                with open(contact_file, 'r') as f:
                    content = f.read()

                if 'Alice' in content and '555-1234' in content:
                    self.test_results.append({
                        'test': 'Add contact functionality',
                        'passed': True,
                        'message': 'Successfully adds and saves contacts'
                    })
                    return True
                else:
                    self.test_results.append({
                        'test': 'Add contact functionality',
                        'passed': False,
                        'message': 'Contact was not saved correctly'
                    })
                    return False
            else:
                self.test_results.append({
                    'test': 'Add contact functionality',
                    'passed': False,
                    'message': 'No contacts file was created'
                })
                return False

        except subprocess.TimeoutExpired:
            self.test_results.append({
                'test': 'Add contact functionality',
                'passed': False,
                'message': 'Program timed out - possible infinite loop'
            })
            return False
        except Exception as e:
            self.test_results.append({
                'test': 'Add contact functionality',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_persistence(self):
        """Test that contacts persist across program runs."""
        try:
            temp_script = os.path.join(self.temp_dir, 'contact_book.py')

            # Run 1: Add Alice
            test_input1 = "1\nAlice\n555-1234\n4\n"
            subprocess.run(
                [sys.executable, temp_script],
                input=test_input1,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.temp_dir
            )

            # Run 2: Add Bob and list contacts
            test_input2 = "1\nBob\n555-5678\n3\n4\n"
            result2 = subprocess.run(
                [sys.executable, temp_script],
                input=test_input2,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.temp_dir
            )

            output = result2.stdout

            # Check if both contacts are listed
            if 'Alice' in output and 'Bob' in output:
                self.test_results.append({
                    'test': 'Data persistence',
                    'passed': True,
                    'message': 'Contacts persist across program runs'
                })
                return True
            else:
                self.test_results.append({
                    'test': 'Data persistence',
                    'passed': False,
                    'message': 'Contacts do not persist correctly'
                })
                return False

        except Exception as e:
            self.test_results.append({
                'test': 'Data persistence',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_search_functionality(self):
        """Test searching for a contact."""
        try:
            temp_script = os.path.join(self.temp_dir, 'contact_book.py')

            # Add a contact, then search for it
            test_input = "1\nCharlie\n555-9999\n2\nCharlie\n4\n"

            result = subprocess.run(
                [sys.executable, temp_script],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.temp_dir
            )

            output = result.stdout.lower()

            # Check if search was successful
            if ('charlie' in output or 'Charlie' in result.stdout) and '555-9999' in result.stdout:
                self.test_results.append({
                    'test': 'Search functionality',
                    'passed': True,
                    'message': 'Successfully searches and finds contacts'
                })
                return True
            else:
                self.test_results.append({
                    'test': 'Search functionality',
                    'passed': False,
                    'message': 'Search does not work correctly'
                })
                return False

        except Exception as e:
            self.test_results.append({
                'test': 'Search functionality',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def test_menu_system(self):
        """Test that the menu system works."""
        try:
            temp_script = os.path.join(self.temp_dir, 'contact_book.py')

            # Just run the program and exit
            test_input = "4\n"

            result = subprocess.run(
                [sys.executable, temp_script],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.temp_dir
            )

            output = result.stdout.lower()

            # Check if menu options are displayed
            menu_indicators = ['1', '2', '3', '4', 'menu', 'add', 'search', 'list', 'exit']
            has_menu = sum(1 for indicator in menu_indicators if indicator in output) >= 6

            if has_menu and result.returncode == 0:
                self.test_results.append({
                    'test': 'Menu system',
                    'passed': True,
                    'message': 'Menu displays correctly and program can exit'
                })
                return True
            else:
                self.test_results.append({
                    'test': 'Menu system',
                    'passed': False,
                    'message': 'Menu does not display properly'
                })
                return False

        except Exception as e:
            self.test_results.append({
                'test': 'Menu system',
                'passed': False,
                'message': f'Error: {str(e)}'
            })
            return False

    def run_all_tests(self):
        """Run all tests and return results."""
        try:
            structure_ok = self.test_code_structure()
            functions_ok = self.test_function_definitions()
            menu_ok = self.test_menu_system()
            add_ok = self.test_add_contact()
            persistence_ok = self.test_persistence()
            search_ok = self.test_search_functionality()

            # Calculate overall pass/fail
            passed_count = sum(1 for result in self.test_results if result['passed'])
            total_count = len(self.test_results)

            self.passed = passed_count >= total_count * 0.70  # 70% pass rate

            return {
                'passed': self.passed,
                'score': f'{passed_count}/{total_count}',
                'percentage': int((passed_count / total_count) * 100),
                'tests': self.test_results,
                'message': 'All tests passed! Your contact book application works correctly.' if self.passed
                          else 'Some tests failed. Please review the feedback and try again.'
            }

        finally:
            self.cleanup()


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

    tester = Module2Tester(submission_path)
    return tester.run_all_tests()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python module2_tester.py <submission_path>")
        sys.exit(1)

    result = test_submission(sys.argv[1])
    print(f"\nTest Results:")
    print(f"Score: {result['score']} ({result['percentage']}%)")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}\n")

    for test in result['tests']:
        status = '✓' if test['passed'] else '✗'
        print(f"{status} {test['test']}: {test['message']}")

    print(f"\n{result['message']}")
