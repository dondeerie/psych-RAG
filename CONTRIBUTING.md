# Contributing to Psychology Course RAG System

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda)
- OpenAI API key

### Setting Up Development Environment
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/psych-rag.git
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Process

### Creating a New Feature
1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Implement your changes
3. Add tests for new functionality
4. Update documentation as needed

### Code Style Guidelines
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Include docstrings for all functions
- Keep functions focused and single-purpose

### Testing
- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Run tests with:
  ```bash
  python -m pytest
  ```

## Pull Request Process
1. Update documentation if needed
2. Run all tests
3. Create a clear PR description
4. Link to relevant issues
5. Wait for review and address any feedback

## Bug Reports
When reporting bugs, please include:
1. Description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. System information
6. Error messages/logs

## Feature Requests
When suggesting new features:
1. Describe the problem you're solving
2. Explain your proposed solution
3. Provide examples of use cases
4. Consider potential impacts

## Questions?
- Create an issue for questions
- Check existing documentation
- Join our discussions