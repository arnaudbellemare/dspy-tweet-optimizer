#!/usr/bin/env python3
"""
Deployment test script for Streamlit Cloud.

This script tests that all components are ready for deployment.
"""

import os
import sys
import importlib
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    required_modules = [
        'streamlit',
        'dspy', 
        'pydantic',
        'requests'
    ]
    
    optional_modules = [
        'openai',
        'pandas'
    ]
    
    all_good = True
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            all_good = False
    
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module} (optional)")
        except ImportError:
            print(f"  ⚠️  {module} (optional, not installed)")
    
    return all_good

def test_files():
    """Test that all required files exist."""
    print("\n🧪 Testing required files...")
    
    required_files = [
        'enhanced_app.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'README.md'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_good = False
    
    return all_good

def test_app_import():
    """Test that the main app can be imported."""
    print("\n🧪 Testing app import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Try to import the main app
        import enhanced_app
        print("  ✅ enhanced_app.py imports successfully")
        
        # Check if main function exists
        if hasattr(enhanced_app, 'main'):
            print("  ✅ main() function found")
        else:
            print("  ❌ main() function not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_environment():
    """Test environment setup."""
    print("\n🧪 Testing environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 9:
        print(f"  ✅ Python {python_version.major}.{python_version.minor} (compatible)")
    else:
        print(f"  ❌ Python {python_version.major}.{python_version.minor} (requires 3.9+)")
        return False
    
    # Check environment variables
    env_vars = ['PERPLEXITY_API_KEY', 'OPENROUTER_API_KEY']
    for var in env_vars:
        if os.getenv(var):
            print(f"  ✅ {var} is set")
        else:
            print(f"  ⚠️  {var} not set (optional)")
    
    return True

def main():
    """Run all deployment tests."""
    print("🚀 Streamlit Cloud Deployment Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Files", test_files),
        ("Imports", test_imports),
        ("App Import", test_app_import)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Deployment Test Results:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Ready for Streamlit Cloud deployment!")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Go to https://share.streamlit.io/")
        print("3. Deploy with main file: enhanced_app.py")
        print("4. Set environment variables if needed")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Fix issues before deployment.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
