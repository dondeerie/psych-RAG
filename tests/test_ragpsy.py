import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from ragpsy import (
    load_data,
    create_student_documents,
    setup_rag,
    query_rag,
    validate_data_sample
)

class TestRAGSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data"""
        cls.test_data = pd.DataFrame({
            'student_id': ['PSY101_F24_001', 'PSY101_F24_002'],
            'gender': ['Female', 'Male'],
            'first_gen_student': ['Yes', 'No'],
            'international_student': ['No', 'Yes'],
            'midterm_grade': [85, 90],
            'final_exam': [88, 92],
            'study_hours_per_week': [10, 8],
            'attendance_rate': [95, 88],
            'course_review': ['Great course', 'Very challenging'],
            'learning_outcomes_assessment': ['Learned a lot', 'Good experience']
        })

    def test_load_data(self):
        """Test data loading functionality"""
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = self.test_data
            df = load_data('dummy_path')
            self.assertIsNotNone(df)
            self.assertEqual(len(df), 2)

    def test_document_creation(self):
        """Test document creation from dataframe"""
        documents = create_student_documents(self.test_data)
        self.assertEqual(len(documents), 2)
        self.assertIn('metadata', documents[0])
        self.assertIn('content', documents[0])

    def test_data_validation(self):
        """Test data validation functionality"""
        mock_docs = [
            MagicMock(metadata={'student_id': 'PSY101_F24_001'}),
            MagicMock(metadata={'student_id': 'PSY101_F24_002'})
        ]
        warning = validate_data_sample(mock_docs, None)
        self.assertIsInstance(warning, str)

    def test_query_processing(self):
        """Test query processing with mock data"""
        mock_vectorstore = MagicMock()
        mock_llm = MagicMock()
        mock_docs = [MagicMock(page_content="Test content")]
        mock_vectorstore.similarity_search.return_value = mock_docs
        
        response = query_rag(
            mock_vectorstore,
            mock_llm,
            "How do students perform?",
            None
        )
        self.assertIsNotNone(response)

    def test_invalid_input_handling(self):
        """Test system handling of invalid inputs"""
        mock_vectorstore = MagicMock()
        mock_llm = MagicMock()
        
        # Test empty question
        response = query_rag(mock_vectorstore, mock_llm, "", None)
        self.assertIn("longer", response.lower())
        
        # Test very short question
        response = query_rag(mock_vectorstore, mock_llm, "hi", None)
        self.assertIn("longer", response.lower())

    def test_gender_filter(self):
        """Test gender-specific filtering"""
        mock_vectorstore = MagicMock()
        mock_llm = MagicMock()
        mock_docs = [MagicMock(page_content="Female student data")]
        mock_vectorstore.similarity_search.return_value = mock_docs
        
        response = query_rag(
            mock_vectorstore,
            mock_llm,
            "How do female students perform?",
            {"gender": "Female"}
        )
        self.assertIsNotNone(response)

    def test_comparative_analysis(self):
        """Test comparative analysis functionality"""
        mock_vectorstore = MagicMock()
        mock_llm = MagicMock()
        mock_docs = [
            MagicMock(page_content="Male student data"),
            MagicMock(page_content="Female student data")
        ]
        mock_vectorstore.similarity_search.return_value = mock_docs
        
        response = query_rag(
            mock_vectorstore,
            mock_llm,
            "Compare male and female student performance",
            None
        )
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()