/* ── Stars Background ────────────────────────────────────────────────── */
(function initStars() {
    const canvas = document.getElementById('stars-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let stars = [];
    const STAR_COUNT = 200;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        createStars();
    }

    function createStars() {
        stars = [];
        for (let i = 0; i < STAR_COUNT; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 1.5 + 0.3,
                speed: Math.random() * 0.3 + 0.05,
                brightness: Math.random(),
                phase: Math.random() * Math.PI * 2,
            });
        }
    }

    function draw(time) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        /* Nebula blobs */
        const nebulae = [
            { x: canvas.width * 0.2, y: canvas.height * 0.3, r: 200, color: 'rgba(120, 40, 180, 0.04)' },
            { x: canvas.width * 0.7, y: canvas.height * 0.6, r: 250, color: 'rgba(80, 20, 140, 0.035)' },
            { x: canvas.width * 0.5, y: canvas.height * 0.8, r: 180, color: 'rgba(160, 60, 220, 0.03)' },
        ];
        for (const n of nebulae) {
            const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r);
            grad.addColorStop(0, n.color);
            grad.addColorStop(1, 'transparent');
            ctx.fillStyle = grad;
            ctx.fillRect(n.x - n.r, n.y - n.r, n.r * 2, n.r * 2);
        }

        /* Stars */
        for (const s of stars) {
            const twinkle = 0.5 + 0.5 * Math.sin(time * 0.001 * s.speed * 5 + s.phase);
            const alpha = 0.3 + 0.7 * twinkle * s.brightness;
            const purpleness = s.brightness > 0.7 ? 40 : 0;
            ctx.fillStyle = `rgba(${220 + purpleness}, ${210 + purpleness}, 255, ${alpha})`;
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            ctx.fill();
        }

        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    requestAnimationFrame(draw);
})();


/* ── Scroll-based fade-in ────────────────────────────────────────────── */
(function initScrollReveal() {
    const observer = new IntersectionObserver(
        (entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            }
        },
        { threshold: 0.1 }
    );

    const targets = document.querySelectorAll(
        '.feature-card, .preview-card, .version-card, .step'
    );
    targets.forEach((el) => observer.observe(el));
})();


