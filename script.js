document.addEventListener("DOMContentLoaded", function () {
    const uploadButton = document.getElementById("uploadButton");
    
    if (uploadButton) {
        uploadButton.addEventListener("click", uploadImage);
    }

    async function uploadImage() {
        const input = document.getElementById("imageInput");
        const imagePreview = document.getElementById("imagePreview");
        const resultText = document.getElementById("result");

        if (!input || !imagePreview || !resultText) {
            console.error("One or more elements are missing in the DOM.");
            return;
        }

        if (input.files.length === 0) {
            alert("Please select an image first.");
            return;
        }

        // Display the selected image
        const file = input.files[0];
        const reader = new FileReader();
        
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = "block";
        };
        reader.readAsDataURL(file);

        // Prepare form data
        const formData = new FormData();
        formData.append("image", file);

        try {
            // Send image to backend for prediction
            const response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            resultText.innerText = "Prediction: " + result.prediction;
        } catch (error) {
            console.error("Error:", error);
            resultText.innerText = "Error processing image.";
        }
    }
});