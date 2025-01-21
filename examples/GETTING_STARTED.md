# Getting Started with Psychology RAG Examples

## Project Structure and Navigation
```
psych-RAG/
├── examples/
│   ├── scripts/
│   │   ├── basic_analysis.py
│   │   ├── advanced_queries.py
│   │   └── visualization_example.py
│   └── GETTING_STARTED.md
├── data/
│   ├── psych101-quantitative.csv
│   ├── psych101-qualitative.csv
│   └── psych101-data-dictionary.md
├── ragpsy.py
└── .env
```

## Directory Navigation Guide

### Correct Directory Structure
✅ Good: Running from examples directory
```bash
cd /path/to/psych-RAG/examples
python scripts/basic_analysis.py
```

❌ Common Mistakes:
```bash
# Wrong: Running from project root
cd /path/to/psych-RAG
python scripts/basic_analysis.py  # Will fail

# Wrong: Running from scripts directory
cd /path/to/psych-RAG/examples/scripts
python basic_analysis.py  # May fail due to relative imports
```

## Common Errors and Solutions

### 1. Module Import Errors

#### Error: No module named 'ragpsy'
```bash
ModuleNotFoundError: No module named 'ragpsy'
```
Solutions:
- Check you're in the correct directory (examples/)
- Verify ragpsy.py exists in project root
- Check Python path:
```python
import sys
print(sys.path)  # Should include path to project root
```

### 2. File Path Errors

#### Error: Can't find data files
```bash
FileNotFoundError: [Errno 2] No such file or directory: '../../data/psych101-quantitative.csv'
```
Solutions:
- Verify data files exist in data/ directory
- Check relative path from script location
- Use absolute paths for testing:
```python
import os
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
print(f"Looking for data in: {data_path}")
```

### 3. API Key Errors

#### Error: OpenAI API key not found
```bash
Error setting up RAG: OpenAI API key not found
```
Solutions:
- Check .env file exists in project root
- Verify .env content:
```bash
OPENAI_API_KEY=your-api-key-here
```
- Try setting key directly in environment:
```bash
export OPENAI_API_KEY='your-api-key'
```

### 4. Data Loading Issues

#### Error: DataFrame column not found
```bash
KeyError: 'column_name'
```
Solutions:
- Verify CSV structure matches expected schema
- Print available columns:
```python
print(df.columns.tolist())
```
- Check for case sensitivity in column names

### 5. Directory Navigation Examples

Good Path:
```bash
# Start from any location
cd ~
# Navigate to examples directory
cd /path/to/psych-RAG/examples
# Run script
python scripts/basic_analysis.py
```

Common Wrong Paths:
```bash
# Wrong: Running from project root
cd /path/to/psych-RAG
python examples/scripts/basic_analysis.py  # Import error

# Wrong: Running from scripts
cd /path/to/psych-RAG/examples/scripts
python basic_analysis.py  # Path error

# Wrong: Running with incorrect relative path
cd /path/to/psych-RAG
python scripts/basic_analysis.py  # File not found
```

### 6. Debugging Tips

1. Check Current Directory:
```bash
pwd  # Print working directory
ls   # List files
```

2. Verify Python Path:
```python
import sys
import os
print("Current directory:", os.getcwd())
print("Python path:", sys.path)
```

3. Test Data Access:
```python
import os
def check_paths():
    print(f"Current directory: {os.getcwd()}")
    print(f"Script location: {os.path.dirname(__file__)}")
    print(f"Data directory exists: {os.path.exists('../../data')}")
```

## Quick Start Checklist

1. Directory Structure:
   - [ ] Project root contains ragpsy.py
   - [ ] data/ directory contains CSV files
   - [ ] examples/scripts/ contains analysis scripts

2. Environment:
   - [ ] Running from examples/ directory
   - [ ] All requirements installed
   - [ ] OpenAI API key configured

3. Common Checks:
   - [ ] Correct working directory
   - [ ] Python path includes project root
   - [ ] Data files accessible
   - [ ] Environment variables set

Need more help? Create an issue on GitHub with:
- Your current directory (output of pwd)
- The command you're running
- The full error message
- The output of ls in your current directory

## Important: Directory Location
When running example scripts, you must be in the correct directory:

### Method 1: Run from examples directory (Recommended)
```bash
# Navigate to examples directory
cd /path/to/psych-RAG/examples

# Run scripts from here
python scripts/basic_analysis.py
python scripts/advanced_queries.py
python scripts/visualization_example.py
```

### Method 2: Run using full path
```bash
# Can run from any location using full path
python /path/to/psych-RAG/examples/scripts/basic_analysis.py
```

### Common Directory Errors
If you see errors like:
```bash
No module named 'ragpsy'
```
or
```bash
Can't open file '.../scripts/basic_analysis.py'
```
→ Check that you're running the script from the correct directory!

## Prerequisites
Before running these examples, ensure you have:
1. Installed all requirements:
   ```bash
   pip install -r ../requirements.txt
   ```
2. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   # Or create a .env file in the project root
   ```
3. Downloaded or created your data files in the data directory

## Running the Examples

### Method 1: Direct Script Execution
Run any example script directly:
```bash
python scripts/basic_analysis.py
```

### Method 2: Import and Modify
Import the examples into your own scripts:
```python
from scripts.basic_analysis import run_basic_analysis
from scripts.advanced_queries import run_advanced_analysis

# Run the example
run_basic_analysis()

# Or modify for your needs
def my_custom_analysis():
    vectorstore, llm, df = setup_rag('path/to/your/data')
    # Your custom analysis here
```

### Method 3: Interactive Exploration
Use the example code snippets in a Python REPL or Jupyter notebook:
```python
# Import necessary functions
from ragpsy import setup_rag, query_rag

# Initialize the system
vectorstore, llm, df = setup_rag('path/to/data')

# Try different queries
response = query_rag(vectorstore, llm, "Your question here", filter_metadata=None)
```

## Adapting Examples for Your Use

### 1. Using Different Data
Replace the default data path with your own:
```python
# Original
vectorstore, llm, df = setup_rag('../../data')

# Modified for your data
vectorstore, llm, df = setup_rag('path/to/your/data')
```

### 2. Customizing Queries
Modify the example queries for your needs:
```python
# Example query
response = query_rag(vectorstore, llm, "What is the grade distribution?", None)

# Your custom query
response = query_rag(
    vectorstore,
    llm,
    "Your specific question",
    {"your_filter": "value"}
)
```

### 3. Adding Custom Filters
Create custom filters based on your data:
```python
# Example filter
filter_metadata = {"gender": "Female"}

# Your custom filter
filter_metadata = {
    "your_field": "your_value",
    "another_field": "another_value"
}
```

## Common Issues and Solutions

### 1. Path Issues
If you see path-related errors:
```python
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### 2. Data Loading Issues
Verify your data structure matches the expected format:
- Check CSV column names
- Ensure data types are correct
- Verify file paths

### 3. Query Issues
If you're not getting expected results:
- Be more specific in your questions
- Check your filter values
- Verify data sample size

## Getting Help
1. Check the documentation in /docs
2. Review example code comments
3. Create an issue on GitHub for bugs
4. Refer to notebooks for additional examples