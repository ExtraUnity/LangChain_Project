async function addMessage() {
    var messageInput = document.getElementById("messageInput");
    var messageContainer = document.getElementById("messageContainer");

    if (messageInput.value.trim() !== "") {
        var apiKey = document.getElementById("APIKeyInput");
        var message = document.createElement("div");
        message.textContent = "User: "+messageInput.value;
    
        // User input message
        messageContainer.append(message);
        messageInput.value = "";        
        messageContainer.scrollTop = messageContainer.scrollHeight;

        var llm = -1;
        if(document.getElementById("FireWorks").checked) {
            llm = 0;
        } else if (document.getElementById("OpenAi").checked) {
            llm = 1
        }

        // Chat bot response
        var fetchAIResponse = await invokePythonFunction(message.textContent, llm, apiKey.value); // Wait for the response
        var botResponse = document.createElement("div");
        botResponse.textContent = "ChatBot: "+fetchAIResponse.result; // Assuming result contains the response
        messageContainer.append(botResponse);
        messageContainer.scrollTop = messageContainer.scrollHeight;

    } else {
        alert("type")
    }
}

function enterPress(ele) {
    if (ele.keyCode === 13) {
        addMessage();
    }

}


function invokePythonFunction(text, llm, apiKey) {
    // Make an AJAX request to the Flask server

    return fetch('/invoke_python_function?prompt='+text+'&llm='+llm+'&api='+apiKey)
      .then(response => response.json())
      .then(data => {
        // Return the result from Python
        return data;
      })
      .catch(error => console.error('Error:', error));
}