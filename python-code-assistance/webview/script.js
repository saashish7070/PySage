const vscode = acquireVsCodeApi();

document.getElementById("sendButton").addEventListener("click", sendMessage);
document.getElementById("chatInput").addEventListener("keypress", function (event) {
    if (event.key === "Enter") sendMessage();
});

function sendMessage() {
    const inputField = document.getElementById("chatInput");
    const message = inputField.value.trim();
    
    if (message) {
        appendMessage("You", message);
        vscode.postMessage({ type: "sendMessage", text: message });
        inputField.value = "";
    }
}

window.addEventListener("message", event => {
    const response = event.data.text;
    appendMessage("Pysage", response);
});

function appendMessage(sender, text) {
    const chatbox = document.getElementById("chatbox");
    const messageElement = document.createElement("p");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}
