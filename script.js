/* ==================================================================
   DNA · CODE OF LIFE — INTERACTIVITY
   Heavy on animations. Every letter has a color, every click has a sound.
   ================================================================== */

/* ==============================================================
   0. AUDIO — Web Audio API synthesizer (no assets needed)
   Generates tiny sound effects from oscillators so the page is
   fully self-contained.
   ============================================================== */
const Sound = (() => {
  let ctx = null;
  let enabled = true;

  function ensure() {
    if (!ctx) {
      try {
        ctx = new (window.AudioContext || window.webkitAudioContext)();
      } catch (e) {}
    }
    if (ctx && ctx.state === 'suspended') ctx.resume();
  }

  function tone(freq, duration = 0.12, type = 'square', volume = 0.06) {
    if (!enabled) return;
    ensure();
    if (!ctx) return;
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = type;
    o.frequency.value = freq;
    g.gain.value = volume;
    o.connect(g).connect(ctx.destination);
    const now = ctx.currentTime;
    g.gain.setValueAtTime(volume, now);
    g.gain.exponentialRampToValueAtTime(0.0001, now + duration);
    o.start(now);
    o.stop(now + duration);
  }

  function sequence(notes, gap = 0.12, type = 'square') {
    if (!enabled) return;
    notes.forEach((n, i) => setTimeout(() => tone(n, gap * 0.9, type), i * gap * 1000));
  }

  return {
    click:    () => tone(880, 0.05, 'square', 0.04),
    hover:    () => tone(660, 0.04, 'sine', 0.03),
    correct:  () => sequence([523, 659, 784], 0.1, 'triangle'),
    wrong:    () => sequence([196, 147], 0.13, 'sawtooth'),
    bond:     () => tone(1046, 0.08, 'sine', 0.05),
    energy:   () => tone(1318, 0.1, 'triangle', 0.05),
    whoosh:   () => tone(220, 0.2, 'sine', 0.04),
    levelup:  () => sequence([523, 659, 784, 1046], 0.09, 'triangle'),
    letterA:  () => tone(440, 0.08, 'square', 0.04),
    letterT:  () => tone(523, 0.08, 'square', 0.04),
    letterC:  () => tone(659, 0.08, 'square', 0.04),
    letterG:  () => tone(784, 0.08, 'square', 0.04),
    letterU:  () => tone(880, 0.08, 'square', 0.04),
    toggle(state) { enabled = state; },
    isEnabled: () => enabled
  };
})();

/* ==============================================================
   1. LOADING SCREEN + entry
   ============================================================== */
window.addEventListener('load', () => {
  setTimeout(() => {
    document.getElementById('loader').classList.add('done');
    Sound.levelup();
  }, 1400);
});

/* ==============================================================
   2. SOUND TOGGLE
   ============================================================== */
const soundBtn = document.getElementById('sound-toggle');
const soundLabel = document.getElementById('sound-label');
const soundIcon = document.getElementById('sound-icon');
let soundOn = true;
soundBtn.addEventListener('click', () => {
  soundOn = !soundOn;
  Sound.toggle(soundOn);
  soundLabel.textContent = 'SOUND: ' + (soundOn ? 'ON' : 'OFF');
  soundIcon.textContent = soundOn ? '♪' : '♫';
  if (soundOn) Sound.click();
});

/* ==============================================================
   3. CURSOR — dot + ring + particle trail
   ============================================================== */
const dot = document.createElement('div');
dot.className = 'cursor-dot';
const ring = document.createElement('div');
ring.className = 'cursor-ring';
document.body.appendChild(dot);
document.body.appendChild(ring);

let mouseX = innerWidth/2, mouseY = innerHeight/2;
let ringX = mouseX, ringY = mouseY;

document.addEventListener('mousemove', e => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  dot.style.transform = `translate(${mouseX - 5}px, ${mouseY - 5}px)`;
});

function animateRing() {
  ringX += (mouseX - ringX) * 0.18;
  ringY += (mouseY - ringY) * 0.18;
  ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;
  requestAnimationFrame(animateRing);
}
animateRing();

