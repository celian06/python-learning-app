import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def load_lesson(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def run_flashcards(lesson):
    print(f"\n=== Leçon : {lesson['title']} ===")
    flashcards = lesson.get("flashcards", [])
    
    if not flashcards:
        print("Aucune flashcard trouvée pour cette leçon.")
        return

    for i, card in enumerate(flashcards, 1):
        print(f"\nQuestion {i} : {card['question']}")
        input(">>> Appuie sur Entrée pour révéler la réponse...")
        print(f"Réponse : {card['answer']}")

if __name__ == "__main__":
    lesson_path = BASE_DIR / "data" / "modules" / "00_test.json"
    lesson = load_lesson(lesson_path)
    
    run_flashcards(lesson)