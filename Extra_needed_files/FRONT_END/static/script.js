document.addEventListener('DOMContentLoaded', () => {
    // 1. Speech-to-Text Functionality
    const micButton = document.getElementById('mic-button');
    const searchInput = document.querySelector('.search-input');
    
    // Check for browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false; // Stop after one phrase
        recognition.lang = 'en-IN'; // Use an Indian English model for better accuracy

        micButton.addEventListener('click', () => {
            recognition.start();
            micButton.style.color = 'red';
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            searchInput.value = transcript;
            micButton.style.color = '#4dcfff'; // Reset color
        };

        recognition.onspeechend = () => {
            recognition.stop();
            micButton.style.color = '#4dcfff';

        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            micButton.style.color = '#4dcfff';
            micButton.classList.remove('blinking-mic');
            alert('Speech recognition not available or an error occurred. Please try typing.');
        };
    } else {
        micButton.style.display = 'none'; // Hide the mic button if not supported
        console.warn('Speech Recognition not supported in this browser.');
    }
});