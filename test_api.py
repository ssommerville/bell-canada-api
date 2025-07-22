#!/usr/bin/env python3
"""
Test script for Bell Canada B2B API
Tests basic functionality and endpoints
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working - API version: {data.get('version')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_businesses():
    """Test businesses endpoints"""
    print("Testing businesses endpoints...")
    
    # Test list businesses
    try:
        response = requests.get(f"{BASE_URL}/api/v1/businesses?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Businesses list working - Found {data.get('total', 0)} businesses")
            
            # Test getting first business
            if data.get('businesses'):
                first_business = data['businesses'][0]
                business_id = first_business['id']
                
                # Test get specific business
                response = requests.get(f"{BASE_URL}/api/v1/businesses/{business_id}")
                if response.status_code == 200:
                    print(f"✅ Get business by ID working - {business_id}")
                else:
                    print(f"❌ Get business by ID failed: {response.status_code}")
                    return False
            return True
        else:
            print(f"❌ Businesses list failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Businesses endpoint error: {e}")
        return False

def test_services():
    """Test services endpoints"""
    print("Testing services endpoints...")
    
    try:
        # Get first business to test services
        response = requests.get(f"{BASE_URL}/api/v1/businesses?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data.get('businesses'):
                business_id = data['businesses'][0]['id']
                
                # Test get business services
                response = requests.get(f"{BASE_URL}/api/v1/businesses/{business_id}/services")
                if response.status_code == 200:
                    services = response.json()
                    print(f"✅ Business services working - {len(services)} services found")
                    return True
                else:
                    print(f"❌ Business services failed: {response.status_code}")
                    return False
        else:
            print(f"❌ Cannot get business for services test: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Services endpoint error: {e}")
        return False

def test_analytics():
    """Test analytics endpoints"""
    print("Testing analytics endpoints...")
    
    try:
        # Test revenue analytics
        response = requests.get(f"{BASE_URL}/api/v1/analytics/revenue")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Revenue analytics working - Total revenue: ${data.get('total_monthly_revenue', 0):,.2f}")
        else:
            print(f"❌ Revenue analytics failed: {response.status_code}")
            return False
        
        # Test customer analytics
        response = requests.get(f"{BASE_URL}/api/v1/analytics/customers")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Customer analytics working - Total customers: {data.get('total_customers', 0)}")
        else:
            print(f"❌ Customer analytics failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Analytics endpoint error: {e}")
        return False

def test_utilities():
    """Test utility endpoints"""
    print("Testing utility endpoints...")
    
    try:
        # Test industries
        response = requests.get(f"{BASE_URL}/api/v1/industries")
        if response.status_code == 200:
            industries = response.json()
            print(f"✅ Industries endpoint working - {len(industries)} industries")
        else:
            print(f"❌ Industries endpoint failed: {response.status_code}")
            return False
        
        # Test provinces
        response = requests.get(f"{BASE_URL}/api/v1/provinces")
        if response.status_code == 200:
            provinces = response.json()
            print(f"✅ Provinces endpoint working - {len(provinces)} provinces")
        else:
            print(f"❌ Provinces endpoint failed: {response.status_code}")
            return False
        
        # Test service types
        response = requests.get(f"{BASE_URL}/api/v1/service-types")
        if response.status_code == 200:
            service_types = response.json()
            print(f"✅ Service types endpoint working - {len(service_types)} service types")
        else:
            print(f"❌ Service types endpoint failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Utility endpoints error: {e}")
        return False

def test_filtering():
    """Test filtering and search functionality"""
    print("Testing filtering and search...")
    
    try:
        # Test search
        response = requests.get(f"{BASE_URL}/api/v1/businesses?search=Technology&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search working - Found {len(data.get('businesses', []))} businesses with 'Technology'")
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
        
        # Test industry filter
        response = requests.get(f"{BASE_URL}/api/v1/businesses?industry=Technology&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Industry filter working - Found {len(data.get('businesses', []))} Technology businesses")
        else:
            print(f"❌ Industry filter failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Filtering error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Bell Canada B2B API Tests")
    print("=" * 50)
    
    tests = [
        test_health,
        test_root,
        test_businesses,
        test_services,
        test_analytics,
        test_utilities,
        test_filtering
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
        print("\n📖 Next steps:")
        print("1. Visit http://localhost:8000/docs for interactive API documentation")
        print("2. Try the example API calls in the README")
        print("3. Start integrating with Salesforce!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 