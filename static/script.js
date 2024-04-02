document.addEventListener('DOMContentLoaded', function() {
    // Select the form and the submit button
    const form = document.querySelector('.vocab-form');
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Disable the submit button and change its text to indicate loading
        submitButton.disabled = true;
        submitButton.textContent = 'Generating...';

        // Here, you would typically make an AJAX request to your Flask backend
        // For demonstration, we'll just simulate a delay and then reset the form
        setTimeout(() => {
            // Reset the button state
            submitButton.disabled = false;
            submitButton.textContent = 'Generate';

            // Optional: Show a success message or update the page content
            alert('Vocabulary generated! Check below for results.');

            // Here, you could also update the DOM with the response from your Flask app
            // For this example, we'll just reload the page to see the updated results
            window.location.reload();
        }, 2000); // Simulate a 2-second delay
    });
});
