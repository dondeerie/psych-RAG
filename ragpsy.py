import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
from langchain.cache import InMemoryCache
from langchain.memory import ConversationBufferMemory 
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_community.cache import InMemoryCache  # Instead of from langchain.cache
from pydantic import BaseModel  # Instead of from langchain_core.pydantic_v1
import langchain

def load_data(data_path):
    """Load and merge relevant data from CSV files"""
    try:
        # Load datasets with specific columns
        quant_df = pd.read_csv(os.path.join(data_path, 'psych101-quantitative.csv'))
        qual_df = pd.read_csv(os.path.join(data_path, 'psych101-qualitative.csv'))
        
        # Select only the columns we need
        quant_cols = ['student_id', 'gender', 'first_gen_student', 'international_student',
                     'midterm_grade', 'final_exam', 'study_hours_per_week', 'attendance_rate']
        qual_cols = ['student_id', 'course_review', 'learning_outcomes_assessment']
        
        quant_df = quant_df[quant_cols]
        qual_df = qual_df[qual_cols]
        
        # Merge datasets
        merged_df = pd.merge(quant_df, qual_df, on='student_id')
        print(f"Loaded {len(merged_df)} student records")
        
        return merged_df
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def create_student_documents(df):
    """Create text documents for each student"""
    documents = []
    
    for _, row in df.iterrows():
        # Create a focused text document
        doc_text = f"""
        Student Demographics:
        - Gender: {row['gender']}
        - First Generation Student: {row['first_gen_student']}
        - International Student: {row['international_student']}

        Academic Performance:
        - Midterm Grade: {row['midterm_grade']}
        - Final Exam: {row['final_exam']}
        - Study Hours per Week: {row['study_hours_per_week']}
        - Attendance Rate: {row['attendance_rate']}

        Student Feedback:
        {row['course_review']}

        Learning Assessment:
        {row['learning_outcomes_assessment']}
        """
        
        # Create focused metadata
        metadata = {
            'student_id': row['student_id'],
            'international_student': row['international_student'],
            'first_gen_student': row['first_gen_student'],
            'final_exam': float(row['final_exam'])
        }
        
        documents.append({"content": doc_text.strip(), "metadata": metadata})
    
    return documents

def setup_rag(data_path):
    """Initialize the RAG system"""
    try:
        # Load environment variables for API key
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        # Add caching to save tokens
        langchain.cache = InMemoryCache()
        
        # Initialize LLM with optimized settings
        llm = ChatOpenAI(
            temperature=0.5,  # Lower temperature for more focused responses
            model="gpt-3.5-turbo",
            cache=True  # Enable caching
        )
            
        # Configure OpenAI settings
        os.environ["OPENAI_API_KEY"] = api_key
            
        # Load and process data
        df = load_data(data_path)
        if df is None:
            raise ValueError("Failed to load data")
            
        # Create document collection
        documents = create_student_documents(df)
        
        # Set up text splitter with optimized settings
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,      # Smaller chunks for more focused retrieval
            chunk_overlap=50,    # Reduced overlap
            separators=["\n\n", "\n", ". ", " ", ""],  # More granular splitting
            length_function=len
        )
        
        # Split documents
        texts = []
        metadatas = []
        for doc in documents:
            chunks = text_splitter.split_text(doc["content"])
            texts.extend(chunks)
            metadatas.extend([doc["metadata"]] * len(chunks))
        
        # Initialize embeddings and vector store
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas
        )
        
        # Initialize LLM
        llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        
        return vectorstore, llm, df
        
    except Exception as e:
        print(f"Error setting up RAG: {str(e)}")
        return None, None, None

def validate_data_sample(docs, filter_metadata):
    """Validate the data sample and return information about limitations"""
    try:
        # Count unique student IDs in retrieved documents
        student_ids = set()
        for doc in docs:
            if 'student_id' in doc.metadata:
                student_ids.add(doc.metadata['student_id'])
        
        sample_size = len(student_ids)
        
        # Create warning message if sample size is small
        if sample_size < 3:
            return f"Note: Analysis is based on a small sample of {sample_size} student(s). Interpret results with caution."
        elif sample_size < 5:
            return f"Note: Analysis is based on {sample_size} students."
        else:
            return ""
            
    except Exception as e:
        return "Warning: Unable to determine sample size."
    
