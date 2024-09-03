document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select an image to upload.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:8000/predict/', {
            method: 'POST',
            body: formData,
            signal: AbortSignal.timeout(60000) // Increase to 60 seconds
        });

        if (!response.ok) {
            throw new Error('Failed to upload image. Status: ' + response.status);
        }

        const blob = await response.blob();
        const imgUrl = URL.createObjectURL(blob);

        // Display the image
        document.getElementById('output').innerHTML = `<h2>Prediction Result:</h2><img src="${imgUrl}" alt="Predicted Image">`;

    } catch (error) {
        console.error('Error:', error);  // Log the error to the console
        document.getElementById('output').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});
