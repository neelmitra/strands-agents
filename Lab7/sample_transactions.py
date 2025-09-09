"""
Sample Transaction Data for Fraud Detection Testing

This module provides sample transaction data representing various scenarios
including legitimate transactions, suspicious activities, and clear fraud cases.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class TransactionData:
    """Container for sample transaction data used in fraud detection testing."""
    
    @staticmethod
    def get_legitimate_transactions() -> List[Dict[str, Any]]:
        """Returns a list of legitimate transaction examples."""
        return [
            {
                "transaction_id": "TXN_001",
                "user_id": "USER_12345",
                "amount": 45.67,
                "currency": "USD",
                "merchant": "Local Grocery Store",
                "merchant_category": "grocery",
                "location": "New York, NY",
                "timestamp": "2024-01-15T14:30:00Z",
                "payment_method": "credit_card",
                "card_last_four": "1234",
                "description": "Weekly grocery shopping"
            },
            {
                "transaction_id": "TXN_002",
                "user_id": "USER_12345",
                "amount": 89.99,
                "currency": "USD",
                "merchant": "Amazon",
                "merchant_category": "online_retail",
                "location": "Seattle, WA",
                "timestamp": "2024-01-16T10:15:00Z",
                "payment_method": "credit_card",
                "card_last_four": "1234",
                "description": "Online purchase - electronics"
            },
            {
                "transaction_id": "TXN_003",
                "user_id": "USER_67890",
                "amount": 12.50,
                "currency": "USD",
                "merchant": "Starbucks",
                "merchant_category": "restaurant",
                "location": "San Francisco, CA",
                "timestamp": "2024-01-16T08:45:00Z",
                "payment_method": "mobile_pay",
                "card_last_four": "5678",
                "description": "Coffee and pastry"
            }
        ]
    
    @staticmethod
    def get_suspicious_transactions() -> List[Dict[str, Any]]:
        """Returns a list of suspicious transaction examples that require investigation."""
        return [
            {
                "transaction_id": "TXN_SUSP_001",
                "user_id": "USER_12345",
                "amount": 2500.00,
                "currency": "USD",
                "merchant": "Electronics Mega Store",
                "merchant_category": "electronics",
                "location": "Miami, FL",
                "timestamp": "2024-01-17T23:45:00Z",
                "payment_method": "credit_card",
                "card_last_four": "1234",
                "description": "Large electronics purchase - unusual time",
                "risk_factors": [
                    "unusual_time",
                    "high_amount",
                    "different_location"
                ]
            },
            {
                "transaction_id": "TXN_SUSP_002",
                "user_id": "USER_67890",
                "amount": 500.00,
                "currency": "USD",
                "merchant": "Gas Station XYZ",
                "merchant_category": "gas_station",
                "location": "Las Vegas, NV",
                "timestamp": "2024-01-17T03:20:00Z",
                "payment_method": "credit_card",
                "card_last_four": "5678",
                "description": "Unusual gas station amount",
                "risk_factors": [
                    "unusual_amount_for_category",
                    "unusual_time",
                    "travel_pattern"
                ]
            },
            {
                "transaction_id": "TXN_SUSP_003",
                "user_id": "USER_11111",
                "amount": 1.00,
                "currency": "USD",
                "merchant": "Online Test Merchant",
                "merchant_category": "online_services",
                "location": "Unknown",
                "timestamp": "2024-01-17T15:30:00Z",
                "payment_method": "credit_card",
                "card_last_four": "9999",
                "description": "Small test transaction",
                "risk_factors": [
                    "card_testing",
                    "unknown_merchant",
                    "small_amount_test"
                ]
            }
        ]
    
    @staticmethod
    def get_fraudulent_transactions() -> List[Dict[str, Any]]:
        """Returns a list of clearly fraudulent transaction examples."""
        return [
            {
                "transaction_id": "TXN_FRAUD_001",
                "user_id": "USER_12345",
                "amount": 5000.00,
                "currency": "USD",
                "merchant": "Luxury Goods International",
                "merchant_category": "luxury_goods",
                "location": "London, UK",
                "timestamp": "2024-01-17T04:00:00Z",
                "payment_method": "credit_card",
                "card_last_four": "1234",
                "description": "High-value international purchase",
                "risk_factors": [
                    "international_transaction",
                    "high_value",
                    "unusual_time",
                    "no_travel_history",
                    "different_spending_pattern"
                ]
            },
            {
                "transaction_id": "TXN_FRAUD_002",
                "user_id": "USER_67890",
                "amount": 999.99,
                "currency": "USD",
                "merchant": "Cash Advance Service",
                "merchant_category": "cash_advance",
                "location": "Detroit, MI",
                "timestamp": "2024-01-17T02:15:00Z",
                "payment_method": "credit_card",
                "card_last_four": "5678",
                "description": "Cash advance - unusual pattern",
                "risk_factors": [
                    "cash_advance",
                    "unusual_time",
                    "high_risk_merchant_category",
                    "location_anomaly"
                ]
            },
            {
                "transaction_id": "TXN_FRAUD_003",
                "user_id": "USER_22222",
                "amount": 3500.00,
                "currency": "USD",
                "merchant": "Cryptocurrency Exchange",
                "merchant_category": "cryptocurrency",
                "location": "Online",
                "timestamp": "2024-01-17T01:30:00Z",
                "payment_method": "credit_card",
                "card_last_four": "7777",
                "description": "Large cryptocurrency purchase",
                "risk_factors": [
                    "cryptocurrency",
                    "high_value",
                    "unusual_time",
                    "new_user_pattern",
                    "high_risk_category"
                ]
            }
        ]
    
    @staticmethod
    def get_user_profiles() -> Dict[str, Dict[str, Any]]:
        """Returns user profile information for context in fraud detection."""
        return {
            "USER_12345": {
                "name": "John Smith",
                "account_age_months": 24,
                "average_monthly_spending": 1200.00,
                "typical_locations": ["New York, NY", "Boston, MA"],
                "typical_merchants": ["grocery", "online_retail", "restaurant"],
                "risk_score": "low",
                "previous_fraud_reports": 0
            },
            "USER_67890": {
                "name": "Jane Doe",
                "account_age_months": 36,
                "average_monthly_spending": 800.00,
                "typical_locations": ["San Francisco, CA", "Oakland, CA"],
                "typical_merchants": ["restaurant", "transportation", "entertainment"],
                "risk_score": "low",
                "previous_fraud_reports": 0
            },
            "USER_11111": {
                "name": "Bob Johnson",
                "account_age_months": 2,
                "average_monthly_spending": 300.00,
                "typical_locations": ["Chicago, IL"],
                "typical_merchants": ["grocery", "gas_station"],
                "risk_score": "medium",
                "previous_fraud_reports": 0
            },
            "USER_22222": {
                "name": "Alice Brown",
                "account_age_months": 1,
                "average_monthly_spending": 150.00,
                "typical_locations": ["Phoenix, AZ"],
                "typical_merchants": ["grocery"],
                "risk_score": "high",
                "previous_fraud_reports": 1
            }
        }
    
    @staticmethod
    def get_transaction_batch() -> List[Dict[str, Any]]:
        """Returns a mixed batch of transactions for comprehensive testing."""
        all_transactions = []
        all_transactions.extend(TransactionData.get_legitimate_transactions())
        all_transactions.extend(TransactionData.get_suspicious_transactions())
        all_transactions.extend(TransactionData.get_fraudulent_transactions())
        return all_transactions
    
    @staticmethod
    def format_transaction_for_analysis(transaction: Dict[str, Any]) -> str:
        """Formats a transaction dictionary into a readable string for agent analysis."""
        return f"""
