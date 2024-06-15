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

        // Chat bot response
        var fetchAIResponse = await getResponse(message.textContent, apiKey.value); // Wait for the response
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

function enterPressAPI(ele) {
    if (ele.keyCode === 13) {
        updateAPI();
    }
}

function updateAPI() {
    var apiKey = document.getElementById("APIKeyInput").value.trim();
    if(apiKey === "") {
        return
    }
    var status = document.getElementById("statusText");
    document.getElementById("APIKeyInput").value = "";
    status.textContent = "Fetching model..."
    status.style.color = "white";
    return fetch('/updateAPIKey?apiKey='+apiKey)
    .then(response => response.json())
    .then(data => {
        if(data.result === "Error") {
            document.getElementById("statusText").textContent="Invalid API Key!";
            document.getElementById("statusText").style.color = "red";
        } else {
            document.getElementById("statusText").textContent="Valid API Key!";
            document.getElementById("statusText").style.color = "green";
        }
    })
    .catch(error => console.error('Error:', error));
}


function clearMemory() {
    var messageContainer = document.getElementById("messageContainer");
    messageContainer.innerHTML = '';

    return fetch('/clear_history')
    .catch(error => console.error('Error:', error))
}

function getResponse(text, llm) {
    // Make an AJAX request to the Flask server

    return fetch('/generate_response?prompt='+encodeURIComponent(text)+'&llm='+encodeURIComponent(llm))
      .then(response => response.json())
      .then(data => {
        // Return the result from Python
        return data;
      })
      .catch(error => console.error('Error:', error));
}