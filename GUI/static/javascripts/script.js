async function addMessage() {
    var messageInput = document.getElementById("messageInput");
    var messageContainer = document.getElementById("messageContainer");

    if (messageInput.value.trim() !== "") {
        var message = document.createElement("div");
        message.textContent = "You: "+messageInput.value;

        // User input message
        messageContainer.append(message);
        messageInput.value = "";
        
        // Chat bot response
        var fetchAIResponse = await invokePythonFunction(message.textContent); // Wait for the response
        var botResponse = document.createElement("div");
        botResponse.textContent = "Bob the bot: "+fetchAIResponse.result; // Assuming result contains the response
        messageContainer.append(botResponse);


    } else {
        alert("type")
    }
}

function enterPress(ele) {
    if (ele.keyCode === 13) {
        addMessage();
    }

}


function invokePythonFunction(text) {
    // Make an AJAX request to the Flask server

    return fetch('/invoke_python_function?prompt='+text)
      .then(response => response.json())
      .then(data => {
        // Return the result from Python
        return data;
      })
      .catch(error => console.error('Error:', error));
}