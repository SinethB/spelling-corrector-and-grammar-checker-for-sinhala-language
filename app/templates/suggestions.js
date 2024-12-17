// Function to show the suggestion box when hovering over a misspelled or grammar-error word
document.addEventListener("DOMContentLoaded", function () {
    // Select all misspelled and grammar error spans
    const spellingErrors = document.querySelectorAll('.spelling-error');
    const grammarErrors = document.querySelectorAll('.grammar-error');

    // Event listener for hovering over spelling errors
    spellingErrors.forEach(error => {
        error.addEventListener('mouseenter', function () {
            const suggestionBox = this.querySelector('.suggestion-box');
            if (suggestionBox) suggestionBox.style.display = 'block'; // Ensure it's shown
        });

        error.addEventListener('mouseleave', function () {
            const suggestionBox = this.querySelector('.suggestion-box');
            if (suggestionBox) suggestionBox.style.display = 'none'; // Hide suggestion box
        });
    });

    // Event listener for hovering over grammar errors
    grammarErrors.forEach(error => {
        error.addEventListener('mouseenter', function () {
            const suggestionBox = this.querySelector('.suggestion-box');
            if (suggestionBox) suggestionBox.style.display = 'block'; 
        });

        error.addEventListener('mouseleave', function () {
            const suggestionBox = this.querySelector('.suggestion-box');
            if (suggestionBox) suggestionBox.style.display = 'none'; 
        });
    });

    // Function to handle the correction when a suggestion is clicked
    const suggestionItems = document.querySelectorAll('.suggestion');
    suggestionItems.forEach(item => {
        item.addEventListener('click', function () {
            const suggestedText = this.innerText;
            // Replace the error word with the selected suggestion
            const errorSpan = this.closest('span');
            errorSpan.innerHTML = suggestedText; // Update the error word with the correct suggestion
        });
    });
});
