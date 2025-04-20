class ChatHandler {
    constructor(roomId) {
        this.roomId = roomId;
        this.messageContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-message');
        this.socket = new WebSocket(`ws://${window.location.host}/ws/classroom/${roomId}/chat/`);
        
        this.initializeChat();
    }

    initializeChat() {
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'chat_message') {
                this.displayMessage(data.message);
            }
        };

        this.sendButton.onclick = () => this.sendMessage();
        this.messageInput.onkeypress = (e) => {
            if (e.key === 'Enter') this.sendMessage();
        };
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        if (message) {
            this.socket.send(JSON.stringify({
                type: 'chat_message',
                message: message
            }));
            this.messageInput.value = '';
        }
    }

    displayMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message';
        messageElement.textContent = message;
        this.messageContainer.appendChild(messageElement);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
}
