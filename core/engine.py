import json
from pathlib import Path
import db

BASE_DIR = Path(__file__).parent.parent

def load_lesson(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def run_flashcards(lesson):
    print(f"\n=== Lesson: {lesson['title']} ===")
    flashcards = lesson.get("flashcards", [])
    
    for i, card in enumerate(flashcards, 1):
        print(f"\nQuestion {i}: {card['question']}")
        input(">>> Press Enter to reveal the answer...")
        print(f"Answer: {card['answer']}")

def run_quiz(lesson):
    quiz = lesson.get("code_quiz")
    if not quiz:
        return 0
        
    print("\n=== Code Quiz ===")
    print(quiz["snippet"])
    print("\nOptions:")
    
    for i, option in enumerate(quiz["options"], 1):
        print(f"{i}. {option}")
        
    choice = input("\nYour choice (1-4): ")
    
    try:
        choice_index = int(choice) - 1
        selected_option = quiz["options"][choice_index]
        
        if selected_option == quiz["correct_answer"]:
            print("Correct!")
            return 1
        else:
            print(f"Wrong. The correct answer was: {quiz['correct_answer']}")
            return 0
    except (ValueError, IndexError):
        print("Invalid input. Scored 0.")
        return 0

if __name__ == "__main__":
    db.init_db()
    
    lesson_path = BASE_DIR / "data" / "modules" / "01_bases.json"
    lesson = load_lesson(lesson_path)
    
    run_flashcards(lesson)
    score = run_quiz(lesson)
    
    db.save_progress(lesson["module_id"], score)
    print("\nProgress saved successfully.")