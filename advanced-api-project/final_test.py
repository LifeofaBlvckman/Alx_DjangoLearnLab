#!/usr/bin/env python
"""
Final test script for ALX Generic Views task.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8003/api"

def print_test(name, success, details=""):
    """Print test result."""
    symbol = "✅" if success else "❌"
    print(f"{symbol} {name}")
    if details:
        print(f"   {details}")

def test_api():
    """Run all tests."""
    print("=" * 60)
    print("ALX Generic Views - Final Verification")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    try:
        # Test 1: API Root
        total_tests += 1
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            tests_passed += 1
            print_test("API Root accessible", True, f"Status: {response.status_code}")
        else:
            print_test("API Root accessible", False, f"Status: {response.status_code}")
        
        # Test 2: Book List (Public)
        total_tests += 1
        response = requests.get(f"{BASE_URL}/books/")
        if response.status_code == 200:
            tests_passed += 1
            data = response.json()
            count = data.get('count', 0)
            print_test("Book List accessible", True, f"Status: {response.status_code}, Books: {count}")
        else:
            print_test("Book List accessible", False, f"Status: {response.status_code}")
        
        # Test 3: Book Create without auth (should fail)
        total_tests += 1
        response = requests.post(
            f"{BASE_URL}/books/create/",
            json={"title": "Test Book", "publication_year": 2020, "author": 1}
        )
        # Note: 403 is acceptable (Forbidden) - means permissions working
        if response.status_code in [401, 403]:
            tests_passed += 1
            print_test("Book Create requires auth", True, f"Correctly returned {response.status_code}")
        else:
            print_test("Book Create requires auth", False, f"Expected 401/403, got {response.status_code}")
        
        # Test 4: Book Detail (Public)
        total_tests += 1
        response = requests.get(f"{BASE_URL}/books/1/")
        if response.status_code == 200:
            tests_passed += 1
            print_test("Book Detail accessible", True, f"Status: {response.status_code}")
        else:
            print_test("Book Detail accessible", False, f"Status: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("Make sure server is running: python manage.py runserver 8003")
        return False
    
    # Results
    print("\n" + "=" * 60)
    print(f"Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED - PROJECT IS COMPLETE!")
        return True
    else:
        print("\n⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    import sys
    success = test_api()
    sys.exit(0 if success else 1)
