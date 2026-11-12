import sys
import json
from pathlib import Path
from nicegui import ui

BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))
from core import validator, db

def load_lessons():
    lessons = []
    modules_dir = BASE_DIR / "data" / "modules"
    for file in sorted(modules_dir.glob("*.json")):
        with open(file, "r", encoding="utf-8") as f:
            lessons.append(json.load(f))
    return lessons

lessons = load_lessons()

@ui.page('/')
def main_page():
    # --- EN-TÊTE (Bleu Python) ---
    with ui.header().classes('bg-[#3776AB] justify-between items-center p-4 border-b-4 border-[#FFD43B]'):
        ui.label('Python Learning App - Parcours Data/IA').classes('text-h5 font-bold text-white')
        ui.button('Menu', on_click=lambda: sidebar.toggle()).props('flat color=white')

    main_content = ui.column().classes('w-full max-w-5xl mx-auto p-4')

    def show_lesson(lesson):
        main_content.clear()
        with main_content:
            # Titre de la leçon (Jaune Python)
            ui.label(lesson['title']).classes('text-h3 font-bold mb-4 text-[#FFD43B]')

            # --- ONGLETS (Jaune Python) ---
            with ui.tabs().classes('w-full text-[#FFD43B]') as tabs:
                tab_theory = ui.tab('Théorie', icon='menu_book')
                tab_flashcards = ui.tab('Flashcards', icon='style')
                tab_quiz = ui.tab('Compréhension', icon='psychology')
                tab_projects = ui.tab('Projets', icon='terminal')

            with ui.tab_panels(tabs, value=tab_theory).classes('w-full bg-transparent'):
                
                # --- THÉORIE ---
                with ui.tab_panel(tab_theory):
                    if 'theory' in lesson:
                        with ui.card().classes('w-full p-6 bg-[#1E1E1E] text-white border-l-4 border-[#3776AB]'):
                            ui.markdown(lesson['theory']).classes('text-lg')

                # --- FLASHCARDS ---
                with ui.tab_panel(tab_flashcards):
                    if 'flashcards' in lesson:
                        ui.label(f"{len(lesson['flashcards'])} cartes à réviser").classes('text-gray-400 mb-4')
                        for card in lesson['flashcards']:
                            with ui.expansion(card['question']).classes('w-full bg-[#1E1E1E] text-white rounded mb-2 border border-gray-700'):
                                ui.label(card['answer']).classes('italic p-4 text-[#FFD43B]')

                # --- COMPRÉHENSION DE CODE ---
                with ui.tab_panel(tab_quiz):
                    quiz_list = lesson.get('code_comprehension', [])
                    if not quiz_list and 'code_quiz' in lesson:
                        quiz_list = [lesson['code_quiz']]
                        
                    for i, quiz in enumerate(quiz_list, 1):
                        with ui.card().classes('w-full mb-6 p-4 bg-[#1E1E1E] border border-gray-700'):
                            ui.label(f"Exercice {i}").classes('text-h6 font-bold mb-2 text-[#3776AB]')
                            ui.markdown(f"```python\n{quiz['snippet']}\n```")
                            
                            radio = ui.radio(quiz['options']).classes('mt-4')
                            feedback = ui.label().classes('mt-2 font-bold')
                            
                            def check_answer(q=quiz, r=radio, f=feedback):
                                if r.value == q['correct_answer']:
                                    f.set_text("[SUCCÈS] Bonne réponse !")
                                    f.classes(replace='text-green-500 font-bold')
                                else:
                                    f.set_text(f"[ERREUR] Faux. La bonne réponse était : {q['correct_answer']}")
                                    f.classes(replace='text-red-500 font-bold')
                                    
                            # Bouton (Bleu Python)
                            ui.button("Vérifier", on_click=check_answer).classes('mt-4 bg-[#3776AB] hover:bg-[#2A5A82] text-white')

                # --- PROJETS ---
                with ui.tab_panel(tab_projects):
                    project_list = lesson.get('projects', [])
                    if not project_list and 'project' in lesson:
                        project_list = [lesson['project']]
                        
                    for i, project in enumerate(project_list, 1):
                        with ui.card().classes('w-full mb-8 p-4 bg-[#1E1E1E] border-t-4 border-[#FFD43B]'):
                            ui.label(f"Projet {i} : {project['title']}").classes('text-h5 font-bold mb-2 text-[#FFD43B]')
                            ui.markdown(project['description']).classes('mb-4')

                            default_code = f"def {project['target_function']}(args):\n    # Ton code ici\n    pass\n"
                            editor = ui.codemirror(language='python', value=default_code).classes('w-full h-48 mb-4')
                            result_label = ui.label("En attente de soumission...").classes("text-italic")

                            def evaluate(p=project, ed=editor, res=result_label):
                                res.set_text("Évaluation en cours...")
                                success = validator.evaluate_code(ed.value, p['target_function'], p['test_cases'])
                                if success:
                                    res.set_text(f"[SUCCÈS] Projet '{p['title']}' validé !")
                                    res.classes(replace="text-green-500 font-bold")
                                    db.save_progress(lesson['module_id'], 1)
                                else:
                                    res.set_text("[ERREUR] Tests échoués. Regarde ton terminal.")
                                    res.classes(replace="text-red-500 font-bold")

                            ui.button("Exécuter les tests", on_click=evaluate).classes('bg-[#3776AB] hover:bg-[#2A5A82] text-white')

    # --- BARRE LATÉRALE ---
    with ui.left_drawer(value=True).classes('bg-[#111111] p-4 border-r border-gray-800') as sidebar:
        ui.label('Parcours').classes('text-h6 font-bold mb-4 text-[#FFD43B]')
        db.init_db()
        progress_data = db.get_all_progress()
        
        for lesson in lessons:
            mod_id = lesson['module_id']
            if mod_id in progress_data:
                # Garde le vert pour indiquer le succès, mais plus sombre pour coller au thème
                btn_color = 'bg-green-900 hover:bg-green-800 text-green-200'
            else:
                btn_color = 'bg-[#1E1E1E] hover:bg-[#2A2A2A] text-white'
                
            ui.button(lesson['title'], on_click=lambda l=lesson: show_lesson(l)).classes(f'w-full mb-2 text-left {btn_color}')

    if lessons:
        show_lesson(lessons[0])

ui.run(title="Apprentissage Python", port=8888, dark=True)