def query_rag(vectorstore, llm, question, filter_metadata=None, memory=None):
    """Enhanced query function with error handling and data validation"""
    try:
        # Retrieve documents
        docs = vectorstore.similarity_search(
            question,
            k=2,
            filter=filter_metadata
        )
        
        # Check if we found any relevant documents
        if not docs:
            return "No relevant data found for your question. Try adjusting your question or using a different filter."
            
        # Validate sample size and get any warnings
        sample_size_warning = validate_data_sample(docs, filter_metadata)
        
        # Combine context
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Create enhanced prompt
        prompt = PromptTemplate(
            template="""You are analyzing psychology student data. Provide a detailed analysis based only on the provided context.
            
            Context: {context}
            Question: {question}
            Data Limitations: {sample_size_warning}
            
            Analysis:""",
            input_variables=["context", "question", "sample_size_warning"]
        )
        
        # Generate response
        chain = prompt | llm
        response = chain.invoke({
            "context": context,
            "question": question,
            "sample_size_warning": sample_size_warning
        })
        
        return response.content
        
    except Exception as e:
        return f"Error processing your question: {str(e)}"
    
def is_comparative_question(question):
    """Detect if a question is asking for comparison between groups"""
    comparative_phrases = [
        'compare', 'versus', 'vs', 'difference', 'better', 'worse',
        'than', 'between', 'higher', 'lower', 'more', 'less'
    ]
    demographic_terms = ['male', 'female', 'gender', 'international', 'first-gen']
    
    question_lower = question.lower()
    has_comparative = any(phrase in question_lower for phrase in comparative_phrases)
    has_demographic = any(term in question_lower for term in demographic_terms)
    
    return has_comparative and has_demographic

def query_rag(vectorstore, llm, question, filter_metadata=None):
    """Enhanced query function with comparative analysis support"""
    try:
        # Check if this is a comparative question
        if is_comparative_question(question):
            print("\nDebug - Detected comparative question, retrieving data for all groups...")
            # For comparative questions, ignore the filter and get data for all groups
            docs = vectorstore.similarity_search(
                question,
                k=6  # Increased to get more documents for comparison
            )
        else:
            # Normal filtered query
            print(f"\nDebug - Applied filter: {filter_metadata}")
            docs = vectorstore.similarity_search(
                question,
                k=3,
                filter=filter_metadata
            )
        
        print(f"Debug - Number of documents found: {len(docs)}")
        
        if not docs:
            return "No relevant information found. Try rephrasing your question."
            
        # Enhanced prompt for comparative questions
        if is_comparative_question(question):
            prompt = PromptTemplate(
                template="""Analyze the psychology student data and provide a detailed comparison.
                Focus on:
                1. Clear statistical comparison between groups
                2. Notable patterns or differences
                3. Important context or limitations of the comparison
                
                Context: {context}
                Question: {question}
                
                Comparative Analysis:""",
                input_variables=["context", "question"]
            )
        else:
            # Regular prompt for non-comparative questions
            prompt = PromptTemplate(
                template="""Analyze the psychology student data based on this context. 
                {filter_context}Provide specific insights with evidence.
                
                Context: {context}
                Question: {question}
                
                Analysis:""",
                input_variables=["context", "question", "filter_context"]
            )
        
        # Generate response
        context = "\n\n".join([doc.page_content for doc in docs])
        
        if is_comparative_question(question):
            chain = prompt | llm
            response = chain.invoke({
                "context": context,
                "question": question
            })
        else:
            filter_context = filter_metadata.get('gender', '') if filter_metadata else ''
            chain = prompt | llm
            response = chain.invoke({
                "context": context,
                "question": question,
                "filter_context": filter_context
            })
        
        return response.content
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return "An error occurred. Please try again."
    
