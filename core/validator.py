def evaluate_code(user_code_str, function_name, test_cases):
    """
    Exécute le code de l'utilisateur et le confronte à des cas de test.
    """
    # 1. Créer un espace mémoire isolé pour stocker les fonctions de l'utilisateur
    namespace = {}
    
    try:
        # 2. Exécuter le texte brut comme du vrai code Python
        exec(user_code_str, namespace)
        
        # 3. Vérifier si l'utilisateur a bien nommé sa fonction comme demandé
        if function_name not in namespace:
            print(f"Erreur : La fonction '{function_name}' est introuvable.")
            return False
            
        user_function = namespace[function_name]
        
        # 4. Faire passer les tests incrémentaux
        print("\n--- Lancement des tests du projet ---")
        for i, test in enumerate(test_cases, 1):
            test_input = test["input"]
            expected = test["expected"]
            
            # Exécuter la fonction de l'utilisateur avec l'entrée de test
            result = user_function(test_input)
            
            if result == expected:
                print(f"Test {i} passé avec succès ! (Entrée: {test_input} -> Sortie: {result})")
            else:
                print(f"Échec au test {i}. Attendu : {expected}, Obtenu : {result}")
                return False
                
        print("Toutes les étapes du projet sont validées ! Score incrémenté.")
        return True
        
    except Exception as e:
        # Capturer les erreurs de syntaxe ou d'exécution dans le code de l'utilisateur
        print(f"Erreur d'exécution dans ton code : {type(e).__name__} - {str(e)}")
        return False

# ==========================================
# TEST DU VALIDATEUR (Simulation locale)
# ==========================================
if __name__ == "__main__":
    # 1. Ce que le JSON définira pour le projet de fin de module
    target_function = "additionner"
    tests = [
        {"input": (2, 3), "expected": 5},
        {"input": (-1, 1), "expected": 0}
    ]
    
    # 2. Ce que l'utilisateur écrira plus tard dans Streamlit (simulé ici en texte)
    # Modifie le '+' en '*' ci-dessous pour voir le test échouer !
    code_soumis = """
def additionner(args):
    a, b = args
    return a + b
"""

    # 3. L'évaluation
    evaluate_code(code_soumis, target_function, tests)