/* ── Preview Canvas Renderers ────────────────────────────────────────── */
(function initPreviews() {
    /* Helper: create a <canvas> filling the parent */
    function makeCanvas(parentId) {
        const parent = document.getElementById(parentId);
        if (!parent) return null;
        const c = document.createElement('canvas');
        c.width = 400;
        c.height = 200;
        c.style.width = '100%';
        c.style.height = '100%';
        c.style.imageRendering = 'pixelated';
        parent.insertBefore(c, parent.firstChild);
        return c.getContext('2d');
    }

    /* Color constants */
    const PD = '#3c0a5a';
    const PM = '#7828b4';
    const PL = '#b464ff';
    const PG = '#c88cff';
    const GD = '#0f051e';

    /* Hearts preview */
    const heartsCtx = makeCanvas('preview-hearts');
    if (heartsCtx) {
        const c = heartsCtx;
        c.fillStyle = GD;
        c.fillRect(0, 0, 400, 200);

        /* Draw Minecraft-style hearts */
        for (let i = 0; i < 10; i++) {
            const hx = 40 + i * 32;
            const hy = 80;
            const s = 3; /* pixel scale */

            /* Heart shape (9x9 pattern) */
            const heart = [
                [0,1,1,0,0,0,1,1,0],
                [1,1,1,1,0,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [0,1,1,1,1,1,1,1,0],
                [0,0,1,1,1,1,1,0,0],
                [0,0,0,1,1,1,0,0,0],
                [0,0,0,0,1,0,0,0,0],
            ];

            for (let row = 0; row < heart.length; row++) {
                for (let col = 0; col < heart[row].length; col++) {
                    if (heart[row][col]) {
                        /* Highlight top-left */
                        if (row < 2 && col < 3) {
                            c.fillStyle = PG;
                        } else {
                            c.fillStyle = PM;
                        }
                        c.fillRect(hx + col * s, hy + row * s, s, s);
                    }
                }
            }
        }

        /* Label bg gradient */
        const grad = c.createLinearGradient(0, 170, 0, 200);
        grad.addColorStop(0, 'transparent');
        grad.addColorStop(1, 'rgba(15, 5, 30, 0.95)');
        c.fillStyle = grad;
        c.fillRect(0, 160, 400, 40);
    }

    /* Hotbar preview */
    const hotbarCtx = makeCanvas('preview-hotbar');
    if (hotbarCtx) {
        const c = hotbarCtx;
        c.fillStyle = GD;
        c.fillRect(0, 0, 400, 200);

        /* Hotbar background */
        const bx = 18;
        const by = 75;
        const bw = 364;
        const bh = 50;

        c.fillStyle = 'rgba(30, 8, 50, 0.85)';
        c.fillRect(bx, by, bw, bh);
        c.strokeStyle = PL;
        c.lineWidth = 2;
        c.strokeRect(bx, by, bw, bh);

        /* Slots */
        for (let i = 0; i < 9; i++) {
            const sx = bx + 4 + i * 40;
            const sy = by + 5;
            c.fillStyle = 'rgba(20, 5, 35, 0.8)';
            c.fillRect(sx, sy, 36, 40);
            c.strokeStyle = 'rgba(80, 30, 130, 0.6)';
            c.lineWidth = 1;
            c.strokeRect(sx, sy, 36, 40);
        }

        /* Selection highlight on slot 0 */
        c.strokeStyle = PG;
        c.lineWidth = 3;
        c.strokeRect(bx + 2, by + 3, 40, 44);
    }

    /* Inventory preview */
    const invCtx = makeCanvas('preview-inventory');
    if (invCtx) {
        const c = invCtx;

        /* Galaxy background */
        const grad = c.createLinearGradient(0, 0, 400, 200);
        grad.addColorStop(0, '#0f051e');
        grad.addColorStop(0.5, '#1a0a30');
        grad.addColorStop(1, '#0f051e');
        c.fillStyle = grad;
        c.fillRect(0, 0, 400, 200);

        /* Stars */
        for (let i = 0; i < 60; i++) {
            const sx = Math.random() * 400;
            const sy = Math.random() * 200;
            const sr = Math.random() * 1.5 + 0.3;
            c.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.3})`;
            c.beginPath();
            c.arc(sx, sy, sr, 0, Math.PI * 2);
            c.fill();
        }

        /* Nebula */
        const ngrad = c.createRadialGradient(200, 100, 0, 200, 100, 120);
        ngrad.addColorStop(0, 'rgba(120, 40, 180, 0.15)');
        ngrad.addColorStop(1, 'transparent');
        c.fillStyle = ngrad;
        c.fillRect(0, 0, 400, 200);

        /* Inventory frame */
        c.fillStyle = 'rgba(15, 5, 30, 0.6)';
        c.fillRect(50, 20, 300, 160);
        c.strokeStyle = PL;
        c.lineWidth = 2;
        c.strokeRect(50, 20, 300, 160);

        /* Slots grid */
        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 9; col++) {
                const sx = 62 + col * 30;
                const sy = 80 + row * 28;
                c.fillStyle = 'rgba(25, 8, 40, 0.8)';
                c.fillRect(sx, sy, 24, 24);
                c.strokeStyle = 'rgba(80, 30, 130, 0.6)';
                c.lineWidth = 1;
                c.strokeRect(sx, sy, 24, 24);
            }
        }
    }

    /* Crosshair preview */
    const crossCtx = makeCanvas('preview-crosshair');
    if (crossCtx) {
        const c = crossCtx;

        /* Fake game background */
        const grad = c.createLinearGradient(0, 0, 0, 200);
        grad.addColorStop(0, '#2a1050');
        grad.addColorStop(1, '#1a0830');
        c.fillStyle = grad;
        c.fillRect(0, 0, 400, 200);

        /* Ground blocks */
        for (let bx = 0; bx < 25; bx++) {
            const shade = 40 + Math.random() * 30;
            c.fillStyle = `rgb(${shade + 40}, ${shade - 10}, ${shade + 60})`;
            c.fillRect(bx * 16, 160, 16, 40);
        }

        /* Crosshair */
        const cx = 200;
        const cy = 90;
        const r = 20;

        c.strokeStyle = 'rgba(180, 100, 255, 0.6)';
        c.lineWidth = 2;
        c.beginPath();
        c.arc(cx, cy, r, 0, Math.PI * 2);
        c.stroke();

        /* Faint fill */
        c.fillStyle = 'rgba(160, 80, 220, 0.12)';
        c.beginPath();
        c.arc(cx, cy, r - 2, 0, Math.PI * 2);
        c.fill();

        /* Cross lines */
        c.strokeStyle = 'rgba(180, 100, 255, 0.5)';
        c.lineWidth = 1;
        c.beginPath();
        c.moveTo(cx - 8, cy);
        c.lineTo(cx + 8, cy);
        c.moveTo(cx, cy - 8);
        c.lineTo(cx, cy + 8);
        c.stroke();

        /* Center dot */
        c.fillStyle = 'rgba(200, 140, 255, 0.8)';
        c.beginPath();
        c.arc(cx, cy, 2, 0, Math.PI * 2);
        c.fill();
    }

    /* Items preview */
    const itemsCtx = makeCanvas('preview-items');
    if (itemsCtx) {
        const c = itemsCtx;
        c.fillStyle = GD;
        c.fillRect(0, 0, 400, 200);

        /* Draw simplified purple items */
        const items = [
            { x: 40, y: 60, type: 'sword' },
            { x: 110, y: 60, type: 'pickaxe' },
            { x: 180, y: 60, type: 'gem' },
            { x: 250, y: 60, type: 'potion' },
            { x: 320, y: 60, type: 'apple' },
        ];

        for (const item of items) {
            const s = 4;
            c.save();
            c.translate(item.x, item.y);

            if (item.type === 'sword') {
                /* Purple sword */
                c.fillStyle = '#6e3810';
                c.fillRect(1*s, 11*s, s, s);
                c.fillRect(2*s, 10*s, s, s);
                c.fillStyle = PD;
                c.fillRect(1*s, 9*s, 4*s, s);
                c.fillStyle = PM;
                c.fillRect(3*s, 8*s, s, s);
                c.fillRect(4*s, 7*s, s, s);
                c.fillStyle = PL;
                c.fillRect(5*s, 6*s, s, s);
                c.fillRect(6*s, 5*s, s, s);
                c.fillRect(7*s, 4*s, s, s);
                c.fillStyle = PG;
                c.fillRect(8*s, 3*s, s, s);
                c.fillRect(9*s, 2*s, s, s);
            } else if (item.type === 'pickaxe') {
                c.fillStyle = '#6e3810';
                c.fillRect(2*s, 10*s, s, s);
                c.fillRect(3*s, 9*s, s, s);
                c.fillRect(4*s, 8*s, s, s);
                c.fillRect(5*s, 7*s, s, s);
                c.fillStyle = PM;
                c.fillRect(4*s, 3*s, s, s);
                c.fillRect(5*s, 2*s, s, s);
                c.fillRect(6*s, 1*s, s, s);
                c.fillRect(7*s, 2*s, s, s);
                c.fillRect(8*s, 3*s, s, s);
                c.fillStyle = PG;
                c.fillRect(5*s, 3*s, s, s);
                c.fillRect(6*s, 2*s, s, s);
                c.fillRect(7*s, 3*s, s, s);
            } else if (item.type === 'gem') {
                c.fillStyle = PM;
                c.fillRect(3*s, 3*s, 6*s, s);
                c.fillRect(2*s, 4*s, 8*s, s);
                c.fillRect(2*s, 5*s, 8*s, s);
                c.fillRect(3*s, 6*s, 6*s, s);
                c.fillRect(4*s, 7*s, 4*s, s);
                c.fillRect(5*s, 8*s, 2*s, s);
                c.fillStyle = PG;
                c.fillRect(3*s, 4*s, 3*s, 2*s);
            } else if (item.type === 'potion') {
                c.fillStyle = '#8c6428';
                c.fillRect(4*s, 0*s, 4*s, 2*s);
                c.fillStyle = 'rgba(200, 170, 230, 0.7)';
                c.fillRect(4*s, 2*s, 4*s, 3*s);
                c.fillRect(2*s, 5*s, 8*s, 6*s);
                c.fillStyle = PM;
                c.fillRect(3*s, 7*s, 6*s, 3*s);
            } else if (item.type === 'apple') {
                c.fillStyle = '#503214';
                c.fillRect(5*s, 0*s, s, 2*s);
                c.fillStyle = '#6428a0';
                c.fillRect(4*s, 0*s, s, 2*s);
                c.fillStyle = PM;
                c.fillRect(3*s, 2*s, 6*s, s);
                c.fillRect(2*s, 3*s, 8*s, 4*s);
                c.fillRect(3*s, 7*s, 6*s, 2*s);
                c.fillRect(4*s, 9*s, 4*s, s);
                c.fillStyle = PG;
                c.fillRect(3*s, 3*s, 2*s, 2*s);
            }

            c.restore();
        }

        /* Labels under items */
        c.font = '11px sans-serif';
        c.fillStyle = PG;
        c.textAlign = 'center';
        const labels = ['Schwert', 'Spitzhacke', 'Diamant', 'Trank', 'Apfel'];
        items.forEach((item, i) => {
            c.fillText(labels[i], item.x + 20, item.y + 56);
        });
    }

    /* Sky preview */
    const skyCtx = makeCanvas('preview-sky');
    if (skyCtx) {
        const c = skyCtx;

        /* Purple sky gradient */
        const grad = c.createLinearGradient(0, 0, 0, 200);
        grad.addColorStop(0, '#280a50');
        grad.addColorStop(0.4, '#501a80');
        grad.addColorStop(0.7, '#6432a0');
        grad.addColorStop(1, '#1a0830');
        c.fillStyle = grad;
        c.fillRect(0, 0, 400, 200);

        /* Stars */
        for (let i = 0; i < 80; i++) {
            const sx = Math.random() * 400;
            const sy = Math.random() * 140;
            const sr = Math.random() * 1.2 + 0.3;
            c.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.6 + 0.2})`;
            c.beginPath();
            c.arc(sx, sy, sr, 0, Math.PI * 2);
            c.fill();
        }

        /* Nebula */
        const ngrad = c.createRadialGradient(280, 60, 0, 280, 60, 100);
        ngrad.addColorStop(0, 'rgba(180, 80, 255, 0.12)');
        ngrad.addColorStop(1, 'transparent');
        c.fillStyle = ngrad;
        c.fillRect(0, 0, 400, 200);

        /* Moon */
        c.fillStyle = 'rgba(200, 170, 230, 0.9)';
        c.beginPath();
        c.arc(100, 50, 18, 0, Math.PI * 2);
        c.fill();
        c.fillStyle = 'rgba(170, 140, 200, 0.7)';
        c.beginPath();
        c.arc(97, 47, 4, 0, Math.PI * 2);
        c.fill();
        c.beginPath();
        c.arc(105, 54, 3, 0, Math.PI * 2);
        c.fill();

        /* Ground silhouette */
        c.fillStyle = '#0a0418';
        c.beginPath();
        c.moveTo(0, 180);
        for (let gx = 0; gx <= 400; gx += 16) {
            c.lineTo(gx, 160 + Math.sin(gx * 0.05) * 10 + Math.random() * 5);
        }
        c.lineTo(400, 200);
        c.lineTo(0, 200);
        c.closePath();
        c.fill();
    }
})();


/* ── Smooth scroll for nav links ─────────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
