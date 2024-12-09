from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class SinhalaGrammarCorrector:
    def __init__(self, model_folder):
        """
        Initialize the grammar corrector with the model and tokenizer from the specified folder.
        """
        # Install sentencepiece if needed (make sure it's in your environment)
        try:
            import sentencepiece
        except ImportError:
            raise ImportError("SentencePiece is required for this model. Please install it using `pip install sentencepiece`.")
        
        # Load the tokenizer (use slow tokenizer if needed)
        self.tokenizer = AutoTokenizer.from_pretrained(model_folder, use_fast=False)  # Change here

        # Load the model
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_folder)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def correct_sentence(self, input_text):
        """
        Corrects grammar for the entire text using the model.
        """
        # Tokenize input text
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        # Generate output
        outputs = self.model.generate(**inputs)
        
        # Decode the output sequence
        corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return corrected_text

    def check_grammar(self, input_text):
        """
        Identifies grammatical errors in the input text and suggests corrections.
        """
        corrected_text = self.correct_sentence(input_text)
        highlighted_text = self.highlight_grammar_errors(input_text, corrected_text)
        return highlighted_text

    def highlight_grammar_errors(self, original_text, corrected_text):
        """
        Highlight grammar errors by comparing the original and corrected texts.
        """
        errors = []
        original_tokens = original_text.split()
        corrected_tokens = corrected_text.split()

        for orig, corr in zip(original_tokens, corrected_tokens):
            if orig != corr:
                errors.append(f'<span class="grammar-error" title="Correct: {corr}">{orig}</span>')
            else:
                errors.append(orig)
        
        return " ".join(errors)
