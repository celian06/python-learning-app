import json
from pathlib import Path
import db
import validator

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
    
def run_project(lesson):
    project = lesson.get("project")
    if not project:
        return 0
        
    print(f"\n=== Projet Final : {project['title']} ===")
    print(project["description"])
    
    # Simulation : en attendant Streamlit, on va charger le code depuis un fichier temporaire
    # plutôt que de demander de taper 10 lignes dans le terminal.
    print("\n[Simulation] : Le moteur va lire le fichier 'user_workspace.py'...")
    
    try:
        with open("user_workspace.py", "r", encoding="utf-8") as f:
            user_code = f.read()
            
        success = validator.evaluate_code(
            user_code, 
            project["target_function"], 
            project["test_cases"]
        )
        return 1 if success else 0
    except FileNotFoundError:
        print("Erreur : Crée un fichier 'user_workspace.py' à la racine et écris ta fonction dedans pour tester.")
        return 0

if __name__ == "__main__":
    db.init_db()
    
    lesson_path = BASE_DIR / "data" / "modules" / "01_bases.json"
    lesson = load_lesson(lesson_path)
    
    run_flashcards(lesson)
    quiz_score = run_quiz(lesson)
    project_score = run_project(lesson)
    
    total_score = quiz_score + project_score
    db.save_progress(lesson["module_id"], total_score)
    print(f"\nProgression sauvegardée ! Score final : {total_score}")