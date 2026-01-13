#!/usr/bin/env python3
"""
Test runner script for SmartSpace Agentic Brain

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run unit tests only
    python run_tests.py --integration      # Run integration tests only
    python run_tests.py --coverage         # Run with coverage report
    python run_tests.py --fast             # Skip slow tests
    python run_tests.py --module models    # Run specific module tests
"""

import sys
import subprocess
from pathlib import Path


def run_tests(args=None):
    """Run pytest with specified arguments"""
    base_cmd = ["pytest"]
    
    if args is None:
        args = sys.argv[1:]
    
    # Parse custom arguments
    if "--unit" in args:
        base_cmd.extend(["-m", "unit"])
        args.remove("--unit")
    
    if "--integration" in args:
        base_cmd.extend(["-m", "integration"])
        args.remove("--integration")
    
    if "--coverage" in args:
        base_cmd.extend([
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term"
        ])
        args.remove("--coverage")
    
    if "--fast" in args:
        base_cmd.extend(["-m", "not slow"])
        args.remove("--fast")
    
    if "--module" in args:
        idx = args.index("--module")
        module = args[idx + 1]
        base_cmd.append(f"tests/test_{module}.py")
        args.remove("--module")
        args.remove(module)
    
    # Add remaining arguments
    base_cmd.extend(args)
    
    # Run pytest
    print(f"Running: {' '.join(base_cmd)}")
    result = subprocess.run(base_cmd)
    
    return result.returncode


def main():
    """Main entry point"""
    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    
    print("=" * 80)
    print("SmartSpace Agentic Brain - Test Suite")
    print("=" * 80)
    print(f"Project root: {project_root}")
    print()
    
    # Run tests
    exit_code = run_tests()
    
    if exit_code == 0:
        print("\n" + "=" * 80)
        print("✅ All tests passed!")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("❌ Some tests failed.")
        print("=" * 80)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
