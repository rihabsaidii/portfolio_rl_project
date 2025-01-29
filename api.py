import os
import json
from flask import Flask, request, jsonify

# Paths and Data Loading
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'data'))
# Load optimal weights
optimal_weights_path = os.path.join(DATA_DIR, 'optimal_weights.json')
if os.path.exists(optimal_weights_path):
    with open(optimal_weights_path, 'r') as f:
        optimal_weights = json.load(f)
else:
    raise FileNotFoundError(f"Le fichier {optimal_weights_path} est introuvable.")

# Initialisation de Flask
app = Flask(__name__)

@app.route('/optimiser', methods=['POST'])
def optimiser_portefeuille():
    data = request.get_json()
    print('data', data)
    stocks = data['stocks']
    print('stocks', stocks)
    stocks_tuple = tuple(sorted(stocks))  # Trie pour cohérence

    # Convertir la combinaison en chaîne de caractères pour correspondre aux clés du dictionnaire
    stocks_key = ','.join(stocks_tuple)

    # Log pour afficher la combinaison triée
    print(f"Combinaison de stocks demandée : {stocks_key}")
    print(optimal_weights)

    # Vérifier si la combinaison existe dans les clés de optimal_weights
    if stocks_key in optimal_weights:
        poids = optimal_weights[stocks_key]
        return jsonify({'poids_optimaux': poids})

    # Log si la combinaison n'est pas trouvée
    print(f"Combinaison de stocks {stocks_key} non trouvée dans les poids optimaux.")
    return jsonify({'erreur': 'Combinaison de stocks non trouvée'}), 404



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
