import json

def load_lesson(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    # Test rapide en local
    lesson = load_lesson("data/modules/00_test.json")
    print(f"Titre de la leçon chargée : {lesson['title']}")
    print(f"Première question : {lesson['flashcards'][0]['question']}")