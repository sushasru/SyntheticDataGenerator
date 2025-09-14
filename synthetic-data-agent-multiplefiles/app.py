
# app.py - Simple web interface
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
        
        # Capture agent messages
        messages = []
        
        # Generate data
        synthetic_data = agent.generate_data(user_request)
        
        # Save to output directory
        filename = agent.save_data(synthetic_data, 
                                 os.path.join('/app/output', 
                                 f"synthetic_data_{len(synthetic_data)}_records.csv"))
        
        return jsonify({
            'success': True,
            'agent_messages': [
                f'🤖 Agent: Analyzing your request...',
                f'🤖 Agent: Generated {len(synthetic_data)} records successfully!',
                f'🤖 Agent: Data saved and ready for download!'
            ],
            'filename': os.path.basename(filename),
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