// Pointer state on interactive elements
document.querySelectorAll('a, button, .amino-card, .letter-cell, .dpad-btn, .btn-a, .btn-b').forEach(el => {
  el.addEventListener('mouseenter', () => { dot.classList.add('pointer'); ring.classList.add('pointer'); Sound.hover(); });
  el.addEventListener('mouseleave', () => { dot.classList.remove('pointer'); ring.classList.remove('pointer'); });
});

/* Cursor trail canvas — draws fading nucleotide letters */
const trail = document.getElementById('cursor-trail');
const tctx = trail.getContext('2d');
function sizeTrail() { trail.width = innerWidth; trail.height = innerHeight; }
sizeTrail();
window.addEventListener('resize', sizeTrail);

const trailParticles = [];
const trailColors = ['#ff3b4c', '#3277ff', '#30d68a', '#ffd23b', '#b44dff'];
const trailLetters = ['A', 'T', 'C', 'G', 'U'];

document.addEventListener('mousemove', e => {
  if (Math.random() < 0.4) {
    const idx = Math.floor(Math.random() * 5);
    trailParticles.push({
      x: e.clientX, y: e.clientY,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2 - 0.5,
      letter: trailLetters[idx],
      color: trailColors[idx],
      life: 1,
      size: 10 + Math.random() * 8
    });
  }
});

function drawTrail() {
  tctx.clearRect(0, 0, trail.width, trail.height);
  for (let i = trailParticles.length - 1; i >= 0; i--) {
    const p = trailParticles[i];
    p.x += p.vx; p.y += p.vy;
    p.life -= 0.02;
    if (p.life <= 0) { trailParticles.splice(i, 1); continue; }
    tctx.globalAlpha = p.life;
    tctx.fillStyle = p.color;
    tctx.font = `bold ${p.size}px "Press Start 2P", monospace`;
    tctx.fillText(p.letter, p.x, p.y);
  }
  tctx.globalAlpha = 1;
  requestAnimationFrame(drawTrail);
}
drawTrail();

/* ==============================================================
   4. FLOATING BACKGROUND PARTICLES (letters drifting up)
   ============================================================== */
const particlesRoot = document.getElementById('particles');
const palette = {
  A: '#ff3b4c', T: '#3277ff', C: '#30d68a', G: '#ffd23b', U: '#b44dff'
};
function spawnParticle() {
  const letters = Object.keys(palette);
  const l = letters[Math.floor(Math.random() * letters.length)];
  const el = document.createElement('div');
  el.className = 'particle';
  el.textContent = l;
  el.style.color = palette[l];
  el.style.left = Math.random() * 100 + '%';
  el.style.fontSize = (12 + Math.random() * 20) + 'px';
  el.style.animationDuration = (12 + Math.random() * 18) + 's';
  el.style.animationDelay = (-Math.random() * 20) + 's';
  particlesRoot.appendChild(el);
  setTimeout(() => el.remove(), 30000);
}
for (let i = 0; i < 35; i++) spawnParticle();
setInterval(spawnParticle, 1000);

/* ==============================================================
   5. HERO CANVAS — rotating DNA double helix
   ============================================================== */
const dnaCanvas = document.getElementById('dna-canvas');
const dctx = dnaCanvas.getContext('2d');
function sizeDNA() {
  dnaCanvas.width = dnaCanvas.offsetWidth * devicePixelRatio;
  dnaCanvas.height = dnaCanvas.offsetHeight * devicePixelRatio;
  dctx.scale(devicePixelRatio, devicePixelRatio);
}
sizeDNA();
window.addEventListener('resize', () => {
  dnaCanvas.width = dnaCanvas.offsetWidth * devicePixelRatio;
  dnaCanvas.height = dnaCanvas.offsetHeight * devicePixelRatio;
});

const dnaPairs = [
  ['A', 'T'], ['G', 'C'], ['T', 'A'], ['C', 'G'],
  ['A', 'T'], ['T', 'A'], ['G', 'C'], ['C', 'G'],
  ['T', 'A'], ['A', 'T'], ['C', 'G'], ['G', 'C'],
  ['A', 'T'], ['T', 'A'], ['G', 'C'], ['A', 'T']
];

let dnaRotation = 0;
let scrollOffset = 0;
window.addEventListener('scroll', () => {
  scrollOffset = window.scrollY;
});

