// This function is made by Nikolaj
// Makes sure that the message is added to the chat container and the chatbot response is displayed
async function addMessage() {
    var messageInput = document.getElementById("messageInput");
    var messageContainer = document.getElementById("messageContainer");

    // Check if the user has entered a message
    if (messageInput.value.trim() !== "") {        
        var apiKey = document.getElementById("APIKeyInput");
        var message = document.createElement("div");
        message.textContent = "User: "+messageInput.value;

        // User input message
        messageContainer.append(message);
        messageInput.value = "";        
        messageContainer.scrollTop = messageContainer.scrollHeight;

        // Chat bot time elapsed display
        var botResponse = document.createElement("div");
        botResponse.textContent = "ChatBot: "+ "Computing response... Time elapsed: 0 seconds";
        messageContainer.append(botResponse);
        messageContainer.scrollTop = messageContainer.scrollHeight;

        var startTime = Date.now();
        var updateInterval = setInterval(function() {updateTimeElapsed(botResponse, startTime)}, 1000);

        // Fetch the response from the AI
        var fetchAIResponse = await getResponse(message.textContent, apiKey.value); // Wait for the response
        botResponse.textContent = "ChatBot: "+fetchAIResponse.result; // Assuming result contains the response
        clearInterval(updateInterval);
    } else {
        alert("Enter message")
    }
}

// This function is made by Christian
// Updates the time elapsed in the chatbot response
function updateTimeElapsed(botResponse, startTime) {
    var elapsedTime = Math.floor((Date.now() - startTime) / 1000); // Time elapsed in seconds
    botResponse.textContent = "ChatBot: Computing response... Time elapsed: " + elapsedTime + " seconds";
}

// This function is made by Tobias
// Eventhandler for when user press enter on keyboard
function enterPress(ele) {
    if (ele.keyCode === 13) {
        addMessage();
    }
}

// This function is made by Christian
// Eventhandler for when user press enter on keyboard for API input field
function enterPressAPI(ele) {
    if (ele.keyCode === 13) {
        updateAPI();
    }
}

// This function is made by Christian
// Updates the API key in the backend
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

// This function is made by Tobias
// Clears the agents' chat history
function clearMemory() {
    var messageContainer = document.getElementById("messageContainer");
    messageContainer.innerHTML = '';

    return fetch('/clear_history')
    .catch(error => console.error('Error:', error))
}

// This function is made by Tobias
// Make an AJAX request to the Flask server
function getResponse(text, llm) {
    return fetch('/generate_response?prompt='+encodeURIComponent(text)+'&llm='+encodeURIComponent(llm))
      .then(response => response.json())
      .then(data => {
        return data;
      })
      .catch(error => console.error('Error:', error));
}