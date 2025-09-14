#!/bin/bash

# Complete setup script for Synthetic Data AI Agent
echo "🚀 Setting up Synthetic Data AI Agent..."

# Create project directory
mkdir -p synthetic-data-agent
cd synthetic-data-agent

echo "📁 Creating project files..."

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY synthetic_data_agent.py .
COPY app.py .

# Create output directory for generated files
RUN mkdir -p /app/output

# Expose port for web interface
EXPOSE 8080

# Run the web application
CMD ["python", "app.py"]
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
pandas==2.1.4
numpy==1.24.3
faker==22.0.0
flask==3.0.0
streamlit==1.29.0
EOF

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  synthetic-data-agent:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./output:/app/output
    environment:
      - FLASK_ENV=development
    restart: unless-stopped
EOF

# Create the main AI agent Python file
cat > synthetic_data_agent.py << 'EOF'
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
EOF

# Create the Flask web app
cat > app.py << 'EOF'
from flask import Flask, request, jsonify, render_template_string, send_file
from synthetic_data_agent import SyntheticDataAgent
import os
import json

app = Flask(__name__)
agent = SyntheticDataAgent()

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Synthetic Data AI Agent</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #333; 
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            resize: vertical;
        }
        input[type="number"] {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 5px;
            width: 100px;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-right: 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }
        .examples {
            background-color: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .examples h3 {
            margin-top: 0;
            color: #0066cc;
        }
        .examples ul {
            margin-bottom: 0;
        }
        .agent-response {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Synthetic Data AI Agent</h1>
        
        <div class="examples">
            <h3>Example Requests:</h3>
            <ul>
                <li>"I need 100 customer records with email and phone"</li>
                <li>"Generate 200 equipment items with completion tracking"</li>
                <li>"Create 50 sales transactions for last quarter"</li>
                <li>"I want employee data with 75 records"</li>
                <li>"Generate time series data for 30 days"</li>
            </ul>
        </div>
        
        <form id="dataForm">
            <div class="form-group">
                <label for="request">What kind of data do you need?</label>
                <textarea 
                    id="request" 
                    name="request" 
                    rows="3" 
                    placeholder="Describe the data you need in plain English..."
                    required
                ></textarea>
            </div>
            
            <div class="form-group">
                <label for="records">Number of records (optional):</label>
                <input type="number" id="records" name="records" min="1" max="10000" placeholder="100">
            </div>
            
            <button type="submit">Generate Data 🚀</button>
            <button type="button" onclick="clearResults()">Clear Results</button>
        </form>
        
        <div id="result" class="result" style="display: none;">
            <h3>Results:</h3>
            <div id="agentResponse" class="agent-response"></div>
            <div id="downloadSection" style="display: none;">
                <button onclick="downloadData()">Download CSV 📥</button>
                <button onclick="viewPreview()">View Preview 👀</button>
            </div>
            <div id="preview" style="display: none; margin-top: 15px;">
                <h4>Data Preview (first 5 rows):</h4>
                <pre id="previewData"></pre>
            </div>
        </div>
    </div>

    <script>
        let currentFilename = null;
        
        document.getElementById('dataForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const request = formData.get('request');
            const records = formData.get('records');
            
            const resultDiv = document.getElementById('result');
            const agentResponse = document.getElementById('agentResponse');
            
            resultDiv.style.display = 'block';
            agentResponse.innerHTML = '🤖 Agent: Analyzing your request and generating data...';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        request: request,
                        records: records ? parseInt(records) : null
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    agentResponse.innerHTML = result.agent_messages.join('<br>');
                    currentFilename = result.filename;
                    document.getElementById('downloadSection').style.display = 'block';
                    document.getElementById('preview').style.display = 'none';
                } else {
                    agentResponse.innerHTML = '❌ Error: ' + result.error;
                    document.getElementById('downloadSection').style.display = 'none';
                }
            } catch (error) {
                agentResponse.innerHTML = '❌ Network error: ' + error.message;
            }
        });
        
        function downloadData() {
            if (currentFilename) {
                window.location.href = '/download/' + currentFilename;
            }
        }
        
        async function viewPreview() {
            if (currentFilename) {
                try {
                    const response = await fetch('/preview/' + currentFilename);
                    const result = await response.json();
                    
                    document.getElementById('previewData').textContent = result.preview;
                    document.getElementById('preview').style.display = 'block';
                } catch (error) {
                    alert('Error loading preview: ' + error.message);
                }
            }
        }
        
        function clearResults() {
            document.getElementById('result').style.display = 'none';
            document.getElementById('request').value = '';
            document.getElementById('records').value = '';
            currentFilename = null;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_data():
    try:
        data = request.get_json()
        user_request = data.get('request', '')
        num_records = data.get('records')
        
        # Modify request if specific number provided
        if num_records:
            user_request = f"{user_request} with {num_records} records"
        
        # Create output directory if it doesn't exist
        os.makedirs('/app/output', exist_ok=True)
        
        # Generate data
        synthetic_data = agent.generate_data(user_request)
        
        # Save to output directory
        filename = f"synthetic_data_{len(synthetic_data)}_records.csv"
        full_path = os.path.join('/app/output', filename)
        synthetic_data.to_csv(full_path, index=False)
        
        return jsonify({
            'success': True,
            'agent_messages': [
                f'🤖 Agent: Analyzing your request...',
                f'🤖 Agent: Generated {len(synthetic_data)} records successfully!',
                f'🤖 Agent: Data saved and ready for download!'
            ],
            'filename': filename,
            'records_generated': len(synthetic_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join('/app/output', filename), 
                        as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/preview/<filename>')
def preview_file(filename):
    try:
        import pandas as pd
        df = pd.read_csv(os.path.join('/app/output', filename))
        preview = df.head().to_string()
        return jsonify({'preview': preview})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
EOF

# Create output directory
mkdir -p output

# Create startup script
cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Synthetic Data AI Agent..."
echo "📦 Building Docker container..."
docker-compose build

echo "🏃 Running container..."
docker-compose up -d

echo "✅ Agent is running!"
echo "🌐 Open your browser to: http://localhost:8080"
echo ""
echo "To stop the agent: docker-compose down"
echo "To view logs: docker-compose logs -f"
EOF

chmod +x start.sh

echo "✅ Setup complete!"
echo ""
echo "📁 All files created in: $(pwd)"
echo "🚀 To start the AI agent, run: ./start.sh"
echo ""
echo "📋 Files created:"
ls -la
echo ""
echo "🎯 Next step: Run './start.sh' to start your AI agent!"