function drawHelix() {
  const w = dnaCanvas.offsetWidth;
  const h = dnaCanvas.offsetHeight;
  dctx.clearRect(0, 0, w, h);

  const cx = w / 2;
  const amplitude = Math.min(w, 400) * 0.25;
  const spacing = h / (dnaPairs.length - 1);

  dnaRotation += 0.015;
  const scrollTwist = scrollOffset * 0.005;

  // Backbones first
  dctx.lineWidth = 3;
  for (let strand = 0; strand < 2; strand++) {
    dctx.beginPath();
    for (let i = 0; i < dnaPairs.length; i++) {
      const y = i * spacing;
      const phase = i * 0.5 + dnaRotation + scrollTwist + (strand ? Math.PI : 0);
      const x = cx + Math.sin(phase) * amplitude;
      if (i === 0) dctx.moveTo(x, y);
      else dctx.lineTo(x, y);
    }
    const grad = dctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, strand ? '#3277ff' : '#ff3b4c');
    grad.addColorStop(1, strand ? '#b44dff' : '#30d68a');
    dctx.strokeStyle = grad;
    dctx.stroke();
  }

  // Rungs and bases
  for (let i = 0; i < dnaPairs.length; i++) {
    const y = i * spacing;
    const phase = i * 0.5 + dnaRotation + scrollTwist;
    const x1 = cx + Math.sin(phase) * amplitude;
    const x2 = cx + Math.sin(phase + Math.PI) * amplitude;
    const depth = Math.cos(phase);

    // Hydrogen-bond rung
    dctx.beginPath();
    dctx.strokeStyle = `rgba(255,255,255,${0.15 + 0.3 * Math.abs(depth)})`;
    dctx.lineWidth = 2;
    dctx.setLineDash([4, 4]);
    dctx.moveTo(x1, y);
    dctx.lineTo(x2, y);
    dctx.stroke();
    dctx.setLineDash([]);

    // Base circles — scale with depth to fake 3D
    const [b1, b2] = dnaPairs[i];
    const r1 = 9 + 4 * depth;
    const r2 = 9 - 4 * depth;

    drawBase(x1, y, r1, b1);
    drawBase(x2, y, r2, b2);
  }
}

function drawBase(x, y, r, letter) {
  if (r <= 1) return;
  dctx.beginPath();
  dctx.arc(x, y, Math.abs(r), 0, Math.PI * 2);
  dctx.fillStyle = palette[letter];
  dctx.shadowColor = palette[letter];
  dctx.shadowBlur = 12;
  dctx.fill();
  dctx.shadowBlur = 0;
  dctx.fillStyle = '#fff';
  dctx.font = `bold ${Math.max(9, r)}px "Press Start 2P", monospace`;
  dctx.textAlign = 'center';
  dctx.textBaseline = 'middle';
  dctx.fillText(letter, x, y + 1);
}

function loopHelix() {
  drawHelix();
  requestAnimationFrame(loopHelix);
}
loopHelix();

/* ==============================================================
   6. SCROLL REVEALS
   ============================================================== */
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      if (e.target.classList.contains('section-heading')) Sound.whoosh();
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

/* ==============================================================
   7. NAV scroll state
   ============================================================== */
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

/* ==============================================================
   8. PARALLAX background in DNA section
   ============================================================== */
const parallax = document.querySelector('.parallax-bg');
window.addEventListener('scroll', () => {
  if (!parallax) return;
  const rect = parallax.getBoundingClientRect();
  const offset = (rect.top - innerHeight / 2) * 0.25;
  parallax.style.transform = `translateY(${offset}px)`;
});

/* ==============================================================
   9. BUILD THE LETTER GRID (16 cols × N rows of A/T/C/G/U)
   ============================================================== */
