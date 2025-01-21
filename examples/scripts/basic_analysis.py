"""
Basic Analysis Examples for Psychology Course RAG System

This script demonstrates basic usage of the RAG system for analyzing course data.
Note: This script uses synthetic data for demonstration purposes.
"""

import sys
import os

# Fix the path to properly find the ragpsy module
current_dir = os.path.dirname(os.path.abspath(__file__))  # /examples/scripts
parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Project root
sys.path.append(parent_dir)

try:
    from ragpsy import setup_rag, query_rag
except ModuleNotFoundError:
    print("Error: Cannot find ragpsy module.")
    print(f"Looking in: {parent_dir}")
    print("Make sure ragpsy.py is in the project root directory")
    sys.exit(1)

def run_basic_analysis():
    """Run basic analysis examples on course data."""
    # Initialize the system
    data_path = os.path.join(parent_dir, 'data')
    print("Initializing RAG system...")
    print(f"Using data path: {data_path}")
    
    try:
        vectorstore, llm, df = setup_rag(data_path)
    except Exception as e:
        print(f"Error initializing system: {str(e)}")
        print("Check your data path and file structure")
        return

    # Example 1: Basic Performance Query
    print("\nAnalyzing overall performance...")
    try:
        performance_query = "What is the overall distribution of final exam scores?"
        response = query_rag(vectorstore, llm, performance_query, None)
        print(f"Performance Analysis:\n{response}")
    except Exception as e:
        print(f"Error in performance analysis: {str(e)}")
    
    # Example 2: Study Habits Query
    print("\nAnalyzing study habits...")
    try:
        study_query = "What are the typical study patterns of high-performing students?"
        response = query_rag(vectorstore, llm, study_query, None)
        print(f"Study Habits Analysis:\n{response}")
    except Exception as e:
        print(f"Error in study habits analysis: {str(e)}")
    
    # Example 3: Filtered Analysis
    print("\nAnalyzing international students...")
    try:
        international_query = "How do international students perform?"
        filter_metadata = {"international_student": "Yes"}
        response = query_rag(
            vectorstore, 
            llm,
            international_query,
            filter_metadata
        )
        print(f"International Student Analysis:\n{response}")
    except Exception as e:
        print(f"Error in filtered analysis: {str(e)}")

if __name__ == "__main__":
    run_basic_analysis()