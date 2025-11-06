"""
Test script to verify the environment setup
Run this before deploying to ensure all dependencies are installed correctly
"""

import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    tests = {
        "streamlit": "Streamlit web framework",
        "pandas": "Pandas data manipulation",
        "geopandas": "GeoPandas geospatial data",
        "ecoscope.io.earthranger": "Ecoscope EarthRanger integration",
        "shapely": "Shapely geometric operations",
        "pytz": "Timezone support",
    }
    
    failed = []
    
    for module, description in tests.items():
        try:
            __import__(module)
            print(f"✅ {description}: OK")
        except ImportError as e:
            print(f"❌ {description}: FAILED - {e}")
            failed.append(module)
    
    print("\n" + "="*50)
    
    if failed:
        print(f"❌ {len(failed)} test(s) failed:")
        for module in failed:
            print(f"   - {module}")
        print("\nRun: pip install -r requirements.txt")
        return False
    else:
        print("✅ All imports successful!")
        print("\nYou can now run the app with:")
        print("   streamlit run app.py")
        return True

def check_python_version():
    """Check Python version"""
    print(f"Python version: {sys.version}")
    major, minor = sys.version_info[:2]
    
    if major >= 3 and minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def main():
    print("="*50)
    print("Environment Setup Test")
    print("="*50 + "\n")
    
    version_ok = check_python_version()
    print("\n" + "="*50 + "\n")
    
    if not version_ok:
        print("⚠️  Please upgrade Python to 3.8 or higher")
        return
    
    imports_ok = test_imports()
    
    print("\n" + "="*50)
    if imports_ok:
        print("\n🎉 Setup complete! Your environment is ready.")
    else:
        print("\n⚠️  Please fix the errors above before running the app.")

if __name__ == "__main__":
    main()
