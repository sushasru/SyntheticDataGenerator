# 🤖 Synthetic Data Generator

A powerful AI-powered tool that generates realistic synthetic data for testing, development, and analysis. Simply describe what data you need in plain English, and the AI agent will create it for you.

## ✨ Features

- **🧠 AI-Powered Data Generation**: Describe your data needs in natural language
- **📁 File Upload & Analysis**: Upload CSV, Excel, or PDF files to learn data patterns
- **🔍 Pattern Learning**: AI analyzes your historical data to understand structure, value ranges, and distributions
- **📊 Multiple Data Types**: Support for various data formats and schemas
- **🌐 Web Interface**: User-friendly browser-based interface with file upload capabilities
- **📥 Export Options**: Download generated data as CSV files
- **👀 Data Preview**: View sample data before downloading
- **🐳 Docker Support**: Easy deployment with Docker and Docker Compose
- **⚡ Fast Generation**: Quickly generate thousands of records
- **🎯 Realistic Data**: Generate synthetic data that matches your actual data patterns

## 🎯 Supported Data Types

- **📁 File-Based Generation**: Upload your historical data (CSV, Excel, PDF) for pattern analysis
- **Customer Data**: Names, emails, addresses, demographics, and customer segments
- **Equipment Tracking**: Platform items with completion tracking, status, and assignments
- **Sales Data**: Transaction records, product information, and revenue data
- **Employee Records**: HR data with departments, salaries, and hire dates
- **Time Series Data**: Date-based data with trends and seasonal patterns
- **Financial Transactions**: Payment records and financial data
- **Custom Schemas**: Define your own data structure and types
- **Pattern-Matched Data**: Synthetic data that replicates your actual data distributions

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system
- Web browser for accessing the interface

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/sushasru/SyntheticDataGenerator.git
cd SyntheticDataGenerator
```

2. **Navigate to the project directory**:
```bash
cd synthetic-data-agent/synthetic-data-agent
```

3. **Start the application**:
```bash
./start.sh
```

4. **Access the web interface**:
   - Open your browser to `http://localhost:8080`
   - Start generating data!

### Alternative Setup (Manual)

If you prefer to run without the setup script:

```bash
# Build and run with Docker Compose
docker-compose build
docker-compose up -d

# Or build and run manually
docker build -t synthetic-data-agent .
docker run -p 8080:8080 -v ./output:/app/output synthetic-data-agent
```

### Simple Generator (No Dependencies)

For environments where external dependencies can't be installed, use the simple generator:

```bash
# Run the simplified version (uses only Python standard library)
python simple_generator.py
```

This will generate sample data files in the `output/` directory:
- `customers.csv` - Customer data with demographics
- `equipment.csv` - Equipment tracking data with completion status
- `sales.csv` - Sales transaction data

## 📖 Usage

### 🆕 NEW: File Upload & Pattern Analysis

The AI agent now supports uploading your historical data files to learn patterns and generate realistic synthetic data!

**Supported File Types**: CSV (.csv), Excel (.xlsx, .xls), PDF (.pdf)

**How it works**:
1. **Upload your file** through the web interface
2. **AI analyzes patterns** - column types, value distributions, ranges, and statistical properties
3. **Generate synthetic data** that matches your real data patterns
4. **Download realistic results** with the same structure and characteristics

**Example workflow**:
```bash
# 1. Start the application
./start.sh

# 2. Open browser to http://localhost:8080
# 3. Upload your CSV/Excel/PDF file
# 4. Enter: "Generate 500 records based on my uploaded data"
# 5. Download synthetic data that matches your patterns!
```

### Web Interface

1. **Open the application** in your browser at `http://localhost:8080`
2. **Describe your data needs** in the text area (e.g., "I need 100 customer records with email and phone")
3. **Specify the number of records** (optional)
4. **Click "Generate Data"** to create your synthetic data
5. **Preview or download** the generated CSV file

### Example Requests

**Traditional requests**:
- `"I need 100 customer records with email and phone"`
- `"Generate 200 equipment items with completion tracking"`
- `"Create 50 sales transactions for last quarter"`
- `"I want employee data with 75 records"`
- `"Generate time series data for 30 days"`

**🆕 File-based requests** (after uploading your data):
- `"Generate 500 records matching my uploaded CSV patterns"`
- `"Create synthetic data based on my historical sales file"`
- `"Generate 1000 customer records using my uploaded customer data"`
- `"Create test data that matches my Excel file structure"`

### Command Line Usage

You can also use the AI agent directly in Python:

```python
from synthetic_data_agent import SyntheticDataAgent

# Create the AI agent
agent = SyntheticDataAgent()

# Generate traditional data
customer_data = agent.generate_data("I need 100 customer records")
print(customer_data.head())

# 🆕 Analyze a file and generate based on patterns
file_patterns = agent.analyze_uploaded_file('your_data.csv', 'csv')
pattern_data = agent.generate_from_file_patterns(file_patterns, 500)
print(pattern_data.head())

# Generate with custom schema and file patterns
equipment_data = agent.generate_data(
    "Generate 200 equipment items", 
    file_patterns=file_patterns
)
print(equipment_data.head())

# Save data to file
agent.save_data(customer_data, "customers.csv")
```

**🆕 File Analysis Features**:
```python
# Analyze different file types
csv_patterns = agent.analyze_uploaded_file('data.csv', 'csv')
excel_patterns = agent.analyze_uploaded_file('data.xlsx', 'xlsx') 
pdf_patterns = agent.analyze_uploaded_file('data.pdf', 'pdf')

# Generate realistic synthetic data from patterns
synthetic_data = agent.generate_from_file_patterns(csv_patterns, 1000)
```

### Simple Generator (No External Dependencies)

For quick testing or environments without pandas/numpy:

```python
from simple_generator import SimpleSyntheticDataAgent

# Create the simple agent
agent = SimpleSyntheticDataAgent()

# Generate data
customers = agent.generate_customer_data(100)
equipment = agent.generate_equipment_data(200)
sales = agent.generate_sales_data(50)

# Save to CSV
agent.save_to_csv(customers, "output/customers.csv")
agent.save_to_csv(equipment, "output/equipment.csv")
agent.save_to_csv(sales, "output/sales.csv")
```

## 🛠️ Development

### Project Structure

```
SyntheticDataGenerator/
├── README.md                       # This file - project documentation
├── synthetic-data-agent/
│   ├── setup.sh                    # Setup script for creating the project
│   └── synthetic-data-agent/
│       ├── synthetic_data_agent.py # Core AI agent logic
│       ├── app.py                  # Flask web application
│       ├── simple_generator.py     # Simplified version (no dependencies)
│       ├── requirements.txt        # Python dependencies
│       ├── Dockerfile             # Docker container configuration
│       ├── Dockerfile.robust       # Docker with SSL bypass for restricted networks
│       ├── docker-compose.yml     # Docker Compose setup
│       ├── start.sh               # Application startup script
│       └── output/                # Generated data files
```

### Dependencies

- **Python 3.11+**
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **faker**: Generate fake data
- **flask**: Web framework
- **streamlit**: Alternative UI framework
- **🆕 openpyxl**: Excel file processing (.xlsx/.xls)
- **🆕 PyPDF2**: PDF file reading and analysis  
- **🆕 pdfplumber**: Advanced PDF text extraction
- **🆕 python-multipart**: File upload handling

### Local Development

1. **Install Python dependencies**:
```bash
pip install -r synthetic-data-agent/synthetic-data-agent/requirements.txt
```

2. **Run the Flask application**:
```bash
cd synthetic-data-agent/synthetic-data-agent
python app.py
```

3. **Run the AI agent directly**:
```bash
python synthetic_data_agent.py
```

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Set to `development` for debug mode
- `PORT`: Custom port for the web application (default: 8080)

### Data Generation Parameters

The AI agent supports various parameters:

- **Number of records**: 1 to 10,000 records per generation
- **Data types**: Automatically detected from natural language descriptions
- **Custom schemas**: Define your own field types and structures

## 📊 API Reference

### Web API Endpoints

#### `POST /generate`
Generate synthetic data based on a text description, with optional file upload for pattern analysis.

**Request Body** (form data):
```json
{
  "request": "I need 100 customer records",
  "records": 100,
  "schema": "{}",
  "dataFile": "<uploaded_file>"  // 🆕 Optional file upload
}
```

**Response**:
```json
{
  "success": true,
  "agent_messages": ["🤖 Agent: Generated 100 records successfully!"],
  "filename": "synthetic_data_100_records.csv",
  "records_generated": 100,
  "used_file_analysis": true  // 🆕 Indicates if file patterns were used
}
```

#### `GET /download/<filename>`
Download a generated CSV file.

#### `GET /preview/<filename>`
Get a preview of the first 5 rows of generated data.

### Python API

#### `SyntheticDataAgent.generate_data(request, custom_schema=None, file_patterns=None)`
Main method for generating synthetic data.

**Parameters**:
- `request` (str): Natural language description of desired data
- `custom_schema` (dict, optional): Custom field definitions
- `file_patterns` (dict, optional): 🆕 File analysis patterns for realistic generation

**Returns**: pandas.DataFrame with generated data

#### 🆕 `SyntheticDataAgent.analyze_uploaded_file(file_path, file_type)`
Analyze uploaded files to extract data patterns.

**Parameters**:
- `file_path` (str): Path to the uploaded file
- `file_type` (str): File type ('csv', 'xlsx', 'xls', 'pdf')

**Returns**: dict with extracted patterns, column types, and statistical information

#### 🆕 `SyntheticDataAgent.generate_from_file_patterns(patterns, num_records)`
Generate synthetic data based on learned file patterns.

**Parameters**:
- `patterns` (dict): Patterns extracted from analyze_uploaded_file()
- `num_records` (int): Number of records to generate

**Returns**: pandas.DataFrame with pattern-matched synthetic data

## 📈 Examples

### Traditional Data Generation

#### Customer Data
```python
agent = SyntheticDataAgent()
customers = agent.generate_data("100 customers with contact info")
```

**Generated columns**: customer_id, first_name, last_name, email, phone, address, signup_date, age, annual_income, customer_segment, is_active

#### Equipment Tracking
```python
equipment = agent.generate_data("200 equipment items with completion tracking")
```

**Generated columns**: platform_id, item_id, item_name, item_type, completion_percentage, due_date, assigned_team, priority, estimated_hours, actual_hours, status

#### Sales Data
```python
sales = agent.generate_data("50 sales transactions")
```

**Generated columns**: transaction_id, customer_id, product_name, category, quantity, unit_price, total_amount, transaction_date, payment_method, sales_rep, region

### 🆕 File-Based Data Generation

#### Analyze and Generate from CSV
```python
agent = SyntheticDataAgent()

# Analyze your historical data
patterns = agent.analyze_uploaded_file('historical_sales.csv', 'csv')
print(f"Found {patterns['num_columns']} columns, {patterns['num_rows']} rows")
print(f"Columns: {patterns['columns']}")

# Generate synthetic data matching your patterns
synthetic_sales = agent.generate_from_file_patterns(patterns, 1000)
print(synthetic_sales.head())
```

#### Excel File Analysis
```python
# Analyze Excel file
excel_patterns = agent.analyze_uploaded_file('employee_data.xlsx', 'xlsx')

# Generate realistic employee data
synthetic_employees = agent.generate_from_file_patterns(excel_patterns, 500)
```

#### Pattern-Aware Generation
```python
# Use file patterns with natural language requests
synthetic_data = agent.generate_data(
    "Generate 800 customer records with realistic patterns",
    file_patterns=patterns
)
```

**Benefits of file-based generation**:
- ✅ Realistic value distributions matching your actual data
- ✅ Proper data types and formats
- ✅ Statistical consistency with historical patterns
- ✅ Maintains relationships between columns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

**Port already in use**:
```bash
# Stop existing containers
docker-compose down

# Or use a different port
docker run -p 8081:8080 synthetic-data-agent
```

**Permission denied on start.sh**:
```bash
chmod +x start.sh
```

**Docker not found**:
- Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

**🆕 File Upload Issues**:

**File too large error**:
- Current limit is 100MB per file
- Try compressing your file or uploading a sample
- For larger files, use the Python API directly

**Unsupported file format**:
- Supported: .csv, .xlsx, .xls, .pdf
- Convert other formats to CSV first
- Check file extension is correct

**File analysis fails**:
```bash
# Check file encoding for CSV files
# Try saving CSV with UTF-8 encoding
# Ensure Excel files are not corrupted
# PDFs should contain structured text data
```

**Missing file processing dependencies**:
```bash
pip install openpyxl PyPDF2 pdfplumber python-multipart
```

**Network connectivity issues during pip install**:
- Try using a different package index: `pip install --index-url https://pypi.python.org/simple/ -r requirements.txt`
- Or install packages individually: `pip install pandas numpy faker flask openpyxl PyPDF2 pdfplumber`
- For SSL certificate issues in Docker, add `--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org` to pip install commands
- For offline environments, the dependencies can be pre-downloaded or use Docker which includes all dependencies

**Docker build fails with SSL errors**:
- This can happen in restricted network environments
- Try building with: `docker build --build-arg HTTP_PROXY=http://proxy:port --build-arg HTTPS_PROXY=http://proxy:port .`
- Or modify the Dockerfile to add SSL bypass options during pip install

### Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/sushasru/SyntheticDataGenerator/issues) page
2. Create a new issue with details about your problem
3. Include error messages and your environment details

## 🔮 Future Features

- [x] ✅ **File upload and pattern analysis** (CSV, Excel, PDF support)
- [x] ✅ **Statistical pattern learning** from historical data  
- [x] ✅ **Realistic data generation** based on learned patterns
- [ ] Integration with external APIs for enhanced data generation
- [ ] Support for JSON, XML, and other output formats
- [ ] Advanced data relationships and constraints
- [ ] Real-time data streaming capabilities
- [ ] Machine learning model training data generation
- [ ] Database direct export capabilities
- [ ] Multi-sheet Excel file support
- [ ] Advanced PDF table extraction
- [ ] Data anonymization and privacy controls

---

**Made with ❤️ by the Synthetic Data Generator team**