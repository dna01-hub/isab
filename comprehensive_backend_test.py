#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite - Edge Cases and System Robustness
Tests specific scenarios mentioned in the review request
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BASE_URL = "https://720b1add-dfe1-4b0e-8a5b-007a9fc21860.preview.emergentagent.com/api"

class ComprehensiveTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.test_results = []
        
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
    
    def test_whatsapp_format_validation(self):
        """Test various WhatsApp format validations"""
        print("\n=== Testing WhatsApp Format Validation ===")
        
        valid_formats = [
            "(11) 99999-8888",
            "(11) 9999-8888", 
            "11999998888",
            "+5511999998888"
        ]
        
        invalid_formats = [
            "invalid-phone",
            "123",
            "(11) 999-888",  # Too short
            "abc123def456",
            ""
        ]
        
        # Test valid formats
        for i, whatsapp in enumerate(valid_formats):
            user_data = {
                "name": f"Test User {i}",
                "whatsapp": whatsapp,
                "companions": [],
                "stay_connected": False
            }
            
            try:
                response = requests.post(f"{self.base_url}/register", json=user_data)
                if response.status_code == 200:
                    self.log_test(f"WhatsApp Format - Valid {whatsapp}", True, 
                                "Accepted valid WhatsApp format")
                else:
                    self.log_test(f"WhatsApp Format - Valid {whatsapp}", False, 
                                f"Should accept valid format, got status {response.status_code}")
            except Exception as e:
                self.log_test(f"WhatsApp Format - Valid {whatsapp}", False, 
                            f"Request failed: {str(e)}")
        
        # Test invalid formats
        for i, whatsapp in enumerate(invalid_formats):
            user_data = {
                "name": f"Invalid User {i}",
                "whatsapp": whatsapp,
                "companions": [],
                "stay_connected": False
            }
            
            try:
                response = requests.post(f"{self.base_url}/register", json=user_data)
                if response.status_code == 400:
                    self.log_test(f"WhatsApp Format - Invalid {whatsapp}", True, 
                                "Correctly rejected invalid WhatsApp format")
                else:
                    self.log_test(f"WhatsApp Format - Invalid {whatsapp}", False, 
                                f"Should reject invalid format, got status {response.status_code}")
            except Exception as e:
                self.log_test(f"WhatsApp Format - Invalid {whatsapp}", False, 
                            f"Request failed: {str(e)}")
    
    def test_unique_gift_availability(self):
        """Test that unique gifts become unavailable after reservation"""
        print("\n=== Testing Unique Gift Availability ===")
        
        # First, get a unique gift (berço or carrinho)
        try:
            response = requests.get(f"{self.base_url}/gifts/quarto")
            if response.status_code == 200:
                gifts = response.json()
                unique_gift = None
                for gift in gifts:
                    if gift.get("is_unique") and gift.get("is_available"):
                        unique_gift = gift
                        break
                
                if unique_gift:
                    # Register a user to make reservation
                    import time
                    timestamp = str(int(time.time()))
                    user_data = {
                        "name": f"Unique Test User {timestamp}",
                        "whatsapp": f"(11) 8888{timestamp[-4:]}",
                        "companions": [],
                        "stay_connected": False
                    }
                    
                    user_response = requests.post(f"{self.base_url}/register", json=user_data)
                    if user_response.status_code == 200:
                        user = user_response.json()
                        user_id = user.get("id")
                        
                        # Reserve the unique gift
                        reservation_data = {
                            "user_id": user_id,
                            "gift_id": unique_gift["id"],
                            "quantity": 1
                        }
                        
                        reserve_response = requests.post(f"{self.base_url}/reserve-gift", json=reservation_data)
                        if reserve_response.status_code == 200:
                            # Check if gift is now unavailable
                            check_response = requests.get(f"{self.base_url}/gifts/quarto")
                            if check_response.status_code == 200:
                                updated_gifts = check_response.json()
                                updated_gift = None
                                for gift in updated_gifts:
                                    if gift["id"] == unique_gift["id"]:
                                        updated_gift = gift
                                        break
                                
                                if updated_gift and not updated_gift.get("is_available"):
                                    self.log_test("Unique Gift Availability", True, 
                                                f"Unique gift '{unique_gift['name']}' correctly became unavailable after reservation")
                                else:
                                    self.log_test("Unique Gift Availability", False, 
                                                "Unique gift should be unavailable after reservation")
                            else:
                                self.log_test("Unique Gift Availability", False, 
                                            "Failed to check gift availability after reservation")
                        else:
                            self.log_test("Unique Gift Availability", False, 
                                        "Failed to reserve unique gift")
                    else:
                        self.log_test("Unique Gift Availability", False, 
                                    "Failed to register user for unique gift test")
                else:
                    self.log_test("Unique Gift Availability", False, 
                                "No available unique gifts found for testing")
            else:
                self.log_test("Unique Gift Availability", False, 
                            "Failed to fetch gifts for unique test")
        except Exception as e:
            self.log_test("Unique Gift Availability", False, 
                        f"Request failed: {str(e)}")
    
    def test_quantity_validation(self):
        """Test quantity validation for gift reservations"""
        print("\n=== Testing Quantity Validation ===")
        
        # Get a gift with limited quantity
        try:
            response = requests.get(f"{self.base_url}/gifts/fraldas")
            if response.status_code == 200:
                gifts = response.json()
                if gifts:
                    test_gift = gifts[0]
                    available_qty = test_gift.get("available_quantity", 0)
                    
                    if available_qty > 0:
                        # Register a user
                        import time
                        timestamp = str(int(time.time()))
                        user_data = {
                            "name": f"Quantity Test User {timestamp}",
                            "whatsapp": f"(11) 7777{timestamp[-4:]}",
                            "companions": [],
                            "stay_connected": False
                        }
                        
                        user_response = requests.post(f"{self.base_url}/register", json=user_data)
                        if user_response.status_code == 200:
                            user = user_response.json()
                            user_id = user.get("id")
                            
                            # Try to reserve more than available
                            excessive_quantity = available_qty + 10
                            reservation_data = {
                                "user_id": user_id,
                                "gift_id": test_gift["id"],
                                "quantity": excessive_quantity
                            }
                            
                            reserve_response = requests.post(f"{self.base_url}/reserve-gift", json=reservation_data)
                            if reserve_response.status_code == 400:
                                self.log_test("Quantity Validation - Excessive", True, 
                                            f"Correctly rejected reservation of {excessive_quantity} when only {available_qty} available")
                            else:
                                self.log_test("Quantity Validation - Excessive", False, 
                                            f"Should reject excessive quantity, got status {reserve_response.status_code}")
                        else:
                            self.log_test("Quantity Validation - Excessive", False, 
                                        "Failed to register user for quantity test")
                    else:
                        self.log_test("Quantity Validation - Excessive", False, 
                                    "No available gifts found for quantity test")
                else:
                    self.log_test("Quantity Validation - Excessive", False, 
                                "No gifts found in fraldas category")
            else:
                self.log_test("Quantity Validation - Excessive", False, 
                            "Failed to fetch gifts for quantity test")
        except Exception as e:
            self.log_test("Quantity Validation - Excessive", False, 
                        f"Request failed: {str(e)}")
    
    def test_admin_credentials(self):
        """Test admin credentials specifically mentioned in requirements"""
        print("\n=== Testing Admin Credentials ===")
        
        # Test exact credentials from requirements
        correct_credentials = {
            "username": "admin",
            "password": "isabelle_isadora_2025"
        }
        
        try:
            response = requests.post(f"{self.base_url}/admin/login", json=correct_credentials)
            if response.status_code == 200:
                self.log_test("Admin Credentials - Exact Match", True, 
                            "Admin login successful with exact credentials from requirements")
            else:
                self.log_test("Admin Credentials - Exact Match", False, 
                            f"Admin login failed with exact credentials, status {response.status_code}")
        except Exception as e:
            self.log_test("Admin Credentials - Exact Match", False, 
                        f"Request failed: {str(e)}")
        
        # Test case sensitivity
        case_sensitive_tests = [
            {"username": "Admin", "password": "isabelle_isadora_2025"},
            {"username": "admin", "password": "Isabelle_Isadora_2025"},
            {"username": "ADMIN", "password": "ISABELLE_ISADORA_2025"}
        ]
        
        for i, creds in enumerate(case_sensitive_tests):
            try:
                response = requests.post(f"{self.base_url}/admin/login", json=creds)
                if response.status_code == 401:
                    self.log_test(f"Admin Credentials - Case Sensitive {i+1}", True, 
                                "Correctly rejected case-sensitive variations")
                else:
                    self.log_test(f"Admin Credentials - Case Sensitive {i+1}", False, 
                                f"Should reject case variations, got status {response.status_code}")
            except Exception as e:
                self.log_test(f"Admin Credentials - Case Sensitive {i+1}", False, 
                            f"Request failed: {str(e)}")
    
    def test_dashboard_statistics(self):
        """Test dashboard statistics accuracy"""
        print("\n=== Testing Dashboard Statistics ===")
        
        try:
            response = requests.get(f"{self.base_url}/admin/dashboard")
            if response.status_code == 200:
                dashboard = response.json()
                
                # Verify statistics make sense
                total_confirmed = dashboard.get("total_confirmed", 0)
                total_companions = dashboard.get("total_companions", 0)
                total_attendees = dashboard.get("total_attendees", 0)
                
                if total_attendees == total_confirmed + total_companions:
                    self.log_test("Dashboard Statistics - Attendee Calculation", True, 
                                f"Attendee calculation correct: {total_confirmed} + {total_companions} = {total_attendees}")
                else:
                    self.log_test("Dashboard Statistics - Attendee Calculation", False, 
                                f"Attendee calculation incorrect: {total_confirmed} + {total_companions} ≠ {total_attendees}")
                
                # Check if we have users and reservations data
                users = dashboard.get("users", [])
                reservations = dashboard.get("reservations", [])
                
                if len(users) == total_confirmed:
                    self.log_test("Dashboard Statistics - User Count", True, 
                                f"User count matches confirmed attendees: {len(users)}")
                else:
                    self.log_test("Dashboard Statistics - User Count", False, 
                                f"User count mismatch: {len(users)} users vs {total_confirmed} confirmed")
                
                # Check available gifts structure
                available_gifts = dashboard.get("available_gifts", [])
                if isinstance(available_gifts, list):
                    self.log_test("Dashboard Statistics - Available Gifts", True, 
                                f"Available gifts list contains {len(available_gifts)} items")
                else:
                    self.log_test("Dashboard Statistics - Available Gifts", False, 
                                "Available gifts should be a list")
                
            else:
                self.log_test("Dashboard Statistics", False, 
                            f"Dashboard request failed with status {response.status_code}")
        except Exception as e:
            self.log_test("Dashboard Statistics", False, 
                        f"Request failed: {str(e)}")
    
    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("🎀 Starting Comprehensive Backend Tests for Isadora and Isabelle 🎀")
        print(f"Testing backend at: {self.base_url}")
        print("=" * 70)
        
        self.test_whatsapp_format_validation()
        self.test_unique_gift_availability()
        self.test_quantity_validation()
        self.test_admin_credentials()
        self.test_dashboard_statistics()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("🎀 COMPREHENSIVE BACKEND TEST SUMMARY 🎀")
        print("=" * 70)
        
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
        
        print("\n" + "=" * 70)
        return failed == 0

if __name__ == "__main__":
    tester = ComprehensiveTester()
    success = tester.run_comprehensive_tests()
    sys.exit(0 if success else 1)