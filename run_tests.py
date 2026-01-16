"""
Runs tests for this webap.

Usage examples:
    (all) uv run ./run_tests.py -v
    (app) uv run ./run_tests.py -v pdf_checker_app
    (file) uv run ./run_tests.py -v tests.test_environment_checks
    (class) uv run ./run_tests.py -v tests.test_environment_checks.TestEnvironmentChecks
    (method) uv run ./run_tests.py -v tests.test_environment_checks.TestEnvironmentChecks.test_check_branch_non_main_raises

Note: there are currently no unit-tests, so this'll show, appropriately, zero tests run.
"""

import sys
import unittest
from pathlib import Path


def main() -> None:
    """
    Main function to discover and run tests.
    """
    # Get the project root directory
    project_root = Path(__file__).parent

    # Create a test suite with all test files
    loader = unittest.TestLoader()
    start_dir = project_root

    # Discover all test files (files starting with 'test_')
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Create a test runner with verbosity
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)

    # Run the tests
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
