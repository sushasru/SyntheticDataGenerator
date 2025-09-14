#!/usr/bin/env python3
"""
Synthetic Data AI Agent
A smart assistant that generates any kind of synthetic data you need
"""

import json
import random
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid
from faker import Faker
import numpy as np

class SyntheticDataAgent:
    def __init__(self):
        self.fake = Faker()
        self.supported_data_types = [
            "customer_data", "equipment_tracking", "sales_data", 
            "employee_records", "financial_transactions", "product_catalog",
            "time_series", "custom_schema"
        ]
        
    def understand_request(self, user_request: str) -> Dict[str, Any]:
        """
        AI-like understanding of what the user wants
        In a real agent, this would use LLM APIs, but we'll use smart pattern matching
        """
        request_lower = user_request.lower()
        
        # Detect data type
        data_type = "custom_schema"
        if any(word in request_lower for word in ["customer", "client", "user"]):
            data_type = "customer_data"
        elif any(word in request_lower for word in ["equipment", "platform", "item", "completion"]):
            data_type = "equipment_tracking"
        elif any(word in request_lower for word in ["sales", "revenue", "purchase"]):
            data_type = "sales_data"
        elif any(word in request_lower for word in ["employee", "staff", "hr"]):
            data_type = "employee_records"
        elif any(word in request_lower for word in ["transaction", "payment", "financial"]):
            data_type = "financial_transactions"
        elif any(word in request_lower for word in ["product", "inventory", "catalog"]):
            data_type = "product_catalog"
        elif any(word in request_lower for word in ["time series", "timeseries", "over time"]):
            data_type = "time_series"
            
        # Extract number of records
        import re
        numbers = re.findall(r'\d+', user_request)
        num_records = 100  # default
        if numbers:
            num_records = int(numbers[0])
            
        return {
            "data_type": data_type,
            "num_records": num_records,
            "original_request": user_request
        }
    
    def generate_customer_data(self, num_records: int) -> pd.DataFrame:
        """Generate realistic customer data"""
        customers = []
        for _ in range(num_records):
            customers.append({
                'customer_id': str(uuid.uuid4())[:8],
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'email': self.fake.email(),
                'phone': self.fake.phone_number(),
                'address': self.fake.address().replace('\n', ', '),
                'signup_date': self.fake.date_between(start_date='-2y', end_date='today'),
                'age': random.randint(18, 80),
                'annual_income': random.randint(30000, 150000),
                'customer_segment': random.choice(['Premium', 'Standard', 'Basic']),
                'is_active': random.choice([True, False], weights=[0.8, 0.2])
            })
        return pd.DataFrame(customers)
    
    def generate_equipment_tracking(self, num_records: int) -> pd.DataFrame:
        """Generate equipment tracking data like your use case"""
        equipment_data = []
        
        # Generate equipment platforms
        num_platforms = max(1, num_records // 50)  # Each platform has ~50 items
        
        for platform_id in range(1, num_platforms + 1):
            num_items = random.randint(30, 80)  # Realistic range per platform
            
            for item_id in range(1, num_items + 1):
                # Create realistic completion patterns
                completion_pct = self._generate_realistic_completion()
                
                equipment_data.append({
                    'platform_id': f'PLAT-{platform_id:03d}',
                    'item_id': f'ITEM-{platform_id:03d}-{item_id:03d}',
                    'item_name': self.fake.catch_phrase(),
                    'item_type': random.choice(['Hardware', 'Software', 'Testing', 'Integration', 'Documentation']),
                    'completion_percentage': completion_pct,
                    'due_date': self.fake.date_between(start_date='-30d', end_date='+90d'),
                    'assigned_team': random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Echo']),
                    'priority': random.choice(['High', 'Medium', 'Low'], weights=[0.2, 0.6, 0.2]),
                    'estimated_hours': random.randint(8, 120),
                    'actual_hours': random.randint(5, 150) if completion_pct > 0 else 0,
                    'status': self._get_status_from_completion(completion_pct)
                })
                
                if len(equipment_data) >= num_records:
                    break
            
            if len(equipment_data) >= num_records:
                break
                
        return pd.DataFrame(equipment_data[:num_records])
    
    def _generate_realistic_completion(self) -> float:
        """Generate realistic completion percentages that cluster around certain values"""
        # Real projects tend to cluster around 0%, 25%, 50%, 75%, 100%
        clusters = [0, 25, 50, 75, 100]
        weights = [0.15, 0.2, 0.3, 0.25, 0.1]  # More items in middle stages
        
        base = random.choices(clusters, weights=weights)[0]
        # Add some noise
        noise = random.uniform(-10, 10)
        completion = max(0, min(100, base + noise))
        return round(completion, 1)
    
    def _get_status_from_completion(self, completion_pct: float) -> str:
        if completion_pct == 0:
            return 'Not Started'
        elif completion_pct < 25:
            return 'Planning'
        elif completion_pct < 75:
            return 'In Progress'
        elif completion_pct < 100:
            return 'Almost Done'
        else:
            return 'Completed'
    
    def generate_sales_data(self, num_records: int) -> pd.DataFrame:
        """Generate sales transaction data"""
        sales = []
        for _ in range(num_records):
            sales.append({
                'transaction_id': str(uuid.uuid4())[:12],
                'customer_id': str(uuid.uuid4())[:8],
                'product_name': self.fake.catch_phrase(),
                'category': random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books']),
                'quantity': random.randint(1, 10),
                'unit_price': round(random.uniform(10, 500), 2),
                'total_amount': 0,  # Will calculate below
                'transaction_date': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash']),
                'sales_rep': self.fake.name(),
                'region': random.choice(['North', 'South', 'East', 'West', 'Central'])
            })
            # Calculate total
            sales[-1]['total_amount'] = round(sales[-1]['quantity'] * sales[-1]['unit_price'], 2)
            
        return pd.DataFrame(sales)
    
    def generate_time_series(self, num_records: int) -> pd.DataFrame:
        """Generate time series data"""
        start_date = datetime.now() - timedelta(days=num_records)
        dates = [start_date + timedelta(days=i) for i in range(num_records)]
        
        # Generate trending data with some noise
        base_value = 100
        trend = 0.1
        values = []
        
        for i, date in enumerate(dates):
            trend_value = base_value + (trend * i)
            noise = random.gauss(0, 10)
            seasonal = 20 * np.sin(2 * np.pi * i / 30)  # 30-day cycle
            value = max(0, trend_value + noise + seasonal)
            values.append(round(value, 2))
            
        return pd.DataFrame({
            'date': dates,
            'value': values,
            'category': [random.choice(['A', 'B', 'C']) for _ in range(num_records)]
        })
    
    def generate_custom_schema(self, schema: Dict[str, str], num_records: int) -> pd.DataFrame:
        """Generate data based on custom schema provided by user"""
        data = []
        
        for _ in range(num_records):
            record = {}
            for field_name, field_type in schema.items():
                if field_type.lower() in ['string', 'text', 'name']:
                    record[field_name] = self.fake.word()
                elif field_type.lower() in ['email']:
                    record[field_name] = self.fake.email()
                elif field_type.lower() in ['int', 'integer', 'number']:
                    record[field_name] = random.randint(1, 1000)
                elif field_type.lower() in ['float', 'decimal']:
                    record[field_name] = round(random.uniform(0, 1000), 2)
                elif field_type.lower() in ['date']:
                    record[field_name] = self.fake.date()
                elif field_type.lower() in ['bool', 'boolean']:
                    record[field_name] = random.choice([True, False])
                else:
                    record[field_name] = self.fake.word()  # fallback
            data.append(record)
            
        return pd.DataFrame(data)
    
    def generate_data(self, request: str, custom_schema: Dict[str, str] = None) -> pd.DataFrame:
        """Main method - the AI agent's brain"""
        print(f"🤖 Agent: Analyzing your request...")
        
        # Understand what user wants
        analysis = self.understand_request(request)
        print(f"🤖 Agent: I understand you want {analysis['data_type']} with {analysis['num_records']} records")
        
        # Generate appropriate data
        if analysis['data_type'] == 'customer_data':
            data = self.generate_customer_data(analysis['num_records'])
        elif analysis['data_type'] == 'equipment_tracking':
            data = self.generate_equipment_tracking(analysis['num_records'])
        elif analysis['data_type'] == 'sales_data':
            data = self.generate_sales_data(analysis['num_records'])
        elif analysis['data_type'] == 'time_series':
            data = self.generate_time_series(analysis['num_records'])
        elif analysis['data_type'] == 'custom_schema' and custom_schema:
            data = self.generate_custom_schema(custom_schema, analysis['num_records'])
        else:
            print("🤖 Agent: I'll create some sample customer data as default")
            data = self.generate_customer_data(analysis['num_records'])
        
        print(f"🤖 Agent: Generated {len(data)} records successfully!")
        return data
    
    def save_data(self, data: pd.DataFrame, filename: str = None):
        """Save generated data"""
        if filename is None:
            filename = f"synthetic_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        data.to_csv(filename, index=False)
        print(f"🤖 Agent: Data saved to {filename}")
        return filename


# Example usage and testing
if __name__ == "__main__":
    # Create the AI agent
    agent = SyntheticDataAgent()
    
    print("=== Synthetic Data AI Agent Demo ===\n")
    
    # Example 1: Equipment data (your use case)
    print("Example 1: Equipment tracking data")
    equipment_data = agent.generate_data("I need 200 equipment platform items with completion tracking")
    print(f"Sample data:\n{equipment_data.head()}\n")
    
    # Example 2: Customer data
    print("Example 2: Customer data")
    customer_data = agent.generate_data("Generate 50 customer records for my CRM")
    print(f"Sample data:\n{customer_data.head()}\n")
    
    # Example 3: Custom schema
    print("Example 3: Custom schema")
    my_schema = {
        'employee_id': 'integer',
        'name': 'string',
        'department': 'string',
        'salary': 'float',
        'hire_date': 'date',
        'is_manager': 'boolean'
    }
    custom_data = agent.generate_data("I need employee data", custom_schema=my_schema)
    print(f"Sample data:\n{custom_data.head()}\n")
    
    print("=== Agent Ready for Use! ===")