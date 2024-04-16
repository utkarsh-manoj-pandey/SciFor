import tkinter as tk
from tkinter import messagebox
import random

# Define quiz questions for different topics and difficulty levels
quiz_questions = {
    'General Knowledge': {
        'Easy': [
            {'question': 'What is the capital of France?', 'options': ['Paris', 'London', 'Berlin', 'Rome'], 'answer': 'Paris'},
            {'question': 'What is 2 + 2?', 'options': ['3', '4', '5', '6'], 'answer': '4'},
            {'question': 'Which planet is known as the Red Planet?', 'options': ['Mars', 'Venus', 'Jupiter', 'Saturn'], 'answer': 'Mars'}
        ],
        'Medium': [
            {'question': 'Who painted the Mona Lisa?', 'options': ['Vincent van Gogh', 'Pablo Picasso', 'Leonardo da Vinci', 'Michelangelo'], 'answer': 'Leonardo da Vinci'},
            {'question': 'What is the chemical symbol for water?', 'options': ['H2O', 'CO2', 'NaCl', 'O2'], 'answer': 'H2O'},
            {'question': 'What is the largest mammal in the world?', 'options': ['Elephant', 'Giraffe', 'Blue whale', 'Hippopotamus'], 'answer': 'Blue whale'}
        ],
        'Hard': [
            {'question': 'In which year did World War I begin?', 'options': ['1912', '1914', '1916', '1918'], 'answer': '1914'},
            {'question': 'What is the smallest country in the world?', 'options': ['Monaco', 'Vatican City', 'Maldives', 'Singapore'], 'answer': 'Vatican City'},
            {'question': 'Who discovered penicillin?', 'options': ['Alexander Fleming', 'Marie Curie', 'Louis Pasteur', 'Albert Einstein'], 'answer': 'Alexander Fleming'}
        ]
    },
    'Sports': {
        'Easy': [
            {'question': 'Which sport is played with a shuttlecock?', 'options': ['Tennis', 'Badminton', 'Table Tennis', 'Squash'], 'answer': 'Badminton'},
            {'question': 'How many players are there in a basketball team?', 'options': ['5', '6', '7', '8'], 'answer': '5'},
            {'question': 'Who won the FIFA World Cup in 2018?', 'options': ['Germany', 'Brazil', 'Spain', 'France'], 'answer': 'France'}
        ],
        'Medium': [
            {'question': 'Which country invented the modern Olympic Games?', 'options': ['Greece', 'Italy', 'United States', 'France'], 'answer': 'Greece'},
            {'question': 'How many players are there in a cricket team?', 'options': ['9', '10', '11', '12'], 'answer': '11'},
            {'question': 'Who has won the most Wimbledon titles in tennis (male)?', 'options': ['Roger Federer', 'Rafael Nadal', 'Novak Djokovic', 'Pete Sampras'], 'answer': 'Roger Federer'}
        ],
        'Hard': [
            {'question': 'Which country won the most gold medals in the 2016 Summer Olympics?', 'options': ['United States', 'China', 'Russia', 'Great Britain'], 'answer': 'United States'},
            {'question': 'Which city hosted the 2016 Summer Olympics?', 'options': ['Rio de Janeiro', 'London', 'Tokyo', 'Beijing'], 'answer': 'Rio de Janeiro'},
            {'question': 'Who holds the record for the fastest 100m sprint?', 'options': ['Usain Bolt', 'Carl Lewis', 'Jesse Owens', 'Yohan Blake'], 'answer': 'Usain Bolt'}
        ]
    }
}

# Define points required to unlock rewards for each difficulty level
points_to_unlock = {
    'Easy': 5,
    'Medium': 10,
    'Hard': 15
}

# Define rewards for each difficulty level
rewards = {
    'Easy': 'Congratulations! You unlocked a bronze badge.',
    'Medium': 'Congratulations! You unlocked a silver badge.',
    'Hard': 'Congratulations! You unlocked a gold badge.'
}

# Function to play the quiz
def play_quiz(topic, difficulty):
    questions = quiz_questions[topic][difficulty]
    random.shuffle(questions)
    
    def check_answer(answer):
        nonlocal points
        if answer.lower() == questions[q_index]['answer'].lower():
            points += 1
            messagebox.showinfo("Correct", "Correct answer!")
        else:
            messagebox.showerror("Incorrect", "Incorrect answer!")
        next_question()
    
    def next_question():
        nonlocal q_index
        if q_index < len(questions) - 1:
            q_index += 1
            question_label.config(text=questions[q_index]['question'])
            for i in range(len(option_buttons)):
                option_buttons[i].config(text=questions[q_index]['options'][i])
        else:
            messagebox.showinfo("Quiz Completed", f"Quiz completed! You scored {points} points.")
            window.destroy()
    
    window = tk.Tk()
    window.title("Quiz Game")
    window.geometry("500x300")
    window.configure(bg="#f0f0f0")
    
    q_index = 0
    points = 0
    
    heading_label = tk.Label(window, text=f"{topic} Quiz - {difficulty}", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
    heading_label.pack(pady=10)
    
    question_label = tk.Label(window, text=questions[q_index]['question'], font=("Helvetica", 14), wraplength=400, bg="#f0f0f0")
    question_label.pack(pady=20)
    
    option_buttons = []
    for option in questions[q_index]['options']:
        button = tk.Button(window, text=option, font=("Helvetica", 12), width=20, bg="#d3d3d3", fg="#000000", command=lambda option=option: check_answer(option))
        button.pack(pady=5)
        option_buttons.append(button)
    
    window.mainloop()

# Main function
def main():
    window = tk.Tk()
    window.title("Quiz Game")
    window.geometry("400x300")
    window.configure(bg="#f0f0f0")
    
    welcome_label = tk.Label(window, text="Welcome to the Quiz Game!", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    welcome_label.pack(pady=20)
    
    def start_quiz(topic, difficulty):
        window.destroy()
        play_quiz(topic, difficulty)
    
    def choose_difficulty(selected_topic):
        difficulty_window = tk.Toplevel(window)
        difficulty_window.title("Choose Difficulty")
        difficulty_window.geometry("300x200")
        difficulty_window.configure(bg="#f0f0f0")
        
        topic_label = tk.Label(difficulty_window, text=f"Choose Difficulty for {selected_topic}", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        topic_label.pack(pady=10)
        
        for difficulty in quiz_questions[selected_topic]:
            button = tk.Button(difficulty_window, text=difficulty, font=("Helvetica", 12), width=15, bg="#d3d3d3", fg="#000000", command=lambda difficulty=difficulty: start_quiz(selected_topic, difficulty))
            button.pack(pady=5)
    
    for idx, topic in enumerate(quiz_questions):
        button = tk.Button(window, text=topic, font=("Helvetica", 12), width=20, bg="#d3d3d3", fg="#000000", command=lambda topic=topic: choose_difficulty(topic))
        button.pack(pady=5)
    
    window.mainloop()

if __name__ == "__main__":
    main()