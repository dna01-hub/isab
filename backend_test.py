#!/usr/bin/env python3
"""
Backend Test Suite for Baby Shower System - Isadora and Isabelle
Tests all API endpoints systematically
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BASE_URL = "https://720b1add-dfe1-4b0e-8a5b-007a9fc21860.preview.emergentagent.com/api"

class BabyShowerTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.test_results = []
        self.test_user_id = None
        self.test_gift_id = None
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_user_registration(self):
        """Test POST /api/register endpoint"""
        print("\n=== Testing User Registration ===")
        
        # Test valid registration
        user_data = {
            "name": "Maria Silva",
            "whatsapp": "(11) 99999-8888",
            "companions": ["João Silva", "Ana Silva"],
            "stay_connected": True
        }
        
        try:
            response = requests.post(f"{self.base_url}/register", json=user_data)
            if response.status_code == 200:
                user = response.json()
                self.test_user_id = user.get("id")
                self.log_test("User Registration - Valid Data", True, 
                            f"User registered successfully with ID: {self.test_user_id}")
            else:
                self.log_test("User Registration - Valid Data", False, 
                            f"Registration failed with status {response.status_code}", 
                            response.text)
        except Exception as e:
            self.log_test("User Registration - Valid Data", False, 
                        f"Request failed: {str(e)}")
        
        # Test duplicate registration
        try:
            response = requests.post(f"{self.base_url}/register", json=user_data)
            if response.status_code == 400:
                self.log_test("User Registration - Duplicate WhatsApp", True, 
                            "Correctly rejected duplicate WhatsApp")
            else:
                self.log_test("User Registration - Duplicate WhatsApp", False, 
                            f"Should have rejected duplicate, got status {response.status_code}")
        except Exception as e:
            self.log_test("User Registration - Duplicate WhatsApp", False, 
                        f"Request failed: {str(e)}")
        
        # Test invalid WhatsApp format
        invalid_user = {
            "name": "Pedro Santos",
            "whatsapp": "invalid-phone",
            "companions": [],
            "stay_connected": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/register", json=invalid_user)
            if response.status_code == 400:
                self.log_test("User Registration - Invalid WhatsApp", True, 
                            "Correctly rejected invalid WhatsApp format")
            else:
                self.log_test("User Registration - Invalid WhatsApp", False, 
                            f"Should have rejected invalid format, got status {response.status_code}")
        except Exception as e:
            self.log_test("User Registration - Invalid WhatsApp", False, 
                        f"Request failed: {str(e)}")
    
    def test_user_login(self):
        """Test POST /api/login endpoint"""
        print("\n=== Testing User Login ===")
        
        # Test valid login
        login_data = {
            "name": "Maria Silva",
            "whatsapp": "(11) 99999-8888"
        }
        
        try:
            response = requests.post(f"{self.base_url}/login", json=login_data)
            if response.status_code == 200:
                user = response.json()
                self.log_test("User Login - Valid Credentials", True, 
                            f"Login successful for user: {user.get('name')}")
            else:
                self.log_test("User Login - Valid Credentials", False, 
                            f"Login failed with status {response.status_code}", 
                            response.text)
        except Exception as e:
            self.log_test("User Login - Valid Credentials", False, 
                        f"Request failed: {str(e)}")
        
        # Test invalid login
        invalid_login = {
            "name": "Usuário Inexistente",
            "whatsapp": "(11) 88888-7777"
        }
        
        try:
            response = requests.post(f"{self.base_url}/login", json=invalid_login)
            if response.status_code == 404:
                self.log_test("User Login - Invalid Credentials", True, 
                            "Correctly rejected invalid credentials")
            else:
                self.log_test("User Login - Invalid Credentials", False, 
                            f"Should have rejected invalid credentials, got status {response.status_code}")
        except Exception as e:
            self.log_test("User Login - Invalid Credentials", False, 
                        f"Request failed: {str(e)}")
    
    def test_gifts_initialization(self):
        """Test if gifts were initialized automatically"""
        print("\n=== Testing Gift Initialization ===")
        
        try:
            response = requests.get(f"{self.base_url}/gifts")
            if response.status_code == 200:
                gifts = response.json()
                if len(gifts) > 0:
                    self.log_test("Gift Initialization", True, 
                                f"Found {len(gifts)} gifts initialized in database")
                    # Store a gift ID for later tests
                    self.test_gift_id = gifts[0].get("id")
                else:
                    self.log_test("Gift Initialization", False, 
                                "No gifts found in database")
            else:
                self.log_test("Gift Initialization", False, 
                            f"Failed to fetch gifts, status {response.status_code}")
        except Exception as e:
            self.log_test("Gift Initialization", False, 
                        f"Request failed: {str(e)}")
    
    def test_gifts_by_category(self):
        """Test GET /api/gifts/{category} endpoint"""
        print("\n=== Testing Gifts by Category ===")
        
        categories = ["fraldas", "roupas", "higiene", "alimentacao", "quarto", "passeio"]
        
        for category in categories:
            try:
                response = requests.get(f"{self.base_url}/gifts/{category}")
                if response.status_code == 200:
                    gifts = response.json()
                    self.log_test(f"Gifts by Category - {category}", True, 
                                f"Found {len(gifts)} gifts in {category} category")
                else:
                    self.log_test(f"Gifts by Category - {category}", False, 
                                f"Failed to fetch {category} gifts, status {response.status_code}")
            except Exception as e:
                self.log_test(f"Gifts by Category - {category}", False, 
                            f"Request failed: {str(e)}")
        
        # Test invalid category
        try:
            response = requests.get(f"{self.base_url}/gifts/categoria_inexistente")
            if response.status_code == 200:
                gifts = response.json()
                if len(gifts) == 0:
                    self.log_test("Gifts by Category - Invalid Category", True, 
                                "Correctly returned empty list for invalid category")
                else:
                    self.log_test("Gifts by Category - Invalid Category", False, 
                                f"Should return empty list, got {len(gifts)} gifts")
            else:
                self.log_test("Gifts by Category - Invalid Category", False, 
                            f"Unexpected status {response.status_code}")
        except Exception as e:
            self.log_test("Gifts by Category - Invalid Category", False, 
                        f"Request failed: {str(e)}")
    
    def test_gift_reservation(self):
        """Test POST /api/reserve-gift endpoint"""
        print("\n=== Testing Gift Reservation ===")
        
        if not self.test_user_id or not self.test_gift_id:
            self.log_test("Gift Reservation - Setup", False, 
                        "Missing user_id or gift_id for reservation test")
            return
        
        # Test valid reservation
        reservation_data = {
            "user_id": self.test_user_id,
            "gift_id": self.test_gift_id,
            "quantity": 1
        }
        
        try:
            response = requests.post(f"{self.base_url}/reserve-gift", json=reservation_data)
            if response.status_code == 200:
                result = response.json()
                self.log_test("Gift Reservation - Valid", True, 
                            "Gift reserved successfully")
            else:
                self.log_test("Gift Reservation - Valid", False, 
                            f"Reservation failed with status {response.status_code}", 
                            response.text)
        except Exception as e:
            self.log_test("Gift Reservation - Valid", False, 
                        f"Request failed: {str(e)}")
        
        # Test reservation with invalid gift ID
        invalid_reservation = {
            "user_id": self.test_user_id,
            "gift_id": "invalid-gift-id",
            "quantity": 1
        }
        
        try:
            response = requests.post(f"{self.base_url}/reserve-gift", json=invalid_reservation)
            if response.status_code == 404:
                self.log_test("Gift Reservation - Invalid Gift", True, 
                            "Correctly rejected invalid gift ID")
            else:
                self.log_test("Gift Reservation - Invalid Gift", False, 
                            f"Should have rejected invalid gift, got status {response.status_code}")
        except Exception as e:
            self.log_test("Gift Reservation - Invalid Gift", False, 
                        f"Request failed: {str(e)}")
    
    def test_user_reservations(self):
        """Test GET /api/user/{user_id}/reservations endpoint"""
        print("\n=== Testing User Reservations ===")
        
        if not self.test_user_id:
            self.log_test("User Reservations - Setup", False, 
                        "Missing user_id for reservations test")
            return
        
        try:
            response = requests.get(f"{self.base_url}/user/{self.test_user_id}/reservations")
            if response.status_code == 200:
                reservations = response.json()
                self.log_test("User Reservations", True, 
                            f"Found {len(reservations)} reservations for user")
            else:
                self.log_test("User Reservations", False, 
                            f"Failed to fetch reservations, status {response.status_code}")
        except Exception as e:
            self.log_test("User Reservations", False, 
                        f"Request failed: {str(e)}")
    
    def test_admin_login(self):
        """Test POST /api/admin/login endpoint"""
        print("\n=== Testing Admin Login ===")
        
        # Test valid admin login
        admin_credentials = {
            "username": "admin",
            "password": "isabelle_isadora_2025"
        }
        
        try:
            response = requests.post(f"{self.base_url}/admin/login", json=admin_credentials)
            if response.status_code == 200:
                self.log_test("Admin Login - Valid Credentials", True, 
                            "Admin login successful")
            else:
                self.log_test("Admin Login - Valid Credentials", False, 
                            f"Admin login failed with status {response.status_code}", 
                            response.text)
        except Exception as e:
            self.log_test("Admin Login - Valid Credentials", False, 
                        f"Request failed: {str(e)}")
        
        # Test invalid admin login
        invalid_credentials = {
            "username": "admin",
            "password": "wrong_password"
        }
        
        try:
            response = requests.post(f"{self.base_url}/admin/login", json=invalid_credentials)
            if response.status_code == 401:
                self.log_test("Admin Login - Invalid Credentials", True, 
                            "Correctly rejected invalid admin credentials")
            else:
                self.log_test("Admin Login - Invalid Credentials", False, 
                            f"Should have rejected invalid credentials, got status {response.status_code}")
        except Exception as e:
            self.log_test("Admin Login - Invalid Credentials", False, 
                        f"Request failed: {str(e)}")
    
    def test_admin_dashboard(self):
        """Test GET /api/admin/dashboard endpoint"""
        print("\n=== Testing Admin Dashboard ===")
        
        try:
            response = requests.get(f"{self.base_url}/admin/dashboard")
            if response.status_code == 200:
                dashboard = response.json()
                required_fields = ["total_confirmed", "total_companions", "total_attendees", 
                                 "total_gifts_reserved", "total_gifts_available", "users", 
                                 "reservations", "available_gifts"]
                
                missing_fields = [field for field in required_fields if field not in dashboard]
                
                if not missing_fields:
                    self.log_test("Admin Dashboard", True, 
                                f"Dashboard returned all required fields. "
                                f"Confirmed: {dashboard['total_confirmed']}, "
                                f"Attendees: {dashboard['total_attendees']}, "
                                f"Gifts Reserved: {dashboard['total_gifts_reserved']}")
                else:
                    self.log_test("Admin Dashboard", False, 
                                f"Missing required fields: {missing_fields}")
            else:
                self.log_test("Admin Dashboard", False, 
                            f"Dashboard request failed with status {response.status_code}")
        except Exception as e:
            self.log_test("Admin Dashboard", False, 
                        f"Request failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests in sequence"""
        print("🎀 Starting Baby Shower Backend Tests for Isadora and Isabelle 🎀")
        print(f"Testing backend at: {self.base_url}")
        print("=" * 60)
        
        # Run tests in logical order
        self.test_gifts_initialization()
        self.test_user_registration()
        self.test_user_login()
        self.test_gifts_by_category()
        self.test_gift_reservation()
        self.test_user_reservations()
        self.test_admin_login()
        self.test_admin_dashboard()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🎀 BABY SHOWER BACKEND TEST SUMMARY 🎀")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if "✅ PASS" in result["status"])
        failed = sum(1 for result in self.test_results if "❌ FAIL" in result["status"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "❌ FAIL" in result["status"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n" + "=" * 60)
        return failed == 0

if __name__ == "__main__":
    tester = BabyShowerTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)