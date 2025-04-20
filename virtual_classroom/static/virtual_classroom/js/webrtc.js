class VirtualClassroom {
    constructor(roomName, iceServers) {
        this.roomName = roomName;
        this.peerConnections = {};
        this.localStream = null;
        this.socket = new WebSocket(
            `ws://${window.location.host}/ws/classroom/${roomName}/`
        );
        this.configuration = { iceServers };
        this.initializeWebSocket();
        this.initializeMedia();
    }

    async initializeMedia() {
        try {
            this.localStream = await navigator.mediaDevices.getUserMedia({
                audio: true,
                video: true
            });
            this.addVideoStream('local', this.localStream);
        } catch (err) {
            console.error('Failed to get media devices:', err);
        }
    }

    initializeWebSocket() {
        this.socket.onmessage = async (event) => {
            const data = JSON.parse(event.data);
            switch(data.type) {
                case 'new-peer':
                    await this.handleNewPeer(data.peerId);
                    break;
                case 'offer':
                    await this.handleOffer(data.offer, data.peerId);
                    break;
                case 'answer':
                    await this.handleAnswer(data.answer, data.peerId);
                    break;
                case 'ice-candidate':
                    await this.handleIceCandidate(data.candidate, data.peerId);
                    break;
            }
        };
    }

    // ... Additional WebRTC methods for peer connections, 
    // screen sharing, recording, and whiteboard functionality
}

class WebRTCHandler {
    constructor(socket, roomId) {
        this.socket = socket;
        this.roomId = roomId;
        this.peerConnections = {};
        this.localStream = null;
        this.remoteStreams = {};
        this.iceServers = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
            ]
        };
        this.init();
    }

    async init() {
        try {
            this.localStream = await navigator.mediaDevices.getUserMedia({
                audio: true,
                video: true
            });
            this.addVideoStream('local', this.localStream);
            this.socket.addEventListener('message', this.handleSocketMessage.bind(this));
        } catch (err) {
            console.error('Media device error:', err);
        }
    }

    handleSocketMessage(event) {
        const data = JSON.parse(event.data);
        switch (data.type) {
            case 'new-peer':
                this.handleNewPeer(data.peerId);
                break;
            case 'offer':
                this.handleOffer(data.offer, data.peerId);
                break;
            case 'answer':
                this.handleAnswer(data.answer, data.peerId);
                break;
            case 'ice-candidate':
                this.handleIceCandidate(data.candidate, data.peerId);
                break;
        }
    }

    async createPeerConnection(peerId) {
        const pc = new RTCPeerConnection(this.iceServers);
        
        pc.onicecandidate = (event) => {
            if (event.candidate) {
                this.socket.send(JSON.stringify({
                    type: 'ice-candidate',
                    candidate: event.candidate,
                    peerId: peerId
                }));
            }
        };

        pc.ontrack = (event) => {
            this.addVideoStream(`remote-${peerId}`, event.streams[0]);
        };

        this.localStream.getTracks().forEach(track => {
            pc.addTrack(track, this.localStream);
        });

        this.peerConnections[peerId] = pc;
        return pc;
    }

    addVideoStream(id, stream) {
        const videoGrid = document.getElementById('video-grid');
        const video = document.createElement('video');
        video.id = id;
        video.srcObject = stream;
        video.autoplay = true;
        video.playsInline = true;
        videoGrid.appendChild(video);
    }
}

// Initialize the virtual classroom
const classroom = new VirtualClassroom(roomName, iceServers);
