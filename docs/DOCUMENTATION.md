# Psychology Course RAG System Documentation

## ⚠️ Synthetic Data Notice
This system uses artificially generated data for demonstration purposes. All patterns, correlations, and insights are synthetic and should not be used to make real-world educational decisions. The data is structured to demonstrate the capabilities of the RAG system while maintaining privacy and avoiding the use of real student information.

## System Architecture

### Components Overview
1. **Data Processing Layer**
   - Handles CSV file loading and preprocessing
   - Manages data validation and cleaning
   - Creates document structures for vectorization

2. **Vector Storage Layer**
   - Uses FAISS for efficient similarity search
   - Manages document embeddings
   - Handles metadata filtering

3. **Query Processing Layer**
   - Processes user questions
   - Applies appropriate filters
   - Handles comparative analysis

4. **Response Generation Layer**
   - Generates context-aware responses
   - Manages conversation memory
   - Applies response validation

## API Reference

### Core Functions

#### `load_data(data_path)`
Loads and processes CSV files from the specified path.
- **Parameters**: data_path (str)
- **Returns**: pandas.DataFrame
- **Raises**: FileNotFoundError if data files missing

#### `create_student_documents(df)`
Creates structured documents from DataFrame.
- **Parameters**: df (pandas.DataFrame)
- **Returns**: List[Dict]
- **Document Structure**:
  ```python
  {
      "content": str,
      "metadata": {
          "student_id": str,
          "gender": str,
          "first_gen_student": str,
          "international_student": str
      }
  }
  ```

#### `query_rag(vectorstore, llm, question, filter_metadata)`
Processes queries and generates responses.
- **Parameters**:
  - vectorstore: FAISS vectorstore instance
  - llm: Language model instance
  - question (str)
  - filter_metadata (Dict, optional)
- **Returns**: str (response)

## Usage Examples

### Basic Queries
```python
# International student performance
response = query_rag(
    vectorstore,
    llm,
    "How do international students perform?",
    {"international_student": "Yes"}
)

# Gender-specific analysis
response = query_rag(
    vectorstore,
    llm,
    "What study patterns do female students show?",
    {"gender": "Female"}
)
```

### Comparative Analysis
```python
# Gender comparison
response = query_rag(
    vectorstore,
    llm,
    "Compare male and female student performance",
    None  # No filter for comparative questions
)
```

## Error Handling

### Common Errors and Solutions

1. **Data Loading Issues**
   - Check file paths
   - Verify CSV format
   - Ensure required columns exist

2. **Query Processing**
   - Invalid filter combinations
   - Empty result sets
   - Malformed queries

3. **Response Generation**
   - Context length limits
   - Invalid metadata
   - Missing required fields

## Best Practices

### Query Formation
1. Be specific in questions
2. Include relevant context
3. Use appropriate filters
4. Consider sample sizes

### Data Management
1. Regular validation
2. Monitor response quality
3. Track usage patterns

### System Performance
1. Optimize chunk sizes
2. Monitor memory usage
3. Cache common queries