def validate_data_advanced(docs, filter_metadata):
    """Enhanced data validation with more sophisticated checks"""
    validation_results = {
        "warnings": [],
        "sample_size": 0,
        "data_quality": "high"
    }
    
    try:
        # Count unique students
        student_ids = set()
        grades_present = True
        feedback_present = True
        
        for doc in docs:
            if 'student_id' in doc.metadata:
                student_ids.add(doc.metadata['student_id'])
            
            # Check for missing crucial data
            if 'final_exam' not in doc.metadata:
                grades_present = False
            if 'course_review' not in str(doc.page_content):
                feedback_present = False
        
        # Add relevant warnings
        if len(student_ids) < 3:
            validation_results["warnings"].append(
                f"Small sample size ({len(student_ids)} students)"
            )
            validation_results["data_quality"] = "limited"
            
        if not grades_present:
            validation_results["warnings"].append(
                "Grade data not available for some students"
            )
            
        if not feedback_present:
            validation_results["warnings"].append(
                "Qualitative feedback missing for some students"
            )
            
        validation_results["sample_size"] = len(student_ids)
        
        return validation_results
        
    except Exception as e:
        validation_results["warnings"].append(f"Validation error: {str(e)}")
        validation_results["data_quality"] = "unknown"
        return validation_results
    
def test_rag_features():
    """Test new RAG features with various scenarios"""
    test_cases = [
        {
            "name": "Memory Integration Test",
            "questions": [
                "How do international students perform in exams?",
                "What study habits do they mention?",
                "Do these habits seem effective based on their grades?"
            ],
            "filter": {"international_student": "Yes"}
        },
        {
            "name": "Data Validation Test",
            "questions": [
                "What's the average final exam score?",
                "How does this compare to midterm performance?",
            ],
            "filter": None
        },
        {
            "name": "Small Sample Test",
            "questions": [
                "How do students with perfect attendance perform?",
            ],
            "filter": {"attendance_rate": 100}
        }
    ]
    
    print("\nRunning RAG Feature Tests...")
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    for test in test_cases:
        print(f"\nTesting: {test['name']}")
        print("-" * 50)
        
        for question in test["questions"]:
            print(f"\nQuestion: {question}")
            response = query_rag_with_memory(
                vectorstore, 
                llm, 
                question, 
                test["filter"],
                memory if "Memory" in test["name"] else None
            )
            print(f"Response: {response}")
            
        input("\nPress Enter to continue to next test...")

def enhanced_interactive_mode(vectorstore, llm):
    """Enhanced interactive mode with all new features"""
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    print("\nEnhanced RAG System")
    print("Commands:")
    print("- 'examples': Show example questions")
    print("- 'test': Run feature tests")
    print("- 'exit': Quit")
    
    while True:
        command = input("\nEnter command or question: ").strip().lower()
        
        if command == 'exit':
            break
        elif command == 'examples':
            show_example_questions()
        elif command == 'test':
            test_rag_features()
        else:
            # Regular question processing with memory
            filter_choice = input("Choose filter (1: International, 2: First-Gen, 3: None): ")
            filter_metadata = get_filter_metadata(filter_choice)
            
            response = query_rag_with_memory(
                vectorstore,
                llm,
                command,
                filter_metadata,
                memory
            )
            print("\nResponse:", response)

