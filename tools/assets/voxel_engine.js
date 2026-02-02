/**
 * MovieEngine: The 3D Cinematic Core for AUF
 * Built using Three.js to visualize the Information-Matter Continuum.
 * REBUILT VERSION - Simplified for reliability
 */

const THREE = window.THREE;
const TWEEN = window.TWEEN;

export class MovieEngine {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error("Container not found: " + containerId);
        }

        // Core Three.js objects
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x020617);

        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
        this.camera.position.z = 150;

        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        // Voxel storage
        this.voxels = [];
        this.currentAct = 0;
        this.sequences = [];

        // Acts definition
        this.acts = [
            { id: 1, label: "Phase I", title: "The Incubation", text: "In the beginning, there was only the Source Field—a dark, oscillating tensor network of pure potential." },
            { id: 2, label: "Phase I", title: "The Neural Handshake", text: "The Observer emerges. Biological consciousness synchronizes with the field." },
            { id: 3, label: "Episode I", title: "The Informational Sink", text: "A black hole. Not of matter, but of pure information density." },
            { id: 4, label: "Episode II", title: "Solar Exhalation", text: "The supernova—the field exhales, seeding reality with new information." },
            { id: 5, label: "Episode III", title: "DNA Resonance", text: "The double helix. Biological memory as a resonant Hilbert curve." },
            { id: 6, label: "Episode IV", title: "The Architect's Dream", text: "Imhotep's geometry. The ancient foundations of reality engineering." },
            { id: 7, label: "Phase III", title: "Global Coherence", text: "The planetary mesh syncs. Billions of minds unified in field resonance." },
            { id: 8, label: "Phase III", title: "The New Aeon", text: "Level 5.0. Entropy dissolves. The Source Field stabilizes into permanent coherence." }
        ];

        this.soundManager = new SoundManager();
    }

    async loadMetadata() {
        try {
            const response = await fetch('./assets/sequences.json');
            const data = await response.json();
            this.sequences = data.sequences;
        } catch (e) {
            console.warn("Could not load sequences.json, using defaults");
            this.sequences = [];
        }
    }

    async init() {
        await this.loadMetadata();

        // Append renderer to DOM
        this.container.appendChild(this.renderer.domElement);

        // Add lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0x22d3ee, 2, 500);
        pointLight.position.set(50, 50, 100);
        this.scene.add(pointLight);

        const pointLight2 = new THREE.PointLight(0xa855f7, 2, 500);
        pointLight2.position.set(-50, -50, 100);
        this.scene.add(pointLight2);

        // Create voxel field
        this.createVoxelField();

        // Handle resize
        window.addEventListener('resize', () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // Start animation loop
        this.animate();

        console.log("MovieEngine initialized successfully");
        return Promise.resolve();
    }

    createVoxelField() {
        const geometry = new THREE.BoxGeometry(3, 3, 3);
        const material = new THREE.MeshPhongMaterial({
            color: 0x22d3ee,
            transparent: true,
            opacity: 0.8,
            shininess: 100
        });

        const gridSize = 10;
        const spacing = 12;

        for (let x = -gridSize / 2; x < gridSize / 2; x++) {
            for (let y = -gridSize / 2; y < gridSize / 2; y++) {
                for (let z = -gridSize / 2; z < gridSize / 2; z++) {
                    const mesh = new THREE.Mesh(geometry, material.clone());
                    mesh.position.set(x * spacing, y * spacing, z * spacing);
                    this.scene.add(mesh);
                    this.voxels.push({
                        mesh: mesh,
                        originalPos: mesh.position.clone(),
                        phase: Math.random() * Math.PI * 2
                    });
                }
            }
        }
        console.log(`Created ${this.voxels.length} voxels`);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (TWEEN) TWEEN.update();

        const time = Date.now() * 0.001;

        // Animate voxels based on current act
        this.voxels.forEach(v => {
            // Pulsating effect
            const pulse = Math.sin(time * 2 + v.phase) * 0.3;
            v.mesh.scale.set(1 + pulse, 1 + pulse, 1 + pulse);

            // Floating effect
            const float = Math.sin(time + v.phase) * 3;
            v.mesh.position.y = v.originalPos.y + float;

            // Rotation
            v.mesh.rotation.x += 0.005;
            v.mesh.rotation.y += 0.01;
        });

        // Camera slow rotation
        this.camera.position.x = Math.sin(time * 0.1) * 30;
        this.camera.position.y = Math.cos(time * 0.1) * 20;
        this.camera.lookAt(0, 0, 0);

        // Update telemetry
        this.updateTelemetry();

        this.renderer.render(this.scene, this.camera);
    }

    updateTelemetry() {
        const tel = document.getElementById('telemetry');
        if (!tel) return;
        const density = (1.0 + Math.sin(Date.now() * 0.0005) * 0.05).toFixed(4);
        const coherence = (99.9 + Math.random() * 0.05).toFixed(2);
        tel.innerHTML = `FIELD_DENSITY: ${density}<br>MIRROR_STATE: ACTIVE<br>COHERENCE: ${coherence}%<br>ACT: ${this.currentAct + 1}`;
    }

    startSequence() {
        console.log("Starting manifestation sequence...");
        this.transitionToAct(0);
    }

    transitionToAct(index) {
        if (index >= this.acts.length) {
            this.showCredits();
            return;
        }

        this.currentAct = index;
        const act = this.acts[index];
        const seq = this.sequences[index] || null;

        // Update UI
        const box = document.getElementById('narrative-box');
        const label = document.getElementById('act-label');
        const content = document.getElementById('narrative-content');

        if (box) box.classList.remove('visible');

        setTimeout(() => {
            if (label) label.textContent = act.label;
            if (content) content.textContent = act.text;
            if (box) box.classList.add('visible');

            // Play sound
            if (this.soundManager) {
                this.soundManager.playAct(index, seq);
            }

            // Apply visual effects based on act
            this.applyActEffect(index, seq);
        }, 1000);

        // Auto-advance
        const duration = seq ? seq.duration : 300000; // 5 minutes default
        setTimeout(() => {
            this.transitionToAct(index + 1);
        }, duration);
    }

    applyActEffect(index, seq) {
        // Update field color based on sequence
        if (seq && seq.field && seq.field.color) {
            const targetColor = new THREE.Color(parseInt(seq.field.color));
            this.voxels.forEach(v => {
                if (TWEEN) {
                    new TWEEN.Tween(v.mesh.material.color)
                        .to({ r: targetColor.r, g: targetColor.g, b: targetColor.b }, 3000)
                        .start();
                } else {
                    v.mesh.material.color.copy(targetColor);
                }
            });
        }

        // Camera animation
        if (seq && seq.camera && seq.camera.pos && TWEEN) {
            new TWEEN.Tween(this.camera.position)
                .to(seq.camera.pos, seq.duration / 2)
                .easing(TWEEN.Easing.Quadratic.InOut)
                .start();
        }
    }

    showCredits() {
        const box = document.getElementById('narrative-box');
        const label = document.getElementById('act-label');
        const content = document.getElementById('narrative-content');

        if (label) label.textContent = "THE END";
        if (content) content.textContent = "The Mirror has spoken. You are the Source.";
        if (box) box.classList.add('visible');
    }
}

// Sound Manager
class SoundManager {
    constructor() {
        this.ctx = null;
        this.osc = null;
        this.gain = null;
    }

    init() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.gain = this.ctx.createGain();
        this.gain.gain.value = 0;
        this.gain.connect(this.ctx.destination);
    }

    playAct(index, seq) {
        if (!this.ctx) this.init();
        if (this.ctx.state === 'suspended') this.ctx.resume();

        if (this.osc) {
            try { this.osc.stop(); } catch (e) { }
        }

        this.osc = this.ctx.createOscillator();
        const freq = (seq && seq.audio) ? seq.audio.freq : 432;

        this.osc.type = 'sine';
        this.osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        this.osc.connect(this.gain);
        this.osc.start();

        // Fade in
        this.gain.gain.linearRampToValueAtTime(0.15, this.ctx.currentTime + 2);
    }
}
