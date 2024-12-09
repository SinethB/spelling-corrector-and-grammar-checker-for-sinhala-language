import re
import numpy as np
import unicodedata
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import difflib

# Load the trained LSTM model
model = tf.keras.models.load_model("./models/spelling_checker_model.h5")

# Set up tokenizer (ensure it's the same tokenizer used during training)
tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)

# Define max_length based on training setup
max_length = 20  # Adjust to match training

def load_dictionary():
    """
    Load the dictionary of unique Sinhala words from a text file.
    """
    with open('./Sinhala_dictionary/sinhala_dictionary.txt', 'r', encoding='utf-8') as f:
        return set(unicodedata.normalize('NFC', word.strip().lower()) for word in f.readlines())

# Load dictionary and fit tokenizer
dictionary = load_dictionary()
tokenizer.fit_on_texts(dictionary)

def preprocess_text(text):
    """
    Preprocess the given text by removing unwanted characters and normalizing it.
    This function will keep only Sinhala characters and spaces.
    """
    text = re.sub(r'[^\u0D80-\u0DFF\s]', '', text)
    text = unicodedata.normalize('NFC', text.strip().lower())
    return text

def predict_correction(word):
    """
    Predict the corrected version of a word using the loaded LSTM model.
    """
    # Tokenize and pad the input word
    seq = tokenizer.texts_to_sequences([word])
    padded_seq = pad_sequences(seq, maxlen=max_length, padding='post')

    # Use the model to predict the sequence of characters
    prediction = model.predict(padded_seq)
    
    # Convert prediction back to text
    corrected_word = "".join(
        [tokenizer.index_word.get(idx, "") for idx in prediction.argmax(axis=1) if np.all(idx != 0)]
    )
    return corrected_word

def check_spelling(text):
    """
    Check the spelling of words in the text using the LSTM model for corrections if necessary.
    """
    words = re.findall(r'\S+|\s+', text)  # This regex captures words and whitespace separately
    corrected_text = []

    for word in words:
        if word.isspace() or not re.search(r'[^\W\d_]', word):
            corrected_text.append(word)
        else:
            clean_word = re.sub(r'[^\u0D80-\u0DFF]', '', word)
            clean_word = unicodedata.normalize('NFC', clean_word.lower())

            if clean_word in dictionary:
                corrected_text.append(word)
            else:
                # Predict correction using the LSTM model
                corrected_word = predict_correction(clean_word)

                # Fall back to difflib for close matches if the prediction doesn't return a good result
                if corrected_word not in dictionary:
                    suggestions = difflib.get_close_matches(clean_word, dictionary, n=3)
                    corrected_word = suggestions[0] if suggestions else corrected_word

                # Display corrected word with suggestion for hover effect
                suggestions_str = ', '.join(suggestions)
                corrected_text.append(f'<span class="spelling-error" title="Suggestions: {suggestions_str}">{word}</span>')

    return ''.join(corrected_text)