def get_filter_metadata():
    """Get and validate filter choice from user with enhanced options including gender"""
    filter_options = {
        '1': {
            'name': 'International Students',
            'metadata': {'international_student': 'Yes'}
        },
        '2': {
            'name': 'First-Generation Students',
            'metadata': {'first_gen_student': 'Yes'}
        },
        '3': {
            'name': 'Filter by Gender',
            'type': 'submenu',
            'options': {
                'a': {'name': 'Female Students', 'metadata': {'gender': 'Female'}},
                'b': {'name': 'Male Students', 'metadata': {'gender': 'Male'}},
                'c': {'name': 'Non-binary Students', 'metadata': {'gender': 'Non-binary'}}
            }
        },
        '4': {
            'name': 'All Students',
            'metadata': None
        }
    }
    
    while True:
        print("\nFilter Options:")
        for key, option in filter_options.items():
            print(f"{key}: {option['name']}")
        
        filter_choice = input("\nChoose filter (1-4): ").strip()
        
        if filter_choice not in filter_options:
            print("Invalid choice. Using no filter.")
            return None
            
        selected_option = filter_options[filter_choice]
        
        # Handle gender submenu
        if filter_choice == '3':
            print("\nGender Options:")
            for sub_key, sub_option in selected_option['options'].items():
                print(f"{sub_key}: {sub_option['name']}")
                
            gender_choice = input("\nChoose gender filter (a-c): ").strip().lower()
            
            if gender_choice not in selected_option['options']:
                print("Invalid gender choice. Using no filter.")
                return None
                
            return selected_option['options'][gender_choice]['metadata']
        
        return selected_option['metadata']
  
def test_rag_system(vectorstore, llm):
    """Test the RAG system with focused question types"""
    
    # Test questions focused on demographics and performance
    test_questions = [
        {
            "category": "Demographic Analysis",
            "question": "What patterns do you notice in how international students describe their learning experience?",
            "filter": {"international_student": "Yes"}
        },
        {
            "category": "Demographic Analysis",
            "question": "How do first-generation students describe their course experience?",
            "filter": {"first_gen_student": "Yes"}
        },
        {
            "category": "Performance Correlation",
            "question": "What's the relationship between study hours and final exam scores?",
            "filter": None
        },
        {
            "category": "Performance Correlation",
            "question": "How does attendance rate correlate with exam performance?",
            "filter": None
        }
    ]
    
    print("\nTesting RAG System...")
    for test in test_questions:
        print(f"\nCategory: {test['category']}")
        print(f"Question: {test['question']}")
        
        response = query_rag(vectorstore, llm, test['question'], test['filter'])
        
        if response:
            print(f"\nResponse: {response}\n")
            print("-" * 50)
        else:
            print("Failed to get response")

def create_student_documents(df):
    """Create text documents for each student with proper metadata"""
    documents = []
    
    for _, row in df.iterrows():
        # Create a focused text document
        doc_text = f"""
        Student Demographics:
        - Gender: {row['gender']}
        - First Generation Student: {row['first_gen_student']}
        - International Student: {row['international_student']}

        Academic Performance:
        - Midterm Grade: {row['midterm_grade']}
        - Final Exam: {row['final_exam']}
        - Study Hours per Week: {row['study_hours_per_week']}
        - Attendance Rate: {row['attendance_rate']}

        Student Feedback:
        {row['course_review']}

        Learning Assessment:
        {row['learning_outcomes_assessment']}
        """
        
        # Enhanced metadata to include all filter fields
        metadata = {
            'student_id': row['student_id'],
            'gender': row['gender'],  # Explicitly include gender
            'international_student': row['international_student'],
            'first_gen_student': row['first_gen_student'],
            'study_hours_per_week': float(row['study_hours_per_week']),
            'final_exam': float(row['final_exam'])
        }
        
        documents.append({"content": doc_text.strip(), "metadata": metadata})
    
    return documents


def interactive_mode(vectorstore, llm):
    """Enhanced interactive mode with comparative question handling"""
    print("\nPsychology Course Analysis System")
    print("----------------------------------")
    print("Commands:")
    print("- 'examples': Show example questions")
    print("- 'help': Show this menu")
    print("- 'exit': Quit the program")
    
    while True:
        try:
            user_input = input("\nEnter your question (or command): ").strip()
            
            if user_input.lower() == 'exit':
                print("Exiting program...")
                return False
            elif user_input.lower() == 'examples':
                show_example_questions()
                continue
            elif user_input.lower() == 'help':
                print("\nCommands:")
                print("- 'examples': Show example questions")
                print("- 'help': Show this menu")
                print("- 'exit': Quit the program")
                continue
                
            if len(user_input) < 3:
                print("Please enter a longer question.")
                continue
            
            # Check if this is a comparative question
            if is_comparative_question(user_input):
                print("\nNote: Detected comparative question - analyzing all relevant groups...")
                filter_metadata = None  # Don't apply filters for comparative questions
            else:
                filter_metadata = get_filter_metadata()
            
            print("\nProcessing your question...")
            response = query_rag(vectorstore, llm, user_input, filter_metadata)
            
            print("\nAnalysis:")
            print("---------")
            print(response)
            print("\nYou can ask another question or type 'exit' to quit.")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            continue
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again or type 'exit' to quit.")

