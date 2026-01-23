"""
End-to-end validation script for the Todo Full-Stack Web Application.

This script performs comprehensive end-to-end validation based on the quickstart scenarios
to ensure all functionality works as expected.
"""

import os
import sys
import time
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Add the backend src directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.user import User
from models.todo import Todo
from database.session import get_session


@dataclass
class ValidationResult:
    """Result of a validation step."""
    name: str
    passed: bool
    details: str
    duration: float = 0.0


class E2EValidator:
    """End-to-end validator for the Todo application."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results: list[ValidationResult] = []
        self.auth_token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.todo_ids: list[str] = []

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request with optional authentication."""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})

        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        kwargs['headers'] = headers
        start_time = time.time()

        response = self.session.request(method, url, **kwargs)
        duration = time.time() - start_time

        return response, duration

    def validate_api_availability(self) -> ValidationResult:
        """Validate that the API is accessible."""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health/ping")
            duration = time.time() - start_time

            if response.status_code == 200:
                result = ValidationResult(
                    name="API Availability",
                    passed=True,
                    details="API is accessible and responding to requests",
                    duration=duration
                )
            else:
                result = ValidationResult(
                    name="API Availability",
                    passed=False,
                    details=f"API returned status code {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="API Availability",
                passed=False,
                details=f"API is not accessible: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_user_registration(self) -> ValidationResult:
        """Validate user registration functionality."""
        start_time = time.time()
        try:
            # Register a new user
            user_data = {
                "email": "e2e_test@example.com",
                "password": "SecurePass123!"
            }

            response, duration = self._make_request('POST', '/auth/register', json=user_data)

            if response.status_code == 200:
                user_info = response.json()
                self.user_id = user_info.get('id')

                result = ValidationResult(
                    name="User Registration",
                    passed=True,
                    details=f"User registered successfully with ID: {self.user_id}",
                    duration=duration
                )
            else:
                result = ValidationResult(
                    name="User Registration",
                    passed=False,
                    details=f"Registration failed with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="User Registration",
                passed=False,
                details=f"Registration failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_user_login(self) -> ValidationResult:
        """Validate user login functionality."""
        start_time = time.time()
        try:
            # Login with the registered user
            login_data = {
                "email": "e2e_test@example.com",
                "password": "SecurePass123!"
            }

            response, duration = self._make_request('POST', '/auth/login', json=login_data)

            if response.status_code == 200:
                token_data = response.json()
                self.auth_token = token_data.get('access_token')

                if self.auth_token:
                    result = ValidationResult(
                        name="User Login",
                        passed=True,
                        details="User logged in successfully, token received",
                        duration=duration
                    )
                else:
                    result = ValidationResult(
                        name="User Login",
                        passed=False,
                        details="Login successful but no token received",
                        duration=duration
                    )
            else:
                result = ValidationResult(
                    name="User Login",
                    passed=False,
                    details=f"Login failed with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="User Login",
                passed=False,
                details=f"Login failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_get_current_user(self) -> ValidationResult:
        """Validate getting current user information."""
        start_time = time.time()
        try:
            response, duration = self._make_request('GET', '/auth/me')

            if response.status_code == 200:
                user_info = response.json()
                if user_info.get('email') == 'e2e_test@example.com':
                    result = ValidationResult(
                        name="Get Current User",
                        passed=True,
                        details="Successfully retrieved current user information",
                        duration=duration
                    )
                else:
                    result = ValidationResult(
                        name="Get Current User",
                        passed=False,
                        details=f"Retrieved user doesn't match expected: {user_info.get('email')}",
                        duration=duration
                    )
            else:
                result = ValidationResult(
                    name="Get Current User",
                    passed=False,
                    details=f"Failed to get user info with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="Get Current User",
                passed=False,
                details=f"Failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_create_todo(self) -> ValidationResult:
        """Validate creating a new todo."""
        start_time = time.time()
        try:
            todo_data = {
                "title": "E2E Test Todo",
                "description": "This is a test todo created during end-to-end validation"
            }

            response, duration = self._make_request('POST', '/todos/', json=todo_data)

            if response.status_code == 200:
                todo_info = response.json()
                todo_id = todo_info.get('id')
                self.todo_ids.append(todo_id)

                result = ValidationResult(
                    name="Create Todo",
                    passed=True,
                    details=f"Todo created successfully with ID: {todo_id}",
                    duration=duration
                )
            else:
                result = ValidationResult(
                    name="Create Todo",
                    passed=False,
                    details=f"Failed to create todo with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="Create Todo",
                passed=False,
                details=f"Failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_get_todos(self) -> ValidationResult:
        """Validate getting all todos for the current user."""
        start_time = time.time()
        try:
            response, duration = self._make_request('GET', '/todos/')

            if response.status_code == 200:
                todos = response.json()
                if len(todos) >= 1:
                    result = ValidationResult(
                        name="Get Todos",
                        passed=True,
                        details=f"Successfully retrieved {len(todos)} todos",
                        duration=duration
                    )
                else:
                    result = ValidationResult(
                        name="Get Todos",
                        passed=False,
                        details="No todos found for the user",
                        duration=duration
                    )
            else:
                result = ValidationResult(
                    name="Get Todos",
                    passed=False,
                    details=f"Failed to get todos with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="Get Todos",
                passed=False,
                details=f"Failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_update_todo(self) -> ValidationResult:
        """Validate updating an existing todo."""
        if not self.todo_ids:
            result = ValidationResult(
                name="Update Todo",
                passed=False,
                details="No todos available to update",
                duration=0.0
            )
            self.results.append(result)
            return result

        start_time = time.time()
        try:
            todo_id = self.todo_ids[0]
            update_data = {
                "title": "Updated E2E Test Todo",
                "description": "This todo has been updated during end-to-end validation",
                "completed": True
            }

            response, duration = self._make_request('PUT', f'/todos/{todo_id}', json=update_data)

            if response.status_code == 200:
                updated_todo = response.json()
                if (updated_todo.get('title') == "Updated E2E Test Todo" and
                    updated_todo.get('completed') is True):
                    result = ValidationResult(
                        name="Update Todo",
                        passed=True,
                        details=f"Todo {todo_id} updated successfully",
                        duration=duration
                    )
                else:
                    result = ValidationResult(
                        name="Update Todo",
                        passed=False,
                        details=f"Todo update didn't return expected values: {updated_todo}",
                        duration=duration
                    )
            else:
                result = ValidationResult(
                    name="Update Todo",
                    passed=False,
                    details=f"Failed to update todo with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="Update Todo",
                passed=False,
                details=f"Failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_toggle_todo_completion(self) -> ValidationResult:
        """Validate toggling todo completion status."""
        if not self.todo_ids:
            result = ValidationResult(
                name="Toggle Todo Completion",
                passed=False,
                details="No todos available to toggle",
                duration=0.0
            )
            self.results.append(result)
            return result

        start_time = time.time()
        try:
            todo_id = self.todo_ids[0]
            toggle_data = {"completed": False}  # Toggle back to incomplete

            response, duration = self._make_request('PATCH', f'/todos/{todo_id}/toggle', json=toggle_data)

            if response.status_code == 200:
                toggled_todo = response.json()
                if toggled_todo.get('completed') is False:
                    result = ValidationResult(
                        name="Toggle Todo Completion",
                        passed=True,
                        details=f"Todo {todo_id} completion toggled successfully",
                        duration=duration
                    )
                else:
                    result = ValidationResult(
                        name="Toggle Todo Completion",
                        passed=False,
                        details=f"Todo toggle didn't return expected completion status: {toggled_todo}",
                        duration=duration
                    )
            else:
                result = ValidationResult(
                    name="Toggle Todo Completion",
                    passed=False,
                    details=f"Failed to toggle todo with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="Toggle Todo Completion",
                passed=False,
                details=f"Failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_delete_todo(self) -> ValidationResult:
        """Validate deleting a todo."""
        if not self.todo_ids:
            result = ValidationResult(
                name="Delete Todo",
                passed=False,
                details="No todos available to delete",
                duration=0.0
            )
            self.results.append(result)
            return result

        start_time = time.time()
        try:
            todo_id = self.todo_ids[0]

            response, duration = self._make_request('DELETE', f'/todos/{todo_id}')

            if response.status_code == 204:
                result = ValidationResult(
                    name="Delete Todo",
                    passed=True,
                    details=f"Todo {todo_id} deleted successfully",
                    duration=duration
                )
                # Remove from our list since it's deleted
                self.todo_ids.remove(todo_id)
            else:
                result = ValidationResult(
                    name="Delete Todo",
                    passed=False,
                    details=f"Failed to delete todo with status {response.status_code}: {response.text}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start_time
            result = ValidationResult(
                name="Delete Todo",
                passed=False,
                details=f"Failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def validate_data_isolation(self) -> ValidationResult:
        """Validate that user data is properly isolated."""
        start_time = time.time()
        try:
            # Create a second user
            second_user_data = {
                "email": "e2e_test2@example.com",
                "password": "SecurePass456!"
            }

            response, _ = self._make_request('POST', '/auth/register', json=second_user_data)
            if response.status_code != 200:
                result = ValidationResult(
                    name="Data Isolation",
                    passed=False,
                    details="Failed to create second user for data isolation test",
                    duration=time.time() - start_time
                )
                self.results.append(result)
                return result

            # Login as second user
            login_data = {
                "email": "e2e_test2@example.com",
                "password": "SecurePass456!"
            }

            response, _ = self._make_request('POST', '/auth/login', json=login_data)
            if response.status_code != 200:
                result = ValidationResult(
                    name="Data Isolation",
                    passed=False,
                    details="Failed to login as second user",
                    duration=time.time() - start_time
                )
                self.results.append(result)
                return result

            second_user_token = response.json().get('access_token')
            if not second_user_token:
                result = ValidationResult(
                    name="Data Isolation",
                    passed=False,
                    details="No token received for second user",
                    duration=time.time() - start_time
                )
                self.results.append(result)
                return result

            # Try to access the first user's todo (should fail)
            original_token = self.auth_token
            self.auth_token = second_user_token

            if self.todo_ids:  # If we still have any todos
                first_todo_id = self.todo_ids[0] if self.todo_ids else None
                if first_todo_id:
                    response, duration = self._make_request('GET', f'/todos/{first_todo_id}')

                    # Should either return 404 (not found) or 403 (forbidden) for proper data isolation
                    if response.status_code in [404, 403]:
                        # Switch back to original user
                        self.auth_token = original_token
                        result = ValidationResult(
                            name="Data Isolation",
                            passed=True,
                            details="User data isolation is properly enforced",
                            duration=duration
                        )
                    else:
                        # Switch back to original user
                        self.auth_token = original_token
                        result = ValidationResult(
                            name="Data Isolation",
                            passed=False,
                            details=f"Data isolation failed - second user could access first user's todo (status: {response.status_code})",
                            duration=duration
                        )
                else:
                    # Switch back to original user
                    self.auth_token = original_token
                    result = ValidationResult(
                        name="Data Isolation",
                        passed=False,
                        details="No todos available to test data isolation",
                        duration=time.time() - start_time
                    )
            else:
                # Switch back to original user
                self.auth_token = original_token
                result = ValidationResult(
                    name="Data Isolation",
                    passed=False,
                    details="No todos available to test data isolation",
                    duration=time.time() - start_time
                )
        except Exception as e:
            # Switch back to original user in case of exception
            self.auth_token = original_token
            duration = time.time() - start_time
            result = ValidationResult(
                name="Data Isolation",
                passed=False,
                details=f"Failed with exception: {str(e)}",
                duration=duration
            )

        self.results.append(result)
        return result

    def run_all_validations(self) -> Dict[str, Any]:
        """Run all validation steps and return a summary."""
        print("Starting end-to-end validation...")

        # Run validations in order
        validations = [
            self.validate_api_availability,
            self.validate_user_registration,
            self.validate_user_login,
            self.validate_get_current_user,
            self.validate_create_todo,
            self.validate_get_todos,
            self.validate_update_todo,
            self.validate_toggle_todo_completion,
            self.validate_delete_todo,
            self.validate_data_isolation,
        ]

        for validation in validations:
            result = validation()
            status = "PASS" if result.passed else "FAIL"
            print(f"{status}: {result.name} ({result.duration:.3f}s)")

        # Calculate summary
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests

        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "details": r.details,
                    "duration": r.duration
                } for r in self.results
            ]
        }

        return summary

    def print_detailed_results(self):
        """Print detailed results of all validations."""
        print("\n" + "="*60)
        print("DETAILED VALIDATION RESULTS")
        print("="*60)

        for i, result in enumerate(self.results, 1):
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"\n{i}. {result.name}")
            print(f"   Status: {status}")
            print(f"   Duration: {result.duration:.3f}s")
            print(f"   Details: {result.details}")

        # Print summary
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)

        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")


def main():
    """Main function to run the end-to-end validation."""
    validator = E2EValidator()
    summary = validator.run_all_validations()
    validator.print_detailed_results()

    # Exit with error code if any tests failed
    if summary['failed_tests'] > 0:
        print(f"\nValidation failed: {summary['failed_tests']} test(s) failed.")
        sys.exit(1)
    else:
        print(f"\nAll validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()