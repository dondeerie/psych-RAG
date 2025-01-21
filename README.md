# Psychology Course RAG System

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-demo-yellow.svg)
![Data](https://img.shields.io/badge/data-synthetic-lightgrey.svg)

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system for analyzing psychology course data using LangChain and OpenAI. The system processes both quantitative (grades, attendance, study hours) and qualitative (student feedback, learning assessments) data to provide insights about student performance and learning patterns.

⚠️ **Note**: This project uses synthetic data for demonstration purposes.

## Features
- **Interactive Query System**: Ask questions about student performance, study patterns, and course feedback
- **Demographic Filtering**: Filter analysis by:
  - Gender (Female/Male/Non-binary)
  - International Student Status
  - First-Generation Student Status
- **Comparative Analysis**: Compare performance and patterns across different student groups
- **Data Validation**: Includes sample size warnings and data quality checks
- **Enhanced Error Handling**: Robust error management for various edge cases
- **Visualization Capabilities**: Generate insightful plots and graphs

## Example Outputs

### Analysis Examples
```python
Query: "How do international students perform in final exams?"
Response: [Example response showing analysis of international student performance]

Query: "Compare male and female student performance"
Response: [Example response showing gender-based comparison]
```

### Visualization Examples
The system generates various visualizations to help understand patterns in the data:

1. Grade Distribution
   - Shows distribution of final exam scores by gender
   - Located in: examples/visualizations/grade_distribution.png

2. Study Hours Impact
   - Demonstrates correlation between study hours and performance
   - Located in: examples/visualizations/study_hours.png

3. Attendance Analysis
   - Visualizes relationship between attendance and academic performance
   - Located in: examples/visualizations/attendance_analysis.png

## Technologies Used
- Python 3.8+
- LangChain
- FAISS for vector storage
- OpenAI GPT-3.5
- HuggingFace Embeddings
- Pandas for data processing
- Matplotlib and Seaborn for visualizations

## Getting Started
See our [Getting Started Guide](examples/GETTING_STARTED.md) for detailed setup and usage instructions.

## Example Scripts
1. Basic Analysis: [examples/scripts/basic_analysis.py](examples/scripts/basic_analysis.py)
2. Advanced Queries: [examples/scripts/advanced_queries.py](examples/scripts/advanced_queries.py)
3. Visualizations: [examples/scripts/visualization_example.py](examples/scripts/visualization_example.py)

## Documentation
- [Full Documentation](docs/DOCUMENTATION.md)
- [Data Dictionary](data/README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- This is a demonstration project using synthetic data
- Created for educational purposes
- Developed by Don Deerie B. Dumayas