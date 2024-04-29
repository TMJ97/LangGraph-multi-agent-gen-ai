document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const fileInput = document.getElementById("file-input");
  const chatMessages = document.getElementById("chat-messages");

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const file = fileInput.files[0];
    if (file) {
      sendMessage(file);
      fileInput.value = "";
    } else {
      alert("Please select a file.");
    }
  });

  function sendMessage(file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("/send_message", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          const agentSteps = data.agent_steps
            .map((step) => `<div>${step}</div>`)
            .join("");
          const responseElement = document.createElement("div");
          responseElement.innerHTML = `
                    <strong>Assistant:</strong> ${data.response}<br>
                    <strong>Agent Steps:</strong><br>${agentSteps}<br>
                    <a href="${data.download_url}" download="${data.download_filename}">Download Cleaned Data</a>
                `;
          chatMessages.appendChild(responseElement);
          chatMessages.scrollTop = chatMessages.scrollHeight;
        }
      });
  }
});
