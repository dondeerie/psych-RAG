# Psychology Course RAG System

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system for analyzing psychology course data using LangChain and OpenAI. The system processes both quantitative (grades, attendance, study hours) and qualitative (student feedback, learning assessments) data to provide insights about student performance and learning patterns.

## Features
- **Interactive Query System**: Ask questions about student performance, study patterns, and course feedback
- **Demographic Filtering**: Filter analysis by:
  - Gender (Female/Male/Non-binary)
  - International Student Status
  - First-Generation Student Status
- **Comparative Analysis**: Compare performance and patterns across different student groups
- **Data Validation**: Includes sample size warnings and data quality checks
- **Enhanced Error Handling**: Robust error management for various edge cases

## Technologies Used
- Python 3.x
- LangChain
- FAISS for vector storage
- OpenAI GPT-3.5
- HuggingFace Embeddings
- Pandas for data processing

## Project Status
🚧 Under Development