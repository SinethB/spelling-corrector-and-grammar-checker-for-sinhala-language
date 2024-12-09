from flask import Flask, request, render_template, jsonify
import re
import unicodedata
import difflib
from spelling_corrector import predict_correction, load_dictionary, preprocess_text
from grammar_checker import SinhalaGrammarCorrector

app = Flask(__name__)

# Load dictionary and define max length for tokenization
dictionary = load_dictionary()

# Initialize grammar corrector with model path and tokenizer
grammar_model_folder = './models/grammar_correction_model'  
grammar_corrector = SinhalaGrammarCorrector(model_folder=grammar_model_folder)

# Check spelling and correct words using the LSTM model
def check_spelling(text):
    tokens = re.findall(r'[\u0D80-\u0DFF]+|\s+|[^\u0D80-\u0DFF\s]+', text)
    corrected_text = []

    for token in tokens:
        if re.match(r'[^\u0D80-\u0DFF]', token):
            corrected_text.append(token)  # Non-Sinhala tokens are added as-is
        else:
            clean_word = preprocess_text(token)  # Normalize word
            if clean_word in dictionary:
                corrected_text.append(token)  # Correct word, add without changes
            else:
                # Use LSTM model to predict correction
                corrected_word = predict_correction(clean_word)
                
                # Fall back to difflib if model prediction isn't in dictionary
                if corrected_word not in dictionary:
                    suggestions = difflib.get_close_matches(clean_word, dictionary, n=3)
                    corrected_word = suggestions[0] if suggestions else token
                
                suggestions_str = ', '.join(difflib.get_close_matches(clean_word, dictionary, n=3))
                corrected_text.append(f'<span class="spelling-error" title="Suggestions: {suggestions_str}">{token}</span>')

    return ''.join(corrected_text)

# Auto-correct function that uses model-based predictions or falls back on difflib
def auto_correct_text(text):
    tokens = re.findall(r'[\u0D80-\u0DFF]+|\s+|[^\u0D80-\u0DFF\s]+', text)
    corrected_text = []

    for token in tokens:
        if re.match(r'[^\u0D80-\u0DFF]', token):  
            corrected_text.append(token)  # Non-Sinhala tokens are added as-is
        else:
            clean_word = preprocess_text(token)
            if clean_word in dictionary:
                corrected_text.append(token)
            else:
                corrected_word = predict_correction(clean_word)
                
                # Fallback if model's prediction isn't recognized
                if corrected_word not in dictionary:
                    best_suggestion = difflib.get_close_matches(clean_word, dictionary, n=1)
                    corrected_word = best_suggestion[0] if best_suggestion else token
                
                corrected_text.append(f'<span class="auto-corrected">{corrected_word}</span>')

    return ''.join(corrected_text)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for checking spelling
@app.route('/check', methods=['POST'])
def check_text():
    input_text = request.form.get('input_text', '')
    processed_text = check_spelling(input_text)
    return render_template('index.html', corrected_text=processed_text, input_text=input_text)

# Route for auto-correct feature
@app.route('/auto-correct', methods=['POST'])
def auto_correct():
    data = request.get_json()
    input_text = data.get('text', '')
    corrected_text = auto_correct_text(input_text)
    return jsonify({'corrected_text': corrected_text})

# Route for grammar check
@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    input_text = request.form.get('input_text', '')
    processed_grammar_text = grammar_corrector.check_grammar(input_text)
    return render_template('index.html', corrected_text=processed_grammar_text, input_text=input_text)

if __name__ == "__main__":
    app.run(debug=True)
