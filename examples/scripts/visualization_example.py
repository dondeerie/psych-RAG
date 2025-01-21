"""
Visualization Examples for Psychology Course RAG System

This script demonstrates how to create visualizations of the RAG analysis results.
Note: This script requires matplotlib and seaborn packages.


Requirements:
    - matplotlib
    - seaborn
    - pandas

Note: These are additional requirements beyond the core RAG system.
Install using: pip install matplotlib seaborn pandas
"""

import sys
import os

# Fix the path to properly find the ragpsy module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

try:
    from ragpsy import setup_rag, query_rag
except ModuleNotFoundError:
    print("Error: Cannot find ragpsy module.")
    print(f"Looking in: {parent_dir}")
    print("Make sure ragpsy.py is in the project root directory")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    print("Error: This script requires matplotlib and seaborn.")
    print("Install them using: pip install matplotlib seaborn")
    sys.exit(1)

def create_visualizations():
    """Create various visualizations of the course data."""
    # Initialize the system
    data_path = os.path.join(parent_dir, 'data')
    print("Initializing RAG system and loading data...")
    print(f"Using data path: {data_path}")
    
    try:
        vectorstore, llm, df = setup_rag(data_path)
        if df is None:
            print("Error: No DataFrame available for visualization")
            return
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return

    # Example 1: Grade Distribution
    try:
        plt.figure(figsize=(10, 6))
        print("\nCreating grade distribution plot...")
        
        # Convert final_exam to numeric if it's not already
        df['final_exam'] = pd.to_numeric(df['final_exam'], errors='coerce')
        
        sns.histplot(data=df, x='final_exam', hue='gender', multiple="stack")
        plt.title('Final Exam Score Distribution by Gender')
        plt.xlabel('Final Exam Score')
        plt.ylabel('Count')
        plt.savefig(os.path.join(parent_dir, 'examples', 'visualizations', 'grade_distribution.png'))
        plt.close()
        print("Grade distribution plot saved")
    except Exception as e:
        print(f"Error creating grade distribution plot: {str(e)}")

    # Example 2: Study Hours vs Performance
    try:
        plt.figure(figsize=(10, 6))
        print("\nCreating study hours vs performance plot...")
        
        # Convert study_hours to numeric
        df['study_hours_per_week'] = pd.to_numeric(df['study_hours_per_week'], errors='coerce')
        
        sns.scatterplot(
            data=df,
            x='study_hours_per_week',
            y='final_exam',
            hue='gender',
            style='international_student'
        )
        plt.title('Study Hours vs Final Exam Performance')
        plt.xlabel('Study Hours per Week')
        plt.ylabel('Final Exam Score')
        plt.savefig(os.path.join(parent_dir, 'examples', 'visualizations', 'study_hours.png'))
        plt.close()
        print("Study hours plot saved")
    except Exception as e:
        print(f"Error creating study hours plot: {str(e)}")

    # Example 3: Attendance Impact
    try:
        plt.figure(figsize=(12, 5))
        print("\nCreating attendance analysis plots...")
        
        # Convert attendance_rate to numeric
        df['attendance_rate'] = pd.to_numeric(df['attendance_rate'], errors='coerce')
        
        plt.subplot(1, 2, 1)
        sns.boxplot(data=df, x='attendance_rate', y='final_exam')
        plt.title('Attendance Impact on Final Exam')
        
        plt.subplot(1, 2, 2)
        sns.boxplot(data=df, x='international_student', y='attendance_rate')
        plt.title('Attendance Rates by Student Type')
        
        plt.tight_layout()
        plt.savefig(os.path.join(parent_dir, 'examples', 'visualizations', 'attendance_analysis.png'))
        plt.close()
        print("Attendance analysis plots saved")
    except Exception as e:
        print(f"Error creating attendance analysis plots: {str(e)}")

if __name__ == "__main__":
    # Create visualizations directory if it doesn't exist
    vis_dir = os.path.join(parent_dir, 'examples', 'visualizations')
    os.makedirs(vis_dir, exist_ok=True)
    
    # Import pandas here to avoid potential import issues
    try:
        import pandas as pd
    except ImportError:
        print("Error: This script requires pandas.")
        print("Install it using: pip install pandas")
        sys.exit(1)
    
    create_visualizations()