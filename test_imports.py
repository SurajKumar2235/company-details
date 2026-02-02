#!/usr/bin/env python
"""Quick import test"""
import sys
import traceback

print("Testing imports...")
print(f"Python path: {sys.path[:3]}")

try:
    print("\n1. Testing settings import...")
    from company_insight_service.config.settings import settings
    print(f"   ✅ Settings loaded: {settings.LOG_LEVEL}")
except Exception as e:
    print(f"   ❌ Settings failed: {e}")
    traceback.print_exc()

try:
    print("\n2. Testing database models import...")
    from company_insight_service.database.models import Company
    print(f"   ✅ Models loaded")
except Exception as e:
    print(f"   ❌ Models failed: {e}")
    traceback.print_exc()

try:
    print("\n3. Testing services import...")
    from company_insight_service.services import search_web
    print(f"   ✅ Services loaded")
except Exception as e:
    print(f"   ❌ Services failed: {e}")
    traceback.print_exc()

try:
    print("\n4. Testing API app import...")
    from company_insight_service.api.app import app
    print(f"   ✅ App loaded")
except Exception as e:
    print(f"   ❌ App failed: {e}")
    traceback.print_exc()

print("\n✅ Import test complete!")
