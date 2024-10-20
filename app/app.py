from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Load the Sinhala dictionary
def load_dictionary():
    with open('Sinhala_dictionary/sinhala_dictionary.txt', 'r', encoding='utf-8') as f:
        return set(word.strip() for word in f.readlines())

# Function to check spelling
def check_spelling(text, dictionary):
    words = text.split()
    corrected_text = []
    for word in words:
        # Remove punctuation for checking
        clean_word = re.sub(r'[^\w\s]', '', word)
        if clean_word in dictionary:
            corrected_text.append(word)
        else:
            # Mark misspelled words (can implement suggestion logic later)
            corrected_text.append(f'<span class="spelling-error">{word}</span>')
    return ' '.join(corrected_text)

# Function to check grammar (placeholder)
def check_grammar(text):
    # This is a placeholder for grammar checking logic
    # For now, it will simply underline every word
    words = text.split()
    return ' '.join(f'<span class="grammar-error">{word}</span>' for word in words)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    input_text = request.form['input_text']
    dictionary = load_dictionary()
    spelling_checked = check_spelling(input_text, dictionary)
    grammar_checked = check_grammar(spelling_checked)
    
    return render_template('index.html', corrected_text=grammar_checked)

if __name__ == '__main__':
    app.run(debug=True)
