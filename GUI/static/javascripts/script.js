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


var input = document.getElementById("messageInput");
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("addMessage").click();
    }
});
    