(function buildLetterGrid() {
  const grid = document.getElementById('letter-grid');
  const letters = ['A', 'T', 'C', 'G', 'U'];
  const cols = 16, rows = 6;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const letter = letters[Math.floor(Math.random() * letters.length)];
      const cell = document.createElement('div');
      cell.className = 'letter-cell ' + letter;
      cell.textContent = letter;
      cell.style.animationDelay = ((r * cols + c) * 0.015) + 's';
      cell.addEventListener('click', () => {
        Sound['letter' + letter]();
        cell.style.transform = 'translateZ(60px) rotateY(180deg) scale(1.3)';
        setTimeout(() => { cell.style.transform = ''; }, 400);
      });
      cell.addEventListener('mouseenter', () => Sound['letter' + letter]());
      grid.appendChild(cell);
    }
  }
})();

/* ==============================================================
  10. HELIX DEMO IN DNA SECTION
   ============================================================== */
(function buildHelixDemo() {
  const root = document.getElementById('helix-demo');
  if (!root) return;
  const seq = ['A','T','G','C','T','A','C','G','A','T','G','C'];
  const pair = { A:'T', T:'A', C:'G', G:'C' };
  const total = seq.length;
  seq.forEach((b, i) => {
    const rung = document.createElement('div');
    rung.className = 'helix-rung';
    const phase = i / total * Math.PI * 4;
    const y = 10 + i * 28;
    rung.style.top = y + 'px';
    rung.style.transform = `rotateZ(0deg) scaleX(${Math.abs(Math.cos(phase)) * 0.5 + 0.5})`;
    rung.innerHTML = `
      <div class="helix-base ${b}">${b}</div>
      <div class="helix-bond"></div>
      <div class="helix-base ${pair[b]}">${pair[b]}</div>
    `;
    rung.addEventListener('mouseenter', () => Sound.bond());
    root.appendChild(rung);
  });
  // Scroll-driven rotation
  window.addEventListener('scroll', () => {
    const rect = root.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > innerHeight) return;
    const t = (innerHeight - rect.top) / (innerHeight + rect.height);
    root.querySelectorAll('.helix-rung').forEach((rung, i) => {
      const phase = i * 0.4 + t * Math.PI * 3;
      rung.style.transform = `scaleX(${Math.abs(Math.cos(phase)) * 0.7 + 0.3})`;
    });
  });
})();

/* ==============================================================
  11. BUILD mRNA MAZE (visual only, animated)
   ============================================================== */
(function buildMaze() {
  const maze = document.getElementById('maze-grid');
  if (!maze) return;
  // Simple 10x10 layout: wall=W, empty=., enzyme=E, energy=$, goal=G, mrna=M
  const layout = [
    'M.........',
    'W.WW.WWWWW',
    'W..W..E..W',
    '.EW.WWWW.W',
    '.$W......W',
    '.W.WWWWW.W',
    '.W.W.E.W.W',
    '.W.W.$.W.W',
    '.W.WWW.W..',
    '.........G'
  ];
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 10; c++) {
      const cell = document.createElement('div');
      cell.className = 'maze-cell';
      const ch = layout[r][c];
      if (ch === 'W') cell.classList.add('wall');
      if (ch === 'E') cell.classList.add('enzyme');
      if (ch === '$') cell.classList.add('energy');
      if (ch === 'G') cell.classList.add('goal');
      if (ch === 'M') cell.classList.add('mrna');
      maze.appendChild(cell);
    }
  }

  // Animate mRNA "player" moving along a path
  const mrnaCell = maze.querySelector('.mrna');
  const path = [
    [0,0],[0,1],[0,2],[0,3],[0,4],[1,4],[2,4],[2,5],[3,5],[3,6],[3,7],
    [4,7],[5,7],[6,7],[7,7],[8,7],[8,8],[8,9],[9,9]
  ];
  let idx = 0;
  function step() {
    maze.querySelectorAll('.mrna').forEach(c => c.classList.remove('mrna'));
    const [r, c] = path[idx % path.length];
    const cells = maze.children;
    const target = cells[r * 10 + c];
    target.classList.add('mrna');
    idx++;
    if (target.classList.contains('energy')) Sound.energy();
  }
  setInterval(step, 600);
})();

/* ==============================================================
  12. CODON / AMINO-ACID INTERACTION
   ============================================================== */
