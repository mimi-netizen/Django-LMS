class VirtualClassroom {
    constructor(config) {
        console.log('Initializing classroom with config:', config);
        // Convert string booleans to real booleans
        this.config = {
            ...config,
            isActive: config.isActive === true || config.isActive === "true",
            isLecturer: config.isLecturer === true || config.isLecturer === "true"
        };
        
        this.setupCSRFToken();
        this.initializeEventHandlers();
        this.initializeComponents();
    }

    setupCSRFToken() {
        const csrfToken = this.config.csrfToken;
        // Add CSRF token to all AJAX requests
        document.querySelectorAll('[data-action]').forEach(button => {
            console.log('Setting up CSRF for:', button);
        });
    }

    initializeEventHandlers() {
        console.log('Setting up event handlers');
        
        // Use event delegation for all controls
        document.addEventListener('click', (e) => {
            const target = e.target.closest('button');
            if (!target) return;

            console.log('Button clicked:', target.id);

            switch(target.id) {
                case 'toggle-session':
                case 'header-toggle-session':
                    this.toggleSession();
                    break;
                    
                case 'controls-start-recording':
                case 'header-start-recording':
                    this.toggleRecording();
                    break;
                    
                case 'controls-toggle-whiteboard':
                case 'header-toggle-whiteboard':
                    this.toggleWhiteboard();
                    break;
                    
                case 'controls-toggle-video':
                    this.webrtc?.toggleVideo();
                    break;
                    
                case 'controls-toggle-audio':
                    this.webrtc?.toggleAudio();
                    break;
                    
                case 'controls-share-screen':
                    this.webrtc?.shareScreen();
                    break;
            }
        });
    }

    initializeComponents() {
        // Initialize WebRTC if session is active
        if (this.config.isActive) {
            this.webrtc = new WebRTCHandler(this.config.roomId);
            this.whiteboard = new Whiteboard('whiteboard');
            if (this.config.isLecturer) {
                this.recorder = new RecordingHandler(this.webrtc.localStream);
            }
        }
    }

    async toggleSession() {
        console.log('Toggling session...');
        try {
            const action = this.config.isActive ? 'deactivate' : 'activate';
            const response = await fetch(`/virtual_classroom/${this.config.roomId}/${action}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.config.csrfToken,
                    'Content-Type': 'application/json',
                },
            });
            
            console.log('Toggle response:', response);
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Failed to toggle session:', await response.text());
            }
        } catch (error) {
            console.error('Error toggling session:', error);
        }
    }

    toggleRecording() {
        if (this.recorder) {
            this.recorder.toggle();
            const button = document.getElementById('start-recording');
            if (button) {
                button.innerHTML = this.recorder.isRecording ? 
                    '<i class="fas fa-stop-circle"></i> Stop Recording' :
                    '<i class="fas fa-record-vinyl"></i> Start Recording';
            }
        }
    }

    toggleWhiteboard() {
        if (this.whiteboard) {
            this.whiteboard.toggle();
            const button = document.getElementById('toggle-whiteboard');
            if (button) {
                button.innerHTML = this.whiteboard.isVisible ? 
                    '<i class="fas fa-chalkboard"></i> Hide Whiteboard' :
                    '<i class="fas fa-chalkboard"></i> Show Whiteboard';
            }
        }
    }
}

// Remove any previous dummy init like: 
// document.addEventListener('DOMContentLoaded', () => {
//   const room = new VirtualClassroom({ roomId: ROOM_ID, ... });
// });

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded');
    if (window.CLASSROOM_CONFIG) {
        const classroom = new VirtualClassroom(window.CLASSROOM_CONFIG);
        window.classroomInstance = classroom;
        console.log('Virtual classroom initialized successfully with config:', window.CLASSROOM_CONFIG);
    } else {
        console.error('CLASSROOM_CONFIG not found.');
    }
});
