function addMessage() {
    var messageInput = document.getElementById("messageInput");
    var messageContainer = document.getElementById("messageContainer");

    if (messageInput.value.trim() !== "") {
        var message = document.createElement("div");
        message.textContent = messageInput.value;
        messageContainer.appendChild(message);
        messageInput.value = "";
    } else {
        alert("type")
    }
}

function enterPress(ele) {
    if (ele.keyCode === 13) {
        addMessage();
    }
}