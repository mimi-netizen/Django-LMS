class ClassroomRecorder {
    constructor(stream, socket) {
        this.stream = stream;
        this.socket = socket;
        this.chunks = [];
        this.mediaRecorder = null;
        this.setupRecorder();
    }

    setupRecorder() {
        this.mediaRecorder = new MediaRecorder(this.stream);
        
        this.mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                this.chunks.push(e.data);
            }
        };

        this.mediaRecorder.onstop = () => {
            const blob = new Blob(this.chunks, { type: 'video/webm' });
            this.saveRecording(blob);
            this.chunks = [];
        };
    }

    startRecording() {
        this.mediaRecorder.start();
        this.socket.send(JSON.stringify({
            type: 'recording_started',
            action: 'start'
        }));
    }

    stopRecording() {
        this.mediaRecorder.stop();
        this.socket.send(JSON.stringify({
            type: 'recording_started',
            action: 'stop'
        }));
    }

    async saveRecording(blob) {
        const formData = new FormData();
        formData.append('recording', blob);
        
        try {
            await fetch('/virtual_classroom/save-recording/', {
                method: 'POST',
                body: formData
            });
        } catch (error) {
            console.error('Failed to save recording:', error);
        }
    }
}
