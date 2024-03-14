const socketio = io();

const messages = document.getElementById("messages");

// Reception du message serveur
socketio.on("message", (data) => {
    console.log(data);
    createMessage(data.username, data.message);
});

// Envoi du message au serveur
const sendMessage = () => {
    const message = document.getElementById("message");
    if (message.value == "") return;
    socketio.emit("message", { data: message.value });
    message.value = "";
};

// Création du message
const createMessage = (username, message) => {
    const content = `
    <div>
        <span>
            <strong>${username}</strong>: ${message}
        </span>
        <span>
            ${new Date().toLocaleString()}
        </span>
    </div>
    `;
    messages.innerHTML += content;
};