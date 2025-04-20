class RecordingHandler {
    constructor(stream, socket, roomId) {
        this.stream = stream;
        this.socket = socket;
        this.roomId = roomId;
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.isRecording = false;
        this.init();
    }

    init() {
        const options = { mimeType: 'video/webm;codecs=vp9,opus' };
        this.mediaRecorder = new MediaRecorder(this.stream, options);
        
        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.recordedChunks.push(event.data);
            }
        };

        this.mediaRecorder.onstop = () => {
            const blob = new Blob(this.recordedChunks, { type: 'video/webm' });
            this.saveRecording(blob);
            this.recordedChunks = [];
        };

        document.getElementById('start-recording').onclick = () => this.toggleRecording();
    }

    toggleRecording() {
        if (!this.isRecording) {
            this.startRecording();
        } else {
            this.stopRecording();
        }
        this.isRecording = !this.isRecording;
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
        formData.append('room_id', this.roomId);

        try {
            const response = await fetch('/virtual_classroom/save-recording/', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            console.log('Recording saved:', data);
        } catch (error) {
            console.error('Failed to save recording:', error);
        }
    }
}