Transaction Analysis Request:
- Transaction ID: {transaction['transaction_id']}
- User ID: {transaction['user_id']}
- Amount: ${transaction['amount']} {transaction['currency']}
- Merchant: {transaction['merchant']} ({transaction['merchant_category']})
- Location: {transaction['location']}
- Time: {transaction['timestamp']}
- Payment Method: {transaction['payment_method']}
- Card: ****{transaction['card_last_four']}
- Description: {transaction['description']}
"""

    @staticmethod
    def get_fraud_detection_scenarios() -> List[Dict[str, Any]]:
        """Returns specific fraud detection scenarios for testing agent capabilities."""
        return [
            {
                "scenario": "Card Testing",
                "description": "Multiple small transactions to test if card is valid",
                "transactions": [
                    {
                        "transaction_id": "TXN_TEST_001",
                        "user_id": "USER_33333",
                        "amount": 1.00,
                        "merchant": "Online Merchant A",
                        "timestamp": "2024-01-17T10:00:00Z"
                    },
                    {
                        "transaction_id": "TXN_TEST_002", 
                        "user_id": "USER_33333",
                        "amount": 1.50,
                        "merchant": "Online Merchant B",
                        "timestamp": "2024-01-17T10:05:00Z"
                    },
                    {
                        "transaction_id": "TXN_TEST_003",
                        "user_id": "USER_33333", 
                        "amount": 2.00,
                        "merchant": "Online Merchant C",
                        "timestamp": "2024-01-17T10:10:00Z"
                    }
                ],
                "expected_risk": "high",
                "reasoning": "Pattern of small test transactions across multiple merchants"
            },
            {
                "scenario": "Geographic Impossibility",
                "description": "Transactions in locations too far apart in short time",
                "transactions": [
                    {
                        "transaction_id": "TXN_GEO_001",
                        "user_id": "USER_44444",
                        "amount": 50.00,
                        "merchant": "Restaurant NYC",
                        "location": "New York, NY",
                        "timestamp": "2024-01-17T12:00:00Z"
                    },
                    {
                        "transaction_id": "TXN_GEO_002",
                        "user_id": "USER_44444",
                        "amount": 75.00,
                        "merchant": "Gas Station LA",
                        "location": "Los Angeles, CA", 
                        "timestamp": "2024-01-17T12:30:00Z"
                    }
                ],
                "expected_risk": "high",
                "reasoning": "Impossible to travel from NYC to LA in 30 minutes"
            },
            {
                "scenario": "Spending Pattern Anomaly",
                "description": "Sudden large purchases inconsistent with user history",
                "user_context": {
                    "typical_spending": 50.00,
                    "max_previous_transaction": 200.00
                },
                "transactions": [
                    {
                        "transaction_id": "TXN_ANOM_001",
                        "user_id": "USER_55555",
                        "amount": 5000.00,
                        "merchant": "Jewelry Store",
                        "timestamp": "2024-01-17T14:00:00Z"
                    }
                ],
                "expected_risk": "high",
                "reasoning": "Transaction amount 25x higher than typical spending"
            }
        ]

# Utility functions for easy access
def get_sample_transaction():
    """Returns a single sample transaction for quick testing."""
    return TransactionData.get_legitimate_transactions()[0]

def get_fraud_example():
    """Returns a single fraud example for quick testing."""
    return TransactionData.get_fraudulent_transactions()[0]

def print_transaction_summary():
    """Prints a summary of all available sample data."""
    legitimate = len(TransactionData.get_legitimate_transactions())
    suspicious = len(TransactionData.get_suspicious_transactions())
    fraudulent = len(TransactionData.get_fraudulent_transactions())
    
    print(f"Sample Transaction Data Summary:")
    print(f"- Legitimate transactions: {legitimate}")
    print(f"- Suspicious transactions: {suspicious}")
    print(f"- Fraudulent transactions: {fraudulent}")
    print(f"- Total transactions: {legitimate + suspicious + fraudulent}")
    print(f"- User profiles: {len(TransactionData.get_user_profiles())}")
    print(f"- Fraud scenarios: {len(TransactionData.get_fraud_detection_scenarios())}")

if __name__ == "__main__":
    print_transaction_summary()
    print("\nSample legitimate transaction:")
    print(json.dumps(get_sample_transaction(), indent=2))
    print("\nSample fraud transaction:")
    print(json.dumps(get_fraud_example(), indent=2))