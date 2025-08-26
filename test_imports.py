
#!/usr/bin/env python3
"""
Test script to verify all imports are working correctly
"""

print("Testing imports...")

try:
    from data_persistence import DataPersistenceManager
    print("✓ DataPersistenceManager imported successfully")
except Exception as e:
    print(f"✗ DataPersistenceManager import failed: {e}")

try:
    from admin.data_manager import DataManager
    print("✓ DataManager imported successfully")
except Exception as e:
    print(f"✗ DataManager import failed: {e}")

try:
    from admin.sidebar_component import SidebarComponent
    print("✓ SidebarComponent imported successfully")
except Exception as e:
    print(f"✗ SidebarComponent import failed: {e}")

try:
    from admin.header_component import HeaderComponent
    print("✓ HeaderComponent imported successfully")
except Exception as e:
    print(f"✗ HeaderComponent import failed: {e}")

try:
    from database import verify_user, init_db
    print("✓ Database functions imported successfully")
except Exception as e:
    print(f"✗ Database functions import failed: {e}")

try:
    from models import User, Report
    print("✓ Models imported successfully")
except Exception as e:
    print(f"✗ Models import failed: {e}")

print("\nImport test completed!")
