#!/usr/bin/env python3
"""
Test script to verify package installation and import
"""

import sys
import os

def test_package_structure():
    """Test if the package structure is correct"""
    print("Testing package structure...")
    
    # Check if financial_models directory exists
    if os.path.exists("financial_models"):
        print("✅ financial_models directory exists")
    else:
        print("❌ financial_models directory missing")
        return False
    
    # Check if rsi subdirectory exists
    if os.path.exists("financial_models/rsi"):
        print("✅ financial_models/rsi directory exists")
    else:
        print("❌ financial_models/rsi directory missing")
        return False
    
    # Check if __init__.py files exist
    if os.path.exists("financial_models/__init__.py"):
        print("✅ financial_models/__init__.py exists")
    else:
        print("❌ financial_models/__init__.py missing")
        return False
    
    if os.path.exists("financial_models/rsi/__init__.py"):
        print("✅ financial_models/rsi/__init__.py exists")
    else:
        print("❌ financial_models/rsi/__init__.py missing")
        return False
    
    if os.path.exists("financial_models/rsi/model.py"):
        print("✅ financial_models/rsi/model.py exists")
    else:
        print("❌ financial_models/rsi/model.py missing")
        return False
    
    return True

def test_import():
    """Test if the package can be imported"""
    print("\nTesting package import...")
    
    try:
        # Add current directory to path
        if '.' not in sys.path:
            sys.path.insert(0, '.')
        
        # Test import
        from financial_models.rsi import RSIModel
        print("✅ Successfully imported RSIModel")
        
        # Test instantiation
        model = RSIModel()
        print("✅ Successfully created RSIModel instance")
        
        # Test basic functionality
        data = model.get_stock_data("AAPL", period="1mo")
        if not data.empty:
            print("✅ Successfully fetched stock data")
        else:
            print("⚠️  Stock data fetch returned empty DataFrame")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        return False

def test_setup_py():
    """Test if setup.py can be executed"""
    print("\nTesting setup.py...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "setup.py", "check"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ setup.py check passed")
            return True
        else:
            print(f"❌ setup.py check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running setup.py: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("PACKAGE INSTALLATION TEST")
    print("=" * 50)
    
    tests = [
        test_package_structure,
        test_import,
        test_setup_py
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Package is ready for installation.")
        print("\nTo install in another project:")
        print("1. pip install -e .")
        print("2. from financial_models.rsi import RSIModel")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    main() 