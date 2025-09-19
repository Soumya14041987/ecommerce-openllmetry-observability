#!/usr/bin/env python3

import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor
import argparse

def test_endpoint(base_url, endpoint, method="GET", data=None):
    """Test a specific endpoint"""
    url = f"{base_url}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"✅ {method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ {method} {endpoint}: {str(e)}")
        return None

def load_test_endpoint(base_url, endpoint, method="GET", data=None, requests_count=10):
    """Perform load testing on an endpoint"""
    print(f"🔄 Load testing {endpoint} with {requests_count} requests...")
    
    def make_request():
        return test_endpoint(base_url, endpoint, method, data)
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda _: make_request(), range(requests_count)))
    
    end_time = time.time()
    successful_requests = sum(1 for r in results if r is not None)
    
    print(f"📊 Load test results for {endpoint}:")
    print(f"   Total requests: {requests_count}")
    print(f"   Successful: {successful_requests}")
    print(f"   Failed: {requests_count - successful_requests}")
    print(f"   Duration: {end_time - start_time:.2f}s")
    print(f"   RPS: {requests_count / (end_time - start_time):.2f}")
    print()

def main():
    parser = argparse.ArgumentParser(description='Test E-commerce OpenLLMetry Application')
    parser.add_argument('--base-url', default='http://localhost:8000', 
                       help='Base URL of the application (default: http://localhost:8000)')
    parser.add_argument('--load-test', action='store_true', 
                       help='Perform load testing')
    parser.add_argument('--requests', type=int, default=20, 
                       help='Number of requests for load testing (default: 20)')
    
    args = parser.parse_args()
    base_url = args.base_url.rstrip('/')
    
    print(f"🚀 Testing E-commerce OpenLLMetry Application at {base_url}")
    print("=" * 60)
    
    # Basic health checks
    print("1. Health Checks")
    print("-" * 20)
    test_endpoint(base_url, "/")
    test_endpoint(base_url, "/health")
    test_endpoint(base_url, "/products")
    test_endpoint(base_url, "/metrics")
    print()
    
    # Test AI endpoints
    print("2. AI Endpoint Tests")
    print("-" * 20)
    
    # Test recommendations
    recommendation_data = {
        "query": "I need a laptop for programming",
        "budget": 1500.0
    }
    test_endpoint(base_url, "/recommendations", "POST", recommendation_data)
    
    # Test chatbot
    chatbot_data = {
        "message": "What are your return policies?"
    }
    test_endpoint(base_url, "/chatbot", "POST", chatbot_data)
    
    # Test search
    search_data = {
        "query": "electronics"
    }
    test_endpoint(base_url, "/search", "POST", search_data)
    print()
    
    # Load testing if requested
    if args.load_test:
        print("3. Load Testing")
        print("-" * 20)
        
        # Load test basic endpoints
        load_test_endpoint(base_url, "/", "GET", None, args.requests // 4)
        load_test_endpoint(base_url, "/products", "GET", None, args.requests // 4)
        
        # Load test AI endpoints with random data
        queries = [
            "I need a smartphone under $700",
            "Looking for headphones for gaming",
            "Best laptop for students",
            "Coffee mug for office use",
            "Programming books recommendation"
        ]
        
        for _ in range(args.requests // 4):
            query = random.choice(queries)
            data = {"query": query, "budget": random.uniform(50, 2000)}
            test_endpoint(base_url, "/recommendations", "POST", data)
            time.sleep(0.1)  # Small delay to avoid overwhelming
        
        print("Load testing completed!")
    
    print("✅ Testing completed!")
    print()
    print("📊 Check your observability dashboards:")
    print(f"   Prometheus: {base_url.replace(':8000', ':9090')}")
    print(f"   Grafana: {base_url.replace(':8000', ':3000')} (admin/admin)")

if __name__ == "__main__":
    main()