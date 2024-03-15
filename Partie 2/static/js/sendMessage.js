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

    // Faire une condition pour savoir qui envoie le msg. Pour savoir si l'utilisateur envoie ou reçois
    // if(){

    // const content = `
    // <div class="d-flex align-items-end flex-column">
    //     <div class="message-top">
    //         <span>
    //             <strong>${username}</strong>
    //         </span>
    //         <span>
    //             ${new Date().toLocaleString()}
    //         </span>
    //     </div>
    //     <hr class="ligne">
    //     <div class="message-bottom">
    //         <p> ${message} </p>
    //     </div>
    // </div>
    // `;

    // }else {
    const content = `
    <div class="message-top-envoye">
        <span>
            <strong>${username}</strong>
        </span>
        <span>
            ${new Date().toLocaleString()}
        </span>
    </div>
    <hr class="ligne">
    <div class="message-bottom-envoye">
        <p> ${message} </p>
    </div>
    `;
    // }
    messages.innerHTML += content;
};