# RAG System Usage Examples

## Overview
This directory contains example scenarios and use cases for the Psychology Course RAG system. All examples use the synthetic dataset provided in the data directory.

## Example Scenarios

### 1. Basic Queries
```python
# Initialize the system
from ragpsy import setup_rag, query_rag

# Load the system
vectorstore, llm, df = setup_rag('path/to/data')

# Simple performance query
response = query_rag(
    vectorstore,
    llm,
    "What is the average final exam score?",
    None
)
```

### 2. Demographic Analysis
```python
# Gender-specific analysis
response = query_rag(
    vectorstore,
    llm,
    "How do female students perform in the course?",
    {"gender": "Female"}
)

# International student analysis
response = query_rag(
    vectorstore,
    llm,
    "What study patterns do international students show?",
    {"international_student": "Yes"}
)
```

### 3. Comparative Analysis
```python
# Compare different groups
response = query_rag(
    vectorstore,
    llm,
    "Compare study habits between international and domestic students",
    None  # No filter for comparative questions
)
```

### 4. Pattern Analysis
```python
# Study habits and performance
response = query_rag(
    vectorstore,
    llm,
    "Is there a correlation between study hours and final grades?",
    None
)
```

## Sample Questions
1. Performance Analysis:
   - "What's the grade distribution for the midterm?"
   - "How do attendance rates correlate with final grades?"
   - "What's the average performance difference between midterm and final?"

2. Student Feedback Analysis:
   - "What common themes appear in student feedback?"
   - "What aspects of the course do students find most challenging?"
   - "What positive feedback is most frequent?"

3. Study Pattern Analysis:
   - "What study habits lead to better performance?"
   - "How do study hours vary across different student groups?"
   - "Is there a relationship between attendance and study hours?"

## Usage Notes
- Remember this uses synthetic data for demonstration
- Response quality may vary based on question specificity
- Some analyses may be limited by sample size
- Complex queries may require multiple filter combinations

## Best Practices
1. Be specific in your questions
2. Consider sample size when filtering
3. Use appropriate filters for your analysis
4. Review the data documentation for context

## Error Handling Examples
```python
# Handle potential errors
try:
    response = query_rag(vectorstore, llm, question, filter_metadata)
    print(response)
except Exception as e:
    print(f"Error processing query: {str(e)}")
```