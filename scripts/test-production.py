#!/usr/bin/env python3
"""
Production Deployment Testing Script
Author: Sharmeen Asif

Tests the production deployment by running through common user workflows.
"""

import asyncio
import httpx
import sys
from typing import Optional, Dict, Any
from datetime import datetime
import json

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class ProductionTester:
    """Tests production deployment end-to-end"""

    def __init__(self, api_url: str, frontend_url: str):
        self.api_url = api_url.rstrip("/")
        self.frontend_url = frontend_url.rstrip("/")
        self.session_token: Optional[str] = None
        self.test_user_email = f"test_{datetime.now().timestamp()}@example.com"
        self.test_user_password = "TestPassword123!"
        self.created_task_ids: list = []

        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def log_test(self, name: str, status: str, message: str = ""):
        """Log test result"""
        if status == "PASS":
            print(f"{GREEN}✓{RESET} {name}")
            if message:
                print(f"  {message}")
            self.passed += 1
        elif status == "FAIL":
            print(f"{RED}✗{RESET} {name}")
            if message:
                print(f"  {RED}{message}{RESET}")
            self.failed += 1
        elif status == "WARN":
            print(f"{YELLOW}⚠{RESET} {name}")
            if message:
                print(f"  {YELLOW}{message}{RESET}")
            self.warnings += 1

    async def test_api_health(self) -> bool:
        """Test API health endpoint"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_url}/")

                if response.status_code == 200:
                    data = response.json()
                    self.log_test(
                        "API Health Check",
                        "PASS",
                        f"Status: {response.status_code}, Message: {data.get('message', 'N/A')}"
                    )
                    return True
                else:
                    self.log_test(
                        "API Health Check",
                        "FAIL",
                        f"Expected 200, got {response.status_code}"
                    )
                    return False
        except Exception as e:
            self.log_test("API Health Check", "FAIL", str(e))
            return False

    async def test_api_docs(self) -> bool:
        """Test OpenAPI documentation is accessible"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_url}/docs")

                if response.status_code == 200:
                    self.log_test(
                        "API Documentation",
                        "PASS",
                        f"Docs available at {self.api_url}/docs"
                    )
                    return True
                else:
                    self.log_test(
                        "API Documentation",
                        "FAIL",
                        f"Expected 200, got {response.status_code}"
                    )
                    return False
        except Exception as e:
            self.log_test("API Documentation", "FAIL", str(e))
            return False

    async def test_user_signup(self) -> bool:
        """Test user registration"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.api_url}/api/auth/signup",
                    json={
                        "email": self.test_user_email,
                        "password": self.test_user_password,
                        "full_name": "Production Test User"
                    }
                )

                if response.status_code == 201:
                    data = response.json()
                    self.log_test(
                        "User Registration",
                        "PASS",
                        f"Created user: {data.get('email', 'N/A')}"
                    )
                    return True
                else:
                    self.log_test(
                        "User Registration",
                        "FAIL",
                        f"Expected 201, got {response.status_code}: {response.text}"
                    )
                    return False
        except Exception as e:
            self.log_test("User Registration", "FAIL", str(e))
            return False

    async def test_user_signin(self) -> bool:
        """Test user authentication"""
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.post(
                    f"{self.api_url}/api/auth/signin",
                    json={
                        "email": self.test_user_email,
                        "password": self.test_user_password,
                        "remember_me": False
                    }
                )

                if response.status_code == 200:
                    # Get session token from cookies
                    self.session_token = response.cookies.get("session_token")

                    if self.session_token:
                        self.log_test(
                            "User Sign In",
                            "PASS",
                            f"Authenticated with session token (length: {len(self.session_token)})"
                        )
                        return True
                    else:
                        self.log_test(
                            "User Sign In",
                            "FAIL",
                            "No session_token cookie returned"
                        )
                        return False
                else:
                    self.log_test(
                        "User Sign In",
                        "FAIL",
                        f"Expected 200, got {response.status_code}: {response.text}"
                    )
                    return False
        except Exception as e:
            self.log_test("User Sign In", "FAIL", str(e))
            return False

    async def test_create_task(self) -> bool:
        """Test task creation"""
        if not self.session_token:
            self.log_test("Create Task", "FAIL", "No session token available")
            return False

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.api_url}/api/tasks",
                    json={
                        "title": "Test task from production test",
                        "completed": False
                    },
                    cookies={"session_token": self.session_token}
                )

                if response.status_code == 201:
                    data = response.json()
                    task_id = data.get("id")
                    self.created_task_ids.append(task_id)

                    self.log_test(
                        "Create Task",
                        "PASS",
                        f"Created task ID: {task_id}, Title: {data.get('title', 'N/A')}"
                    )
                    return True
                else:
                    self.log_test(
                        "Create Task",
                        "FAIL",
                        f"Expected 201, got {response.status_code}: {response.text}"
                    )
                    return False
        except Exception as e:
            self.log_test("Create Task", "FAIL", str(e))
            return False

    async def test_list_tasks(self) -> bool:
        """Test listing tasks"""
        if not self.session_token:
            self.log_test("List Tasks", "FAIL", "No session token available")
            return False

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.api_url}/api/tasks",
                    cookies={"session_token": self.session_token}
                )

                if response.status_code == 200:
                    data = response.json()
                    task_count = len(data)

                    self.log_test(
                        "List Tasks",
                        "PASS",
                        f"Retrieved {task_count} task(s)"
                    )
                    return True
                else:
                    self.log_test(
                        "List Tasks",
                        "FAIL",
                        f"Expected 200, got {response.status_code}"
                    )
                    return False
        except Exception as e:
            self.log_test("List Tasks", "FAIL", str(e))
            return False

    async def test_update_task(self) -> bool:
        """Test task update"""
        if not self.session_token or not self.created_task_ids:
            self.log_test("Update Task", "FAIL", "No task available to update")
            return False

        task_id = self.created_task_ids[0]

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(
                    f"{self.api_url}/api/tasks/{task_id}",
                    json={
                        "title": "Updated task from production test",
                        "completed": True
                    },
                    cookies={"session_token": self.session_token}
                )

                if response.status_code == 200:
                    data = response.json()
                    self.log_test(
                        "Update Task",
                        "PASS",
                        f"Updated task {task_id}: {data.get('title', 'N/A')}, Completed: {data.get('completed', False)}"
                    )
                    return True
                else:
                    self.log_test(
                        "Update Task",
                        "FAIL",
                        f"Expected 200, got {response.status_code}"
                    )
                    return False
        except Exception as e:
            self.log_test("Update Task", "FAIL", str(e))
            return False

    async def test_delete_task(self) -> bool:
        """Test task deletion"""
        if not self.session_token or not self.created_task_ids:
            self.log_test("Delete Task", "FAIL", "No task available to delete")
            return False

        task_id = self.created_task_ids[0]

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(
                    f"{self.api_url}/api/tasks/{task_id}",
                    cookies={"session_token": self.session_token}
                )

                if response.status_code == 204:
                    self.log_test(
                        "Delete Task",
                        "PASS",
                        f"Deleted task {task_id}"
                    )
                    return True
                else:
                    self.log_test(
                        "Delete Task",
                        "FAIL",
                        f"Expected 204, got {response.status_code}"
                    )
                    return False
        except Exception as e:
            self.log_test("Delete Task", "FAIL", str(e))
            return False

    async def test_cors(self) -> bool:
        """Test CORS headers"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.options(
                    f"{self.api_url}/api/tasks",
                    headers={"Origin": self.frontend_url}
                )

                cors_header = response.headers.get("access-control-allow-origin")

                if cors_header:
                    if cors_header == self.frontend_url or cors_header == "*":
                        self.log_test(
                            "CORS Configuration",
                            "PASS",
                            f"CORS allows origin: {cors_header}"
                        )
                        return True
                    else:
                        self.log_test(
                            "CORS Configuration",
                            "WARN",
                            f"CORS allows {cors_header}, expected {self.frontend_url}"
                        )
                        return True
                else:
                    self.log_test(
                        "CORS Configuration",
                        "WARN",
                        "No CORS headers found (may cause frontend issues)"
                    )
                    return True
        except Exception as e:
            self.log_test("CORS Configuration", "WARN", str(e))
            return True  # Don't fail on CORS check

    async def test_response_time(self) -> bool:
        """Test API response time"""
        try:
            import time
            start = time.time()

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_url}/")

            elapsed = (time.time() - start) * 1000  # Convert to ms

            if elapsed < 500:
                self.log_test(
                    "Response Time",
                    "PASS",
                    f"{elapsed:.0f}ms (excellent)"
                )
            elif elapsed < 1000:
                self.log_test(
                    "Response Time",
                    "PASS",
                    f"{elapsed:.0f}ms (good)"
                )
            elif elapsed < 2000:
                self.log_test(
                    "Response Time",
                    "WARN",
                    f"{elapsed:.0f}ms (acceptable, but could be faster)"
                )
            else:
                self.log_test(
                    "Response Time",
                    "WARN",
                    f"{elapsed:.0f}ms (slow, investigate performance)"
                )

            return True
        except Exception as e:
            self.log_test("Response Time", "FAIL", str(e))
            return False

    async def run_all_tests(self):
        """Run all production tests"""
        print(f"{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}Production Deployment Test Suite{RESET}")
        print(f"{BLUE}{'='*70}{RESET}\n")
        print(f"API URL: {self.api_url}")
        print(f"Frontend URL: {self.frontend_url}")
        print(f"Test User: {self.test_user_email}\n")

        print(f"{BLUE}Running Tests...{RESET}\n")

        # Infrastructure tests
        print(f"{BLUE}[Infrastructure Tests]{RESET}")
        await self.test_api_health()
        await self.test_api_docs()
        await self.test_response_time()
        print()

        # Authentication tests
        print(f"{BLUE}[Authentication Tests]{RESET}")
        if not await self.test_user_signup():
            print(f"{RED}Cannot continue without user signup{RESET}")
            return

        if not await self.test_user_signin():
            print(f"{RED}Cannot continue without user signin{RESET}")
            return
        print()

        # CRUD tests
        print(f"{BLUE}[CRUD Operation Tests]{RESET}")
        await self.test_create_task()
        await self.test_list_tasks()
        await self.test_update_task()
        await self.test_delete_task()
        print()

        # Configuration tests
        print(f"{BLUE}[Configuration Tests]{RESET}")
        await self.test_cors()
        print()

        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed + self.warnings

        print(f"{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}Test Summary{RESET}")
        print(f"{BLUE}{'='*70}{RESET}\n")

        print(f"{GREEN}✓ Passed:  {self.passed}/{total}{RESET}")
        if self.warnings > 0:
            print(f"{YELLOW}⚠ Warnings: {self.warnings}/{total}{RESET}")
        if self.failed > 0:
            print(f"{RED}✗ Failed:  {self.failed}/{total}{RESET}")

        print()

        if self.failed == 0:
            print(f"{GREEN}{'='*70}{RESET}")
            print(f"{GREEN}✓ All critical tests passed! Production deployment is working.{RESET}")
            print(f"{GREEN}{'='*70}{RESET}")
            return 0
        else:
            print(f"{RED}{'='*70}{RESET}")
            print(f"{RED}✗ {self.failed} test(s) failed. Review errors above.{RESET}")
            print(f"{RED}{'='*70}{RESET}")
            return 1


async def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print(f"{RED}Usage: python test-production.py <API_URL> <FRONTEND_URL>{RESET}")
        print("\nExample:")
        print("  python test-production.py \\")
        print("    https://your-username-todo-backend.hf.space \\")
        print("    https://your-app.vercel.app")
        sys.exit(1)

    api_url = sys.argv[1]
    frontend_url = sys.argv[2]

    tester = ProductionTester(api_url, frontend_url)
    await tester.run_all_tests()

    sys.exit(tester.failed)


if __name__ == "__main__":
    asyncio.run(main())
