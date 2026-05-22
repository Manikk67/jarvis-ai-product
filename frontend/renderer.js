const chatBox = document.getElementById("chatBox");

async function sendMessage() {

    const input = document.getElementById("userInput");

    const message = input.value;

    if (!message.trim()) return;

    // USER MESSAGE

    chatBox.innerHTML += `
        <div class="user">
            🧑 ${message}
        </div>
    `;

    // AI THINKING

    chatBox.innerHTML += `
        <div class="bot">
            🤖 Jarvis is thinking...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    // SEND TO PYTHON BACKEND

    try {

        const response = await fetch(

            "http://127.0.0.1:5000/jarvis",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({

                    command: message
                })
            }
        );

        const data = await response.json();

        // REMOVE THINKING MESSAGE

        const botMessages =
            document.querySelectorAll(".bot");

        botMessages[
            botMessages.length - 1
        ].remove();

        // REAL RESPONSE

        chatBox.innerHTML += `
            <div class="bot">
                🤖 ${data.response}
            </div>
        `;

    }

    catch (error) {

        chatBox.innerHTML += `
            <div class="bot">
                ❌ Backend connection failed.
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";
}

function openManual() {

    document.getElementById(
        "manualModal"
    ).style.display = "block";
}

function closeManual() {

    document.getElementById(
        "manualModal"
    ).style.display = "none";
}

function showHistory() {

    alert(
        "🚀 Command history system coming soon."
    );
}