def show_example_questions():
    """Display example questions that work well with the dataset"""
    examples = {
        "Performance Analysis": [
            "What's the typical range of midterm scores for international students?",
            "How do first-generation students perform in final exams?",
            "Is there a relationship between study hours and exam performance?"
        ],
        "Engagement Patterns": [
            "What attendance patterns do we see among high-performing students?",
            "How many hours do students with above-average grades typically study?",
            "What's the relationship between attendance and final exam scores?"
        ],
        "Student Feedback": [
            "What common challenges do international students mention?",
            "What aspects of the course do first-generation students find most helpful?",
            "How do students describe their learning experience in this course?"
        ]
    }
    
    print("\nExample Questions You Can Ask:")
    for category, questions in examples.items():
        print(f"\n{category}:")
        for q in questions:
            print(f"- {q}")

def run_psychology_specific_tests(vectorstore, llm):
    """Run tests specifically designed for psychology student data"""
    print("\nRunning Psychology Dataset Tests...")
    
    test_scenarios = [
        {
            "category": "Performance Analysis",
            "tests": [
                {
                    "description": "Basic Grade Distribution",
                    "question": "What's the distribution of final exam scores?",
                    "expected_elements": ["average", "range", "sample size"]
                },
                {
                    "description": "Study Hours Impact",
                    "question": "How do study hours correlate with exam performance?",
                    "expected_elements": ["correlation", "patterns", "examples"]
                }
            ]
        },
        {
            "category": "Student Demographics",
            "tests": [
                {
                    "description": "International Student Experience",
                    "question": "What common themes appear in international student feedback?",
                    "filter": {"international_student": "Yes"},
                    "expected_elements": ["challenges", "successes", "recommendations"]
                }
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\nTesting {scenario['category']}:")
        for test in scenario["tests"]:
            print(f"\nRunning: {test['description']}")
            response = query_rag_with_memory(
                vectorstore,
                llm,
                test["question"],
                test.get("filter"),
                None  # No memory for individual tests
            )
            
            # Validate response content
            validation = validate_response_content(response, test["expected_elements"])
            print(f"Response includes expected elements: {validation}")

def interpret_validation_results(validation_results):
    """Interpret and explain validation results"""
    interpretation = {
        "reliability_score": 0,
        "recommendations": [],
        "data_quality_explanation": ""
    }
    
    # Calculate reliability score (0-100)
    base_score = 100
    if validation_results["sample_size"] < 3:
        base_score -= 40
    elif validation_results["sample_size"] < 5:
        base_score -= 20
        
    for warning in validation_results["warnings"]:
        if "missing" in warning.lower():
            base_score -= 15
        elif "small sample" in warning.lower():
            base_score -= 10
            
    interpretation["reliability_score"] = max(base_score, 0)
    
    # Generate recommendations
    if validation_results["sample_size"] < 3:
        interpretation["recommendations"].append(
            "Consider broadening filter criteria to include more students"
        )
    
    if "Grade data not available" in str(validation_results["warnings"]):
        interpretation["recommendations"].append(
            "For grade analysis, focus on students with complete grade records"
        )
        
    # Create explanation
    quality_levels = {
        "high": "Results are highly reliable with good sample size and complete data",
        "limited": "Results should be interpreted cautiously due to data limitations",
        "unknown": "Unable to fully verify data quality"
    }
    
    interpretation["data_quality_explanation"] = quality_levels.get(
        validation_results["data_quality"],
        "Data quality assessment inconclusive"
    )
    
    return interpretation

class EnhancedConversationMemory:
    def __init__(self, max_tokens=1000):
        self.conversations = []
        self.max_tokens = max_tokens
        self.topic_tracking = {}
        
    def add_interaction(self, question, response, metadata=None):
        """Add an interaction with topic tracking"""
        interaction = {
            "question": question,
            "response": response,
            "timestamp": pd.Timestamp.now(),
            "metadata": metadata or {}
        }
        
        # Track topics
        topics = self.extract_topics(question)
        for topic in topics:
            if topic not in self.topic_tracking:
                self.topic_tracking[topic] = 0
            self.topic_tracking[topic] += 1
        
        self.conversations.append(interaction)
        self._prune_old_conversations()
        
    def get_relevant_history(self, current_question):
        """Get relevant conversation history"""
        topics = self.extract_topics(current_question)
        relevant_interactions = []
        
        for interaction in reversed(self.conversations):
            if any(topic in interaction["question"].lower() for topic in topics):
                relevant_interactions.append(interaction)
                
        return relevant_interactions[-3:]  # Return last 3 relevant interactions
        
    def extract_topics(self, text):
        """Extract key topics from text"""
        key_topics = [
            "international", "first-gen", "grades", "study",
            "exam", "attendance", "performance", "feedback"
        ]
        return [topic for topic in key_topics if topic in text.lower()]
        
    def _prune_old_conversations(self):
        """Remove old conversations to stay within token limit"""
        while len(str(self.conversations)) > self.max_tokens:
            self.conversations.pop(0)

def enhanced_interactive_mode_with_validation(vectorstore, llm):
    """Interactive mode with enhanced features"""
    memory = EnhancedConversationMemory()
    
    print("\nEnhanced Psychology RAG System")
    print("Available commands:")
    print("- 'analyze': Run data quality analysis")
    print("- 'topics': Show frequently discussed topics")
    print("- 'test': Run specific tests")
    print("- 'exit': Quit")
    
    while True:
        command = input("\nEnter command or question: ").strip().lower()
        
        if command == 'exit':
            break
        elif command == 'analyze':
            # Run data quality analysis
            docs = vectorstore.similarity_search("", k=5)
            validation_results = validate_data_advanced(docs, None)
            interpretation = interpret_validation_results(validation_results)
            print("\nData Quality Analysis:")
            print(f"Reliability Score: {interpretation['reliability_score']}/100")
            print(f"Quality: {interpretation['data_quality_explanation']}")
            for rec in interpretation['recommendations']:
                print(f"- {rec}")
        elif command == 'topics':
            # Show topic statistics
            print("\nFrequently Discussed Topics:")
            for topic, count in sorted(
                memory.topic_tracking.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"- {topic}: {count} times")
        elif command == 'test':
            run_psychology_specific_tests(vectorstore, llm)
        else:
            # Process regular question
            filter_metadata = get_filter_choice()
            response = query_rag_with_memory(
                vectorstore,
                llm,
                command,
                filter_metadata,
                memory
            )
            print("\nResponse:", response)

def main():
    """Main function with proper exit handling"""
    print("Initializing RAG system...")
    
    try:
        data_path = '/Users/dondeerie/projects/Test-DD/data/'
        vectorstore, llm, df = setup_rag(data_path)
        
        if not all([vectorstore, llm, df is not None]):
            print("Error: Failed to initialize one or more components")
            return
            
        while True:
            print("\nChoose mode:")
            print("1. Interactive mode")
            print("2. Run test questions")
            print("3. Exit")
            
            try:
                choice = input("Enter your choice (1-3): ").strip()
                
                if choice == '1':
                    continue_program = interactive_mode(vectorstore, llm)
                    if not continue_program:
                        break
                elif choice == '2':
                    test_rag_system(vectorstore, llm)
                elif choice == '3':
                    print("Exiting program...")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                break  # Exit on Ctrl+C
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                print("Please try again.")
                
    except Exception as e:
        print(f"Critical error: {str(e)}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()