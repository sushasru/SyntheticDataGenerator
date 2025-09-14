#!/usr/bin/env python3
"""
Simplified synthetic data generator that works without external dependencies
This version uses only Python standard library components
"""

import csv
import json
import random
import uuid
from datetime import datetime, timedelta
import os

class SimpleSyntheticDataAgent:
    """Simplified version using only standard library"""
    
    def __init__(self):
        self.first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
        self.last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        self.domains = ["example.com", "test.com", "demo.com", "sample.org", "company.net"]
        self.teams = ["Alpha", "Beta", "Gamma", "Delta", "Echo"]
        self.priorities = ["High", "Medium", "Low"]
        self.categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
        
    def generate_customer_data(self, num_records=100):
        """Generate customer data using standard library only"""
        customers = []
        for i in range(num_records):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            customers.append({
                'customer_id': str(uuid.uuid4())[:8],
                'first_name': first_name,
                'last_name': last_name,
                'email': f"{first_name.lower()}.{last_name.lower()}@{random.choice(self.domains)}",
                'age': random.randint(18, 80),
                'signup_date': (datetime.now() - timedelta(days=random.randint(1, 730))).isoformat()[:10],
                'annual_income': random.randint(30000, 150000),
                'customer_segment': random.choice(['Premium', 'Standard', 'Basic']),
                'is_active': random.choice([True, False])
            })
        return customers
    
    def generate_equipment_data(self, num_records=100):
        """Generate equipment tracking data"""
        equipment = []
        num_platforms = max(1, num_records // 50)
        
        for platform_id in range(1, num_platforms + 1):
            items_per_platform = min(50, num_records - len(equipment))
            
            for item_id in range(1, items_per_platform + 1):
                completion = random.choice([0, 25, 50, 75, 100]) + random.randint(-10, 10)
                completion = max(0, min(100, completion))
                
                equipment.append({
                    'platform_id': f'PLAT-{platform_id:03d}',
                    'item_id': f'ITEM-{platform_id:03d}-{item_id:03d}',
                    'item_name': f'Equipment Item {platform_id}-{item_id}',
                    'completion_percentage': round(completion, 1),
                    'due_date': (datetime.now() + timedelta(days=random.randint(-30, 90))).isoformat()[:10],
                    'assigned_team': random.choice(self.teams),
                    'priority': random.choice(self.priorities),
                    'estimated_hours': random.randint(8, 120),
                    'status': self._get_status_from_completion(completion)
                })
                
                if len(equipment) >= num_records:
                    break
            
            if len(equipment) >= num_records:
                break
        
        return equipment[:num_records]
    
    def _get_status_from_completion(self, completion_pct):
        """Convert completion percentage to status"""
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
    
    def generate_sales_data(self, num_records=100):
        """Generate sales transaction data"""
        sales = []
        for i in range(num_records):
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(10, 500), 2)
            sales.append({
                'transaction_id': str(uuid.uuid4())[:12],
                'customer_id': str(uuid.uuid4())[:8],
                'product_name': f'Product {i+1}',
                'category': random.choice(self.categories),
                'quantity': quantity,
                'unit_price': unit_price,
                'total_amount': round(quantity * unit_price, 2),
                'transaction_date': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()[:10],
                'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash']),
                'region': random.choice(['North', 'South', 'East', 'West', 'Central'])
            })
        return sales
    
    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        if not data:
            print("No data to save")
            return
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Data saved to {filename} ({len(data)} records)")

def main():
    """Main function for testing and demonstration"""
    print("🤖 Simple Synthetic Data Generator")
    print("=" * 50)
    
    agent = SimpleSyntheticDataAgent()
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate different types of data
    print("\n1. Generating customer data...")
    customers = agent.generate_customer_data(50)
    agent.save_to_csv(customers, f"{output_dir}/customers.csv")
    print(f"Sample: {customers[0]}")
    
    print("\n2. Generating equipment data...")
    equipment = agent.generate_equipment_data(100)
    agent.save_to_csv(equipment, f"{output_dir}/equipment.csv")
    print(f"Sample: {equipment[0]}")
    
    print("\n3. Generating sales data...")
    sales = agent.generate_sales_data(75)
    agent.save_to_csv(sales, f"{output_dir}/sales.csv")
    print(f"Sample: {sales[0]}")
    
    print(f"\n✅ All data generated successfully!")
    print(f"📁 Check the '{output_dir}' directory for CSV files")

if __name__ == "__main__":
    main()