# 🤖 Synthetic Data Generator

A powerful AI-powered tool that generates realistic synthetic data for testing, development, and analysis. Simply describe what data you need in plain English, and the AI agent will create it for you.

## ✨ Features

- **🧠 AI-Powered Data Generation**: Describe your data needs in natural language
- **📊 Multiple Data Types**: Support for various data formats and schemas
- **🌐 Web Interface**: User-friendly browser-based interface
- **📥 Export Options**: Download generated data as CSV files
- **🔍 Data Preview**: View sample data before downloading
- **🐳 Docker Support**: Easy deployment with Docker and Docker Compose
- **⚡ Fast Generation**: Quickly generate thousands of records

## 🎯 Supported Data Types

- **Customer Data**: Names, emails, addresses, demographics, and customer segments
- **Equipment Tracking**: Platform items with completion tracking, status, and assignments
- **Sales Data**: Transaction records, product information, and revenue data
- **Employee Records**: HR data with departments, salaries, and hire dates
- **Time Series Data**: Date-based data with trends and seasonal patterns
- **Financial Transactions**: Payment records and financial data
- **Custom Schemas**: Define your own data structure and types

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

### Web Interface

1. **Open the application** in your browser at `http://localhost:8080`
2. **Describe your data needs** in the text area (e.g., "I need 100 customer records with email and phone")
3. **Specify the number of records** (optional)
4. **Click "Generate Data"** to create your synthetic data
5. **Preview or download** the generated CSV file

### Example Requests

- `"I need 100 customer records with email and phone"`
- `"Generate 200 equipment items with completion tracking"`
- `"Create 50 sales transactions for last quarter"`
- `"I want employee data with 75 records"`
- `"Generate time series data for 30 days"`

### Command Line Usage

You can also use the AI agent directly in Python:

```python
from synthetic_data_agent import SyntheticDataAgent

# Create the AI agent
agent = SyntheticDataAgent()

# Generate customer data
customer_data = agent.generate_data("I need 100 customer records")
print(customer_data.head())

# Generate equipment tracking data
equipment_data = agent.generate_data("Generate 200 equipment items with completion tracking")
print(equipment_data.head())

# Save data to file
agent.save_data(customer_data, "customers.csv")
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
Generate synthetic data based on a text description.

**Request Body**:
```json
{
  "request": "I need 100 customer records",
  "records": 100
}
```

**Response**:
```json
{
  "success": true,
  "agent_messages": ["🤖 Agent: Generated 100 records successfully!"],
  "filename": "synthetic_data_100_records.csv",
  "records_generated": 100
}
```

#### `GET /download/<filename>`
Download a generated CSV file.

#### `GET /preview/<filename>`
Get a preview of the first 5 rows of generated data.

### Python API

#### `SyntheticDataAgent.generate_data(request, custom_schema=None)`
Main method for generating synthetic data.

**Parameters**:
- `request` (str): Natural language description of desired data
- `custom_schema` (dict, optional): Custom field definitions

**Returns**: pandas.DataFrame with generated data

## 📈 Examples

### Customer Data
```python
agent = SyntheticDataAgent()
customers = agent.generate_data("100 customers with contact info")
```

**Generated columns**: customer_id, first_name, last_name, email, phone, address, signup_date, age, annual_income, customer_segment, is_active

### Equipment Tracking
```python
equipment = agent.generate_data("200 equipment items with completion tracking")
```

**Generated columns**: platform_id, item_id, item_name, item_type, completion_percentage, due_date, assigned_team, priority, estimated_hours, actual_hours, status

### Sales Data
```python
sales = agent.generate_data("50 sales transactions")
```

**Generated columns**: transaction_id, customer_id, product_name, category, quantity, unit_price, total_amount, transaction_date, payment_method, sales_rep, region

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

**Network connectivity issues during pip install**:
- Try using a different package index: `pip install --index-url https://pypi.python.org/simple/ -r requirements.txt`
- Or install packages individually: `pip install pandas numpy faker flask`
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

- [ ] Integration with external APIs for enhanced data generation
- [ ] Support for JSON, XML, and other output formats
- [ ] Advanced data relationships and constraints
- [ ] Real-time data streaming capabilities
- [ ] Machine learning model training data generation
- [ ] Database direct export capabilities

---

**Made with ❤️ by the Synthetic Data Generator team**