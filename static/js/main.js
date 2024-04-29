document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const messageInput = document.getElementById("message-input");
  const chatMessages = document.getElementById("chat-messages");

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    if (message !== "") {
      sendMessage(message);
      messageInput.value = "";
    }
  });

  function sendMessage(message) {
    const messageElement = document.createElement("div");
    messageElement.innerHTML = `<strong>You:</strong> ${message}`;
    chatMessages.appendChild(messageElement);

    fetch("/send_message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        const responseElement = document.createElement("div");
        responseElement.innerHTML = `<strong>Bot:</strong> ${data.response}`;
        chatMessages.appendChild(responseElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
      });
  }
});
