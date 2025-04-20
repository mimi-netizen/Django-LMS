class Whiteboard {
    constructor(canvas, socket) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.socket = socket;
        this.drawing = false;
        this.setupCanvas();
        this.bindEvents();
    }

    setupCanvas() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        this.ctx.strokeStyle = '#000000';
        this.ctx.lineWidth = 2;
    }

    bindEvents() {
        this.canvas.addEventListener('mousedown', this.startDrawing.bind(this));
        this.canvas.addEventListener('mousemove', this.draw.bind(this));
        this.canvas.addEventListener('mouseup', this.stopDrawing.bind(this));
        this.socket.addEventListener('message', this.handleMessage.bind(this));
    }

    startDrawing(e) {
        this.drawing = true;
        this.draw(e);
    }

    draw(e) {
        if (!this.drawing) return;
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        this.ctx.lineTo(x, y);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);

        this.socket.send(JSON.stringify({
            type: 'whiteboard_data',
            data: { x, y },
            action: 'draw'
        }));
    }

    stopDrawing() {
        this.drawing = false;
        this.ctx.beginPath();
    }

    handleMessage(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'whiteboard_data') {
            this.drawRemote(data.data);
        }
    }
}
