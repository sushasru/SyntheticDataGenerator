from flask import Flask, request, jsonify, render_template_string, send_file
from werkzeug.utils import secure_filename
from synthetic_data_agent import SyntheticDataAgent
import os
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = '/app/uploads'
agent = SyntheticDataAgent()

# Ensure directories exist
os.makedirs('/app/uploads', exist_ok=True)
os.makedirs('/app/output', exist_ok=True)

# HTML template with file upload
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Synthetic Data AI Agent</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 900px; 
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
        textarea, input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            resize: vertical;
            box-sizing: border-box;
        }
        input[type="number"] {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 5px;
            width: 120px;
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
        .file-feature {
            background-color: #e8f5e8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 2px solid #28a745;
        }
        .examples h3, .file-feature h3 {
            margin-top: 0;
            color: #0066cc;
        }
        .file-feature h3 {
            color: #28a745;
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
        .file-info {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Synthetic Data AI Agent</h1>
        
        <div class="file-feature">
            <h3>🆕 NEW: File Analysis Feature!</h3>
            <p><strong>📁 Upload your data files (CSV, Excel, PDF)</strong> and the AI will analyze patterns, 
            column types, value distributions, and statistical properties to generate realistic synthetic data 
            that matches your historical data structure.</p>
            <p><strong>Supported formats:</strong> .csv, .xlsx, .xls, .pdf</p>
        </div>
        
        <div class="examples">
            <h3>Example Requests:</h3>
            <ul>
                <li>"I need 100 customer records with email and phone"</li>
                <li>"Generate 200 equipment items with completion tracking"</li>
                <li>"Create 50 sales transactions for last quarter"</li>
                <li><strong style="color: #28a745;">"Create synthetic data based on my uploaded file"</strong></li>
                <li><strong style="color: #28a745;">"Generate 500 records matching the patterns in my CSV"</strong></li>
            </ul>
        </div>
        
        <form id="dataForm" enctype="multipart/form-data">
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
            
            <div class="form-group">
                <label for="dataFile">📁 Upload Data File (CSV, Excel, PDF) - Optional:</label>
                <input type="file" id="dataFile" name="dataFile" accept=".csv,.xlsx,.xls,.pdf">
                <div class="file-info">
                    <strong>How it works:</strong> Upload your historical data and the AI will learn your patterns 
                    (value ranges, formats, distributions) to create realistic synthetic data.
                </div>
            </div>
            
            <div class="form-group">
                <label for="schema">Custom Schema (JSON format) - Optional:</label>
                <textarea 
                    id="schema" 
                    name="schema" 
                    rows="6" 
                    placeholder='Leave empty for auto-detection, or specify custom schema:
{
  "employee_id": {"type": "integer", "description": "Unique employee ID"},
  "full_name": {"type": "string", "description": "Employee full name"},
  "salary": {"type": "float", "description": "Annual salary"},
  "email": {"type": "email", "description": "Work email"}
}'
                ></textarea>
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
            const schema = formData.get('schema');
            const dataFile = formData.get('dataFile');
            
            const resultDiv = document.getElementById('result');
            const agentResponse = document.getElementById('agentResponse');
            
            resultDiv.style.display = 'block';
            
            if (dataFile && dataFile.size > 0) {
                agentResponse.innerHTML = '🤖 Agent: Analyzing your uploaded file and generating data...';
            } else {
                agentResponse.innerHTML = '🤖 Agent: Analyzing your request and generating data...';
            }
            
            try {
                // Parse schema if provided
                if (schema && schema.trim()) {
                    try {
                        JSON.parse(schema);
                    } catch (e) {
                        agentResponse.innerHTML = '❌ Invalid JSON in schema field. Please check the format.';
                        return;
                    }
                }
                
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    agentResponse.innerHTML = result.agent_messages.join('<br>');
                    currentFilename = result.filename;
                    document.getElementById('downloadSection').style.display = 'block';
                    document.getElementById('preview').style.display = 'none';
                    
                    if (result.used_file_analysis) {
                        agentResponse.innerHTML += '<br><strong style="color: #28a745;">✅ Used file analysis patterns!</strong>';
                    }
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
            document.getElementById('schema').value = '';
            document.getElementById('dataFile').value = '';
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
        user_request = request.form.get('request', '')
        num_records = request.form.get('records')
        custom_schema_json = request.form.get('schema')
        uploaded_file = request.files.get('dataFile')
        
        # Parse custom schema if provided
        custom_schema = None
        if custom_schema_json:
            try:
                custom_schema = json.loads(custom_schema_json)
            except:
                return jsonify({
                    'success': False,
                    'error': 'Invalid JSON in schema field'
                })
        
        # Modify request if specific number provided
        if num_records:
            user_request = f"{user_request} with {num_records} records"
        
        file_patterns = None
        messages = ['🤖 Agent: Analyzing your request...']
        
        # Handle file upload and analysis
        if uploaded_file and uploaded_file.filename:
            try:
                # Save uploaded file
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join('/app/uploads', filename)
                uploaded_file.save(file_path)
                
                # Determine file type
                file_ext = filename.split('.')[-1].lower()
                
                messages.append(f'🤖 Agent: Analyzing uploaded {file_ext.upper()} file...')
                
                # Analyze the file
                file_patterns = agent.analyze_uploaded_file(file_path, file_ext)
                
                if 'error' in file_patterns:
                    messages.append(f'❌ File analysis error: {file_patterns["error"]}')
                    messages.append('🤖 Agent: Falling back to standard generation...')
                    file_patterns = None
                else:
                    messages.append('✅ File analysis complete! Using learned patterns...')
                    if file_patterns.get('num_rows'):
                        messages.append(f'📊 Found {file_patterns["num_rows"]} rows, {file_patterns["num_columns"]} columns')
                    
                # Clean up uploaded file
                try:
                    os.remove(file_path)
                except:
                    pass
                    
            except Exception as e:
                messages.append(f'❌ File upload error: {str(e)}')
                messages.append('🤖 Agent: Falling back to standard generation...')
                file_patterns = None
        
        # Generate data
        synthetic_data = agent.generate_data(user_request, 
                                           custom_schema=custom_schema, 
                                           file_patterns=file_patterns)
        
        # Save to output directory
        filename = f"synthetic_data_{len(synthetic_data)}_records.csv"
        full_path = os.path.join('/app/output', filename)
        synthetic_data.to_csv(full_path, index=False)
        
        # Update messages
        if file_patterns:
            messages.append(f'🤖 Agent: Generated {len(synthetic_data)} records using your file patterns!')
        elif custom_schema:
            messages.append(f'🤖 Agent: Generated {len(synthetic_data)} records using your custom schema!')
        else:
            messages.append(f'🤖 Agent: Generated {len(synthetic_data)} records successfully!')
            
        messages.append('🤖 Agent: Data saved and ready for download!')
        
        return jsonify({
            'success': True,
            'agent_messages': messages,
            'filename': filename,
            'records_generated': len(synthetic_data),
            'used_file_analysis': file_patterns is not None
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