document.querySelectorAll('.amino-card').forEach(card => {
  card.addEventListener('click', () => {
    const isCorrect = card.hasAttribute('data-correct');
    card.classList.remove('correct', 'wrong');
    // Reflow to retrigger animation
    void card.offsetWidth;
    if (isCorrect) {
      card.classList.add('correct');
      Sound.correct();
    } else {
      card.classList.add('wrong');
      Sound.wrong();
    }
    setTimeout(() => card.classList.remove('correct', 'wrong'), 600);
  });
});

/* ==============================================================
  13. CELL HEALTH DEMO
   ============================================================== */
(function healthDemo() {
  let health = 100;
  const fill = document.querySelector('.health-bar-fill');
  const num = document.getElementById('health-num');
  const dmg = document.getElementById('damage-btn');
  const heal = document.getElementById('heal-btn');
  const cell = document.querySelector('.cell-org');

  function update() {
    fill.style.width = health + '%';
    num.textContent = health;
    if (health < 30) {
      cell.style.animationDuration = '0.8s';
      cell.style.borderColor = 'var(--c-a)';
    } else {
      cell.style.animationDuration = '3s';
      cell.style.borderColor = 'rgba(124, 249, 255, 0.3)';
    }
  }

  dmg.addEventListener('click', () => {
    health = Math.max(0, health - 15);
    update();
    Sound.wrong();
    cell.animate([
      { transform: 'scale(1)' }, { transform: 'scale(1.1) translateX(-6px)' },
      { transform: 'scale(1) translateX(6px)' }, { transform: 'scale(1)' }
    ], { duration: 400 });
    if (health <= 0) {
      Sound.whoosh();
      setTimeout(() => { health = 100; update(); }, 1000);
    }
  });
  heal.addEventListener('click', () => {
    health = Math.min(100, health + 10);
    update();
    Sound.correct();
  });
})();

/* ==============================================================
  14. TITLE WORD HOVER GLITCH
   ============================================================== */
document.querySelectorAll('.title-word').forEach(w => {
  w.addEventListener('mouseenter', () => {
    Sound.click();
    const orig = w.textContent;
    const chars = 'ATCGU';
    let i = 0;
    const iv = setInterval(() => {
      w.textContent = orig.split('').map(c =>
        Math.random() < 0.5 ? chars[Math.floor(Math.random() * 5)] : c
      ).join('');
      i++;
      if (i > 6) { clearInterval(iv); w.textContent = orig; }
    }, 40);
  });
});

/* ==============================================================
  15. GAMEPAD BUTTON SOUNDS
   ============================================================== */
document.querySelectorAll('.dpad-btn').forEach(b => b.addEventListener('click', Sound.click));
document.querySelector('.btn-a').addEventListener('click', () => Sound.correct());
document.querySelector('.btn-b').addEventListener('click', () => Sound.bond());

/* ==============================================================
  16. POLYMERASE DROPLET — click anywhere in track to test
   ============================================================== */
const polyTrack = document.querySelector('.poly-track');
if (polyTrack) {
  polyTrack.addEventListener('click', e => {
    const rect = polyTrack.getBoundingClientRect();
    const dropletEl = document.getElementById('poly-droplet');
    const dropletRect = dropletEl.getBoundingClientRect();
    const dropletCenter = dropletRect.left + dropletRect.width / 2;
    const promoter = polyTrack.querySelector('.poly-promoter').getBoundingClientRect();
    if (dropletCenter > promoter.left && dropletCenter < promoter.right) {
      Sound.correct();
      dropletEl.animate([
        { transform: 'scale(1)', filter: 'hue-rotate(0deg)' },
        { transform: 'scale(2)', filter: 'hue-rotate(180deg)' },
        { transform: 'scale(1)', filter: 'hue-rotate(0deg)' }
      ], { duration: 600 });
    } else {
      Sound.wrong();
    }
  });
}

/* ==============================================================
  17. KEEP AUDIO CTX LIVE ON FIRST USER GESTURE
   ============================================================== */
document.addEventListener('click', () => Sound.click(), { once: true });
document.addEventListener('keydown', () => Sound.click(), { once: true });

console.log('%cDNA · CODE OF LIFE loaded.', 'color:#7cf9ff;font-weight:bold;font-size:14px;');
console.log('%cEvery nucleotide is a color. Every interaction is a sound.', 'color:#b44dff;');
