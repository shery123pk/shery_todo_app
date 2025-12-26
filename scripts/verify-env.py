#!/usr/bin/env python3
"""
Environment Variables Verification Script
Author: Sharmeen Asif

Verifies all required environment variables are set correctly for production deployment.
"""

import os
import sys
import re
from typing import Dict, List, Tuple
from urllib.parse import urlparse

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class EnvironmentValidator:
    """Validates environment configuration for production deployment"""

    def __init__(self, env_type: str = "backend"):
        self.env_type = env_type
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []

    def check_required_vars(self) -> bool:
        """Check all required environment variables"""
        if self.env_type == "backend":
            return self._check_backend_env()
        elif self.env_type == "frontend":
            return self._check_frontend_env()
        else:
            self.errors.append(f"Unknown environment type: {self.env_type}")
            return False

    def _check_backend_env(self) -> bool:
        """Check backend environment variables"""
        print(f"{BLUE}Checking Backend Environment Variables{RESET}\n")

        # DATABASE_URL
        self._check_database_url()

        # BETTER_AUTH_SECRET
        self._check_auth_secret()

        # BETTER_AUTH_URL
        self._check_auth_url()

        # FRONTEND_URL
        self._check_frontend_url()

        return len(self.errors) == 0

    def _check_frontend_env(self) -> bool:
        """Check frontend environment variables"""
        print(f"{BLUE}Checking Frontend Environment Variables{RESET}\n")

        # NEXT_PUBLIC_API_URL
        self._check_api_url()

        # BETTER_AUTH_SECRET (must match backend)
        self._check_auth_secret()

        # BETTER_AUTH_URL (must match backend)
        self._check_auth_url()

        return len(self.errors) == 0

    def _check_database_url(self):
        """Validate DATABASE_URL"""
        var_name = "DATABASE_URL"
        url = os.getenv(var_name)

        if not url:
            self.errors.append(f"{var_name} is not set")
            return

        # Parse URL
        try:
            parsed = urlparse(url)

            # Check protocol
            if parsed.scheme != "postgresql":
                self.errors.append(
                    f"{var_name} must use 'postgresql://' scheme, got '{parsed.scheme}://'"
                )
            else:
                self.passed.append(f"{var_name} uses correct protocol")

            # Check host
            if not parsed.hostname:
                self.errors.append(f"{var_name} missing hostname")
            elif "neon.tech" in parsed.hostname:
                self.passed.append(f"{var_name} uses Neon PostgreSQL")
            else:
                self.warnings.append(
                    f"{var_name} does not appear to be Neon (expected '*.neon.tech')"
                )

            # Check credentials
            if not parsed.username:
                self.errors.append(f"{var_name} missing username")
            if not parsed.password:
                self.errors.append(f"{var_name} missing password")
            if parsed.username and parsed.password:
                self.passed.append(f"{var_name} has credentials")

            # Check database name
            if not parsed.path or parsed.path == "/":
                self.errors.append(f"{var_name} missing database name")
            else:
                db_name = parsed.path.lstrip("/")
                self.passed.append(f"{var_name} specifies database: {db_name}")

            # Check SSL mode
            if "sslmode=require" not in url:
                self.errors.append(
                    f"{var_name} must include '?sslmode=require' for Neon"
                )
            else:
                self.passed.append(f"{var_name} has SSL mode enabled")

        except Exception as e:
            self.errors.append(f"{var_name} is not a valid URL: {e}")

    def _check_auth_secret(self):
        """Validate BETTER_AUTH_SECRET"""
        var_name = "BETTER_AUTH_SECRET"
        secret = os.getenv(var_name)

        if not secret:
            self.errors.append(f"{var_name} is not set")
            return

        # Check length (should be at least 32 characters)
        if len(secret) < 32:
            self.errors.append(
                f"{var_name} is too short ({len(secret)} chars). Should be at least 32 characters for security."
            )
        else:
            self.passed.append(f"{var_name} has sufficient length ({len(secret)} chars)")

        # Check entropy (should contain mix of characters)
        has_upper = any(c.isupper() for c in secret)
        has_lower = any(c.islower() for c in secret)
        has_digit = any(c.isdigit() for c in secret)
        has_special = any(not c.isalnum() for c in secret)

        entropy_score = sum([has_upper, has_lower, has_digit, has_special])

        if entropy_score < 3:
            self.warnings.append(
                f"{var_name} may have low entropy. Consider using a cryptographically secure random generator."
            )
        else:
            self.passed.append(f"{var_name} has good character diversity")

        # Check for common weak secrets
        weak_secrets = [
            "secret",
            "password",
            "12345",
            "test",
            "development",
            "production",
        ]
        if any(weak in secret.lower() for weak in weak_secrets):
            self.errors.append(f"{var_name} contains common weak patterns")

    def _check_auth_url(self):
        """Validate BETTER_AUTH_URL"""
        var_name = "BETTER_AUTH_URL"
        url = os.getenv(var_name)

        if not url:
            self.errors.append(f"{var_name} is not set")
            return

        # Check protocol
        if not url.startswith("https://"):
            self.warnings.append(
                f"{var_name} should use HTTPS in production (got: {url[:20]}...)"
            )
        else:
            self.passed.append(f"{var_name} uses HTTPS")

        # Check for HuggingFace Spaces domain
        if ".hf.space" in url:
            self.passed.append(f"{var_name} uses HuggingFace Spaces")
        elif "localhost" in url or "127.0.0.1" in url:
            self.warnings.append(f"{var_name} appears to be localhost (not production)")
        else:
            self.warnings.append(
                f"{var_name} uses custom domain (ensure it's correct)"
            )

        # Check for trailing slash
        if url.endswith("/"):
            self.errors.append(f"{var_name} should not have trailing slash")

    def _check_frontend_url(self):
        """Validate FRONTEND_URL"""
        var_name = "FRONTEND_URL"
        url = os.getenv(var_name)

        if not url:
            self.errors.append(f"{var_name} is not set")
            return

        # Check protocol
        if not url.startswith("https://"):
            self.warnings.append(
                f"{var_name} should use HTTPS in production (got: {url[:20]}...)"
            )
        else:
            self.passed.append(f"{var_name} uses HTTPS")

        # Check for Vercel domain
        if ".vercel.app" in url:
            self.passed.append(f"{var_name} uses Vercel")
        elif "localhost" in url or "127.0.0.1" in url:
            self.warnings.append(f"{var_name} appears to be localhost (not production)")
        else:
            self.passed.append(f"{var_name} uses custom domain")

        # Check for trailing slash
        if url.endswith("/"):
            self.errors.append(f"{var_name} should not have trailing slash")

    def _check_api_url(self):
        """Validate NEXT_PUBLIC_API_URL"""
        var_name = "NEXT_PUBLIC_API_URL"
        url = os.getenv(var_name)

        if not url:
            self.errors.append(f"{var_name} is not set")
            return

        # Check protocol
        if not url.startswith("https://"):
            self.warnings.append(
                f"{var_name} should use HTTPS in production (got: {url[:20]}...)"
            )
        else:
            self.passed.append(f"{var_name} uses HTTPS")

        # Check for HuggingFace Spaces domain
        if ".hf.space" in url:
            self.passed.append(f"{var_name} points to HuggingFace Spaces backend")
        elif "localhost" in url or "127.0.0.1" in url:
            self.warnings.append(f"{var_name} appears to be localhost (not production)")

        # Check for trailing slash
        if url.endswith("/"):
            self.errors.append(f"{var_name} should not have trailing slash")

    def print_report(self):
        """Print validation report"""
        print(f"\n{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}Environment Validation Report - {self.env_type.upper()}{RESET}")
        print(f"{BLUE}{'='*70}{RESET}\n")

        # Passed checks
        if self.passed:
            print(f"{GREEN}✓ PASSED ({len(self.passed)}){RESET}")
            for item in self.passed:
                print(f"  {GREEN}✓{RESET} {item}")
            print()

        # Warnings
        if self.warnings:
            print(f"{YELLOW}⚠ WARNINGS ({len(self.warnings)}){RESET}")
            for item in self.warnings:
                print(f"  {YELLOW}⚠{RESET} {item}")
            print()

        # Errors
        if self.errors:
            print(f"{RED}✗ ERRORS ({len(self.errors)}){RESET}")
            for item in self.errors:
                print(f"  {RED}✗{RESET} {item}")
            print()

        # Summary
        total = len(self.passed) + len(self.warnings) + len(self.errors)
        print(f"{BLUE}{'='*70}{RESET}")

        if not self.errors:
            print(f"{GREEN}✓ All critical checks passed! Environment is ready for deployment.{RESET}")
            return 0
        else:
            print(
                f"{RED}✗ {len(self.errors)} critical error(s) found. Fix these before deploying.{RESET}"
            )
            return 1


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(f"{RED}Usage: python verify-env.py [backend|frontend]{RESET}")
        print(
            "\nExample:\n  python verify-env.py backend   # Check backend environment"
        )
        print("  python verify-env.py frontend  # Check frontend environment")
        sys.exit(1)

    env_type = sys.argv[1].lower()

    if env_type not in ["backend", "frontend"]:
        print(f"{RED}Error: env_type must be 'backend' or 'frontend'{RESET}")
        sys.exit(1)

    validator = EnvironmentValidator(env_type)
    validator.check_required_vars()
    exit_code = validator.print_report()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
