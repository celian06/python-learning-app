import sys
import json
from pathlib import Path
from nicegui import ui

# Configuration des chemins
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))
from core import validator

# 1. Fonction pour charger tous les JSON du dossier data/modules
def load_lessons():
    lessons = []
    modules_dir = BASE_DIR / "data" / "modules"
    for file in sorted(modules_dir.glob("*.json")):
        with open(file, "r", encoding="utf-8") as f:
            lessons.append(json.load(f))
    return lessons

lessons = load_lessons()

# 2. Construction de la page Web
@ui.page('/')
def main_page():
    # --- EN-TÊTE ---
    with ui.header().classes('bg-blue-900 justify-between items-center p-4'):
        ui.label('Python Learning App').classes('text-h5 font-bold')
        ui.button(icon='menu', on_click=lambda: sidebar.toggle()).props('flat color=white')

    # --- CONTENEUR PRINCIPAL ---
    main_content = ui.column().classes('w-full max-w-4xl mx-auto p-4')

    def show_lesson(lesson):
        main_content.clear()
        with main_content:
            ui.label(lesson['title']).classes('text-h3 font-bold mb-6 text-blue-400')

            # Bloc Théorie
            if 'theory' in lesson:
                with ui.card().classes('w-full mb-6 p-4'):
                    ui.label('Théorie').classes('text-h5 font-bold mb-2')
                    ui.markdown(lesson['theory']).classes('text-lg')

            # Bloc Flashcards
            if 'flashcards' in lesson:
                with ui.card().classes('w-full mb-6 p-4'):
                    ui.label('Flashcards').classes('text-h5 font-bold mb-4')
                    for card in lesson['flashcards']:
                        with ui.expansion(card['question'], icon='help_outline').classes('w-full bg-gray-800 text-white rounded mb-2'):
                            ui.label(card['answer']).classes('italic p-2 text-green-300')

            # Bloc Projet
            if 'project' in lesson:
                project = lesson['project']
                with ui.card().classes('w-full mb-6 p-4'):
                    ui.label(f"Projet : {project['title']}").classes('text-h5 font-bold mb-2')
                    ui.label(project['description']).classes('mb-4')

                    default_code = f"def {project['target_function']}(args):\n    # Ton code ici\n    pass\n"
                    editor = ui.codemirror(language='python', value=default_code).classes('w-full h-48')
                    
                    result_label = ui.label("Prêt pour l'évaluation.").classes("text-italic mt-4")

                    def evaluate():
                        result_label.set_text("Évaluation en cours...")
                        success = validator.evaluate_code(editor.value, project['target_function'], project['test_cases'])
                        if success:
                            result_label.set_text("[SUCCÈS] Code validé. Tous les tests sont passés.")
                            result_label.classes("text-green-500 font-bold")
                        else:
                            result_label.set_text("[ERREUR] Échec. Regarde le terminal pour les détails.")
                            result_label.classes("text-red-500 font-bold")

                    ui.button("Soumettre le code", on_click=evaluate).classes('mt-4 bg-blue-600')

    # --- BARRE DE NAVIGATION LATÉRALE ---
    with ui.left_drawer(value=True).classes('bg-gray-900 p-4') as sidebar:
        ui.label('Parcours').classes('text-h6 font-bold mb-4 text-gray-300')
        for lesson in lessons:
            ui.button(lesson['title'], on_click=lambda l=lesson: show_lesson(l)).classes('w-full mb-2 bg-gray-800 hover:bg-gray-700 text-left')

    if lessons:
        show_lesson(lessons[0])

ui.run(title="Apprentissage Python", port=8888, dark=True)