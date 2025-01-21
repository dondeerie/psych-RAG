"""
Advanced Query Examples for Psychology Course RAG System

This script demonstrates advanced usage patterns including:
- Comparative analysis
- Multi-filter queries
- Complex pattern analysis
- Gender-based analysis
- Study pattern correlations
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

def run_advanced_analysis():
    """Run advanced analysis examples demonstrating complex queries."""
    # Initialize the system
    data_path = os.path.join(parent_dir, 'data')
    print("Initializing RAG system for advanced analysis...")
    print(f"Using data path: {data_path}")
    
    try:
        vectorstore, llm, df = setup_rag(data_path)
    except Exception as e:
        print(f"Error initializing system: {str(e)}")
        return

    # Example 1: Comparative Analysis
    print("\n1. Comparative Analysis Example")
    try:
        comparative_query = "Compare the performance of international and domestic students in final exams"
        response = query_rag(vectorstore, llm, comparative_query, None)
        print(f"Comparative Analysis:\n{response}")
    except Exception as e:
        print(f"Error in comparative analysis: {str(e)}")

    # Example 2: Gender-Based Study Patterns
    print("\n2. Gender-Based Analysis Example")
    try:
        # Analysis for each gender
        for gender in ["Female", "Male", "Non-binary"]:
            query = f"What are the typical study habits and performance patterns of {gender} students?"
            response = query_rag(
                vectorstore,
                llm,
                query,
                {"gender": gender}
            )
            print(f"\n{gender} Student Analysis:\n{response}")
    except Exception as e:
        print(f"Error in gender analysis: {str(e)}")

    # Example 3: Complex Pattern Analysis
    print("\n3. Complex Pattern Analysis Example")
    try:
        pattern_query = """
        Among students who study more than 8 hours per week:
        1. What is their typical attendance rate?
        2. How do they perform in exams?
        3. What common themes appear in their feedback?
        """
        response = query_rag(vectorstore, llm, pattern_query, None)
        print(f"Pattern Analysis:\n{response}")
    except Exception as e:
        print(f"Error in pattern analysis: {str(e)}")

if __name__ == "__main__":
    run_advanced_analysis()