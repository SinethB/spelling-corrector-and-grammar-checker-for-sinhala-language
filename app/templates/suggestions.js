function showSuggestions(wordElement) {
    // Retrieve suggestions directly from the title attribute
    const suggestionsHTML = wordElement.getAttribute('title');
    const suggestionBox = document.createElement('div');
    suggestionBox.classList.add('suggestion-box');

    // Convert HTML string to DOM elements
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = suggestionsHTML;
    const suggestions = tempDiv.children;

    // Add suggestions to the suggestion box
    Array.from(suggestions).forEach(suggestionElement => {
        suggestionElement.addEventListener('click', function() {
            applySuggestion(wordElement, suggestionElement.textContent);
        });

        suggestionElement.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                applySuggestion(wordElement, suggestionElement.textContent);
            }
        });

        suggestionBox.appendChild(suggestionElement);
    });

    // Remove any existing suggestion box and add the new one
    removeExistingSuggestionBox();
    wordElement.appendChild(suggestionBox);

    // Position the suggestion box
    const rect = wordElement.getBoundingClientRect();
    suggestionBox.style.position = 'absolute';
    suggestionBox.style.top = `${rect.bottom + window.scrollY}px`;
    suggestionBox.style.left = `${rect.left}px`;

    // Handle arrow key navigation
    handleArrowNavigation(suggestionBox);
}

function applySuggestion(wordElement, suggestionText) {
    // Replace the incorrect word with the selected suggestion
    wordElement.innerHTML = suggestionText;
    removeExistingSuggestionBox();
}

function removeExistingSuggestionBox() {
    const existingSuggestionBox = document.querySelector('.suggestion-box');
    if (existingSuggestionBox) {
        existingSuggestionBox.remove();
    }
}

function handleArrowNavigation(suggestionBox) {
    const suggestionElements = suggestionBox.querySelectorAll('div');
    let currentIndex = -1;

    suggestionBox.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown') {
            currentIndex = (currentIndex + 1) % suggestionElements.length;
            suggestionElements[currentIndex].focus();
        } else if (e.key === 'ArrowUp') {
            currentIndex = (currentIndex - 1 + suggestionElements.length) % suggestionElements.length;
            suggestionElements[currentIndex].focus();
        }
    });
}
