import streamlit as st
import random
import time
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Python MCQ Quiz App",
    page_icon="✅",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .question-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .option-button {
        margin: 0.5rem 0;
    }
    .result-container {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .correct {
        color: #28a745;
        font-weight: bold;
    }
    .incorrect {
        color: #dc3545;
        font-weight: bold;
    }
    .timer {
        font-size: 1.2rem;
        font-weight: bold;
        color: #6c757d;
        text-align: center;
        margin-bottom: 1rem;
    }
    .time-warning {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Sample MCQ data
mcq_data = [
    {
        "question": "What is the output of print(2 ** 3)?",
        "options": ["6", "8", "9", "5"],
        "correct_answer": "8",
        "explanation": "The ** operator in Python represents exponentiation. 2 ** 3 = 2³ = 8"
    },
    {
        "question": "Which of the following is NOT a Python data type?",
        "options": ["List", "Dictionary", "Tuple", "Array"],
        "correct_answer": "Array",
        "explanation": "Array is not a built-in data type in Python. Python has lists instead, though NumPy provides array functionality."
    },
    {
        "question": "What does the 'len()' function do in Python?",
        "options": ["Returns the length of an object", "Returns the largest item in an iterable", "Rounds a number to the nearest integer", "Returns the smallest item in an iterable"],
        "correct_answer": "Returns the length of an object",
        "explanation": "The len() function returns the number of items in an object like a string, list, tuple, etc."
    },
    {
        "question": "Which method is used to add an element to the end of a list?",
        "options": ["append()", "extend()", "insert()", "add()"],
        "correct_answer": "append()",
        "explanation": "The append() method adds a single element to the end of a list."
    },
    {
        "question": "What is the correct way to create a function in Python?",
        "options": ["function myFunc():", "def myFunc():", "create myFunc():", "func myFunc():"],
        "correct_answer": "def myFunc():",
        "explanation": "In Python, functions are defined using the 'def' keyword followed by the function name and parentheses."
    }
]

# Time settings
QUESTION_TIME_LIMIT = 30  # seconds per question

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = random.sample(mcq_data, len(mcq_data))
    
# Timing related session state
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = time.time()
if 'question_start_time' not in st.session_state:
    st.session_state.question_start_time = time.time()
if 'question_times' not in st.session_state:
    st.session_state.question_times = {}
if 'total_quiz_time' not in st.session_state:
    st.session_state.total_quiz_time = 0

# Functions
def check_answer(selected_option, question_idx):
    # Record time taken for this question
    question_end_time = time.time()
    time_taken = question_end_time - st.session_state.question_start_time
    st.session_state.question_times[question_idx] = time_taken
    
    current_question = st.session_state.shuffled_questions[question_idx]
    st.session_state.user_answers[question_idx] = selected_option
    
    if selected_option == current_question["correct_answer"]:
        st.session_state.score += 1
        return True
    return False

def next_question():
    st.session_state.current_question += 1
    st.session_state.question_start_time = time.time()
    
    if st.session_state.current_question >= len(st.session_state.shuffled_questions):
        st.session_state.quiz_completed = True
        st.session_state.total_quiz_time = time.time() - st.session_state.quiz_start_time

def restart_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_completed = False
    st.session_state.user_answers = {}
    st.session_state.shuffled_questions = random.sample(mcq_data, len(mcq_data))
    st.session_state.quiz_start_time = time.time()
    st.session_state.question_start_time = time.time()
    st.session_state.question_times = {}
    st.session_state.total_quiz_time = 0

def format_time(seconds):
    """Format seconds into minutes and seconds"""
    return str(timedelta(seconds=int(seconds))).split('.')[0]

# App header
st.title("Python MCQ Quiz App")
st.markdown("Test your Python knowledge with these multiple-choice questions!")

# Display quiz
if not st.session_state.quiz_completed:
    # Progress bar
    progress = (st.session_state.current_question) / len(st.session_state.shuffled_questions)
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question + 1} of {len(st.session_state.shuffled_questions)}")
    
    # Timer display
    current_time = time.time()
    total_elapsed = current_time - st.session_state.quiz_start_time
    question_elapsed = current_time - st.session_state.question_start_time
    time_remaining = max(0, QUESTION_TIME_LIMIT - question_elapsed)
    
    # Display timers
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="timer">
            Total Time: {format_time(total_elapsed)}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        time_class = "timer time-warning" if time_remaining < 10 else "timer"
        st.markdown(f"""
        <div class="{time_class}">
            Time Remaining: {format_time(time_remaining)}
        </div>
        """, unsafe_allow_html=True)
    
    # Auto-submit if time runs out
    if time_remaining <= 0:
        st.warning("Time's up! Moving to the next question.")
        st.session_state.user_answers[st.session_state.current_question] = "Time expired"
        st.session_state.question_times[st.session_state.current_question] = QUESTION_TIME_LIMIT
        next_question()
        st.experimental_rerun()
    
    # Current question
    current_q = st.session_state.shuffled_questions[st.session_state.current_question]
    
    # Question container
    st.markdown(f"""
    <div class="question-container">
        <h3>{current_q["question"]}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Options
    option_selected = False
    for option in current_q["options"]:
        if st.button(option, key=f"option_{option}", use_container_width=True):
            is_correct = check_answer(option, st.session_state.current_question)
            option_selected = True
            
            if is_correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect! The correct answer is: {current_q['correct_answer']}")
            
            st.info(f"Explanation: {current_q['explanation']}")
            st.button("Next Question", on_click=next_question, use_container_width=True)
            
    # Skip question button
    if not option_selected:
        if st.button("Skip Question", use_container_width=True):
            st.session_state.user_answers[st.session_state.current_question] = "Skipped"
            st.session_state.question_times[st.session_state.current_question] = time.time() - st.session_state.question_start_time
            next_question()
            st.experimental_rerun()
else:
    # Quiz completed - show results
    st.markdown(f"""
    <div class="result-container">
        <h2>Quiz Completed!</h2>
        <h3>Your Score: {st.session_state.score}/{len(st.session_state.shuffled_questions)}</h3>
        <p>Percentage: {(st.session_state.score/len(st.session_state.shuffled_questions))*100:.2f}%</p>
        <p>Total Time: {format_time(st.session_state.total_quiz_time)}</p>
        <p>Average Time per Question: {format_time(st.session_state.total_quiz_time/len(st.session_state.shuffled_questions))}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Review answers
    st.markdown("### Review Your Answers")
    for i, question in enumerate(st.session_state.shuffled_questions):
        user_answer = st.session_state.user_answers.get(i, "Not answered")
        is_correct = user_answer == question["correct_answer"]
        time_taken = st.session_state.question_times.get(i, 0)
        
        st.markdown(f"""
        <div class="question-container">
            <p><strong>Question {i+1}:</strong> {question["question"]}</p>
            <p><strong>Your answer:</strong> <span class="{'correct' if is_correct else 'incorrect'}">{user_answer}</span></p>
            <p><strong>Correct answer:</strong> {question["correct_answer"]}</p>
            <p><strong>Time taken:</strong> {format_time(time_taken)}</p>
            <p><strong>Explanation:</strong> {question["explanation"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Restart button
    if st.button("Restart Quiz", use_container_width=True):
        restart_quiz()
        st.experimental_rerun()