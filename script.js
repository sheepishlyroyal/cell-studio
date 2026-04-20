/* ==================================================================
   CELL STUDIO — DNA: CODE OF LIFE
   Interactivity for the landing page.
   ================================================================== */

/* ==============================================================
   0. AUDIO — Web Audio API synthesizer
   ============================================================== */
const Sound = (() => {
  let ctx = null;
  let enabled = true;

  function ensure() {
    if (!ctx) {
      try { ctx = new (window.AudioContext || window.webkitAudioContext)(); }
      catch (e) {}
    }
    if (ctx && ctx.state === 'suspended') ctx.resume();
  }

  function tone(freq, duration = 0.12, type = 'square', volume = 0.05) {
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

  function sequence(notes, gap = 0.1, type = 'square') {
    if (!enabled) return;
    notes.forEach((n, i) => setTimeout(() => tone(n, gap * 0.9, type), i * gap * 1000));
  }

  return {
    click:    () => tone(880, 0.05, 'square', 0.03),
    correct:  () => sequence([523, 659, 784], 0.1, 'triangle'),
    wrong:    () => sequence([196, 147], 0.13, 'sawtooth'),
    bond:     () => tone(1046, 0.08, 'sine', 0.04),
    energy:   () => tone(1318, 0.1, 'triangle', 0.04),
    whoosh:   () => tone(220, 0.2, 'sine', 0.03),
    levelup:  () => sequence([523, 659, 784, 1046], 0.09, 'triangle'),
    glitch:   () => tone(200 + Math.random() * 800, 0.03, 'square', 0.02),
    toggle(state) { enabled = state; },
    isEnabled: () => enabled
  };
})();

/* ==============================================================
   1. LOADING SCREEN
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
  soundLabel.textContent = 'SOUND ' + (soundOn ? 'ON' : 'OFF');
  soundIcon.textContent = soundOn ? '♪' : '♫';
  if (soundOn) Sound.click();
});
document.addEventListener('click', () => Sound.click(), { once: true });

/* ==============================================================
   3. SCROLL PROGRESS BAR
   ============================================================== */
const progress = document.getElementById('scroll-progress');
window.addEventListener('scroll', () => {
  const h = document.documentElement;
  const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
  progress.style.width = pct + '%';
});

/* ==============================================================
   4. FLOATING BACKGROUND PARTICLES
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
  el.style.fontSize = (10 + Math.random() * 18) + 'px';
  el.style.animationDuration = (14 + Math.random() * 20) + 's';
  el.style.animationDelay = (-Math.random() * 20) + 's';
  particlesRoot.appendChild(el);
  setTimeout(() => el.remove(), 35000);
}
for (let i = 0; i < 30; i++) spawnParticle();
setInterval(spawnParticle, 1200);

/* ==============================================================
   5. THREE.JS — 3D DNA HELIX (longer, rotating, scroll-aware)
   ============================================================== */
(function initThreeDNA() {
  const mount = document.getElementById('three-dna');
  if (!mount || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x05060d, 40, 140);

  const camera = new THREE.PerspectiveCamera(55, mount.clientWidth / mount.clientHeight, 0.1, 500);
  camera.position.set(0, 0, 55);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(mount.clientWidth, mount.clientHeight);
  renderer.setClearColor(0x000000, 0);
  mount.appendChild(renderer.domElement);

  // Lights
  scene.add(new THREE.AmbientLight(0x8899ff, 0.6));
  const dir1 = new THREE.DirectionalLight(0xffffff, 0.8);
  dir1.position.set(20, 20, 30);
  scene.add(dir1);
  const dir2 = new THREE.PointLight(0x7cf9ff, 1.2, 120);
  dir2.position.set(-20, 10, 10);
  scene.add(dir2);
  const dir3 = new THREE.PointLight(0xb44dff, 1.0, 120);
  dir3.position.set(20, -20, 10);
  scene.add(dir3);

  // DNA container — long and twisting
  const dna = new THREE.Group();
  scene.add(dna);

  const PAIR_COUNT = 64;          // length of the strand
  const HELIX_RADIUS = 6;
  const PAIR_SPACING = 1.4;
  const TWIST_PER_PAIR = Math.PI / 5;
  const totalHeight = PAIR_COUNT * PAIR_SPACING;

  const colors = {
    A: 0xff3b4c, T: 0x3277ff, C: 0x30d68a, G: 0xffd23b
  };
  const pairs = [
    ['A','T'], ['G','C'], ['T','A'], ['C','G'],
    ['A','T'], ['T','A'], ['G','C'], ['C','G']
  ];

  const sphereGeo = new THREE.SphereGeometry(0.9, 20, 16);
  const backboneGeo = new THREE.SphereGeometry(0.35, 12, 10);
  const rungGeo = new THREE.CylinderGeometry(0.1, 0.1, HELIX_RADIUS * 2 - 1.8, 8);
  rungGeo.rotateZ(Math.PI / 2);

  for (let i = 0; i < PAIR_COUNT; i++) {
    const y = -totalHeight / 2 + i * PAIR_SPACING;
    const angle = i * TWIST_PER_PAIR;
    const [b1, b2] = pairs[i % pairs.length];

    // Rung (hydrogen bond)
    const rungMat = new THREE.MeshStandardMaterial({
      color: 0xffffff, transparent: true, opacity: 0.35,
      emissive: 0xffffff, emissiveIntensity: 0.1
    });
    const rung = new THREE.Mesh(rungGeo, rungMat);
    rung.position.set(0, y, 0);
    rung.rotation.y = angle;
    dna.add(rung);

    // Base 1
    const mat1 = new THREE.MeshStandardMaterial({
      color: colors[b1],
      emissive: colors[b1],
      emissiveIntensity: 0.6,
      roughness: 0.35,
      metalness: 0.1
    });
    const base1 = new THREE.Mesh(sphereGeo, mat1);
    base1.position.set(Math.cos(angle) * HELIX_RADIUS, y, Math.sin(angle) * HELIX_RADIUS);
    dna.add(base1);

    // Base 2
    const mat2 = new THREE.MeshStandardMaterial({
      color: colors[b2],
      emissive: colors[b2],
      emissiveIntensity: 0.6,
      roughness: 0.35,
      metalness: 0.1
    });
    const base2 = new THREE.Mesh(sphereGeo, mat2);
    base2.position.set(-Math.cos(angle) * HELIX_RADIUS, y, -Math.sin(angle) * HELIX_RADIUS);
    dna.add(base2);

    // Backbone beads between adjacent bases
    if (i > 0) {
      const prevAngle = (i - 1) * TWIST_PER_PAIR;
      const prevY = y - PAIR_SPACING;
      for (let t = 0; t < 6; t++) {
        const f = t / 6;
        const a = prevAngle + (angle - prevAngle) * f;
        const yy = prevY + PAIR_SPACING * f;
        const bbMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x444488, emissiveIntensity: 0.3, transparent: true, opacity: 0.5 });
        const bead1 = new THREE.Mesh(backboneGeo, bbMat);
        bead1.position.set(Math.cos(a) * HELIX_RADIUS, yy, Math.sin(a) * HELIX_RADIUS);
        dna.add(bead1);
        const bead2 = new THREE.Mesh(backboneGeo, bbMat);
        bead2.position.set(-Math.cos(a) * HELIX_RADIUS, yy, -Math.sin(a) * HELIX_RADIUS);
        dna.add(bead2);
      }
    }
  }

  // Floating label spheres representing free nucleotides
  const floaters = [];
  for (let i = 0; i < 20; i++) {
    const letters = Object.keys(colors);
    const l = letters[Math.floor(Math.random() * letters.length)];
    const mat = new THREE.MeshStandardMaterial({
      color: colors[l], emissive: colors[l], emissiveIntensity: 0.8,
      transparent: true, opacity: 0.8
    });
    const s = new THREE.Mesh(new THREE.SphereGeometry(0.5 + Math.random() * 0.6, 12, 10), mat);
    s.position.set(
      (Math.random() - 0.5) * 80,
      (Math.random() - 0.5) * totalHeight,
      (Math.random() - 0.5) * 40 - 20
    );
    s.userData = {
      vy: (Math.random() - 0.5) * 0.02,
      vx: (Math.random() - 0.5) * 0.02,
    };
    scene.add(s);
    floaters.push(s);
  }

  // Resize
  window.addEventListener('resize', () => {
    camera.aspect = mount.clientWidth / mount.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(mount.clientWidth, mount.clientHeight);
  });

  // Mouse parallax
  let mx = 0, my = 0;
  window.addEventListener('mousemove', e => {
    mx = (e.clientX / window.innerWidth - 0.5) * 2;
    my = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    lastScroll = window.scrollY;
  });

  // Animate
  const clock = new THREE.Clock();
  function animate() {
    const dt = clock.getDelta();
    const t = clock.getElapsedTime();
    // Keep constant auto-rotation
    dna.rotation.y += dt * 0.3;
    // Add scroll-driven twist
    dna.rotation.y += lastScroll * 0.00005;
    // Subtle floating bob
    dna.position.y = Math.sin(t * 0.6) * 0.6;
    // Tilt with pointer
    dna.rotation.z = mx * 0.15;
    dna.rotation.x = my * 0.1;

    // Floating bases
    floaters.forEach(f => {
      f.position.y += f.userData.vy;
      f.position.x += f.userData.vx;
      if (f.position.y > totalHeight / 2) f.position.y = -totalHeight / 2;
      if (f.position.y < -totalHeight / 2) f.position.y = totalHeight / 2;
    });

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  animate();
})();

/* ==============================================================
   6. SCROLL REVEALS + letter-by-letter heading split
   ============================================================== */
// Wrap each character of [data-split] headings in a .char span, then reveal
document.querySelectorAll('[data-split]').forEach(h => {
  const text = h.textContent;
  h.textContent = '';
  let delay = 0;
  for (const c of text) {
    const span = document.createElement('span');
    span.className = 'char';
    span.textContent = c === ' ' ? '\u00A0' : c;
    span.style.transitionDelay = (delay * 18) + 'ms';
    h.appendChild(span);
    delay++;
  }
});

const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      if (e.target.classList.contains('section-heading')) Sound.whoosh();
      if (e.target.classList.contains('stat')) startCount(e.target);
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

/* ==============================================================
   7. COUNT-UP NUMBERS
   ============================================================== */
const countedStats = new WeakSet();
function startCount(stat) {
  if (countedStats.has(stat)) return;
  countedStats.add(stat);
  const numEl = stat.querySelector('.stat-num');
  if (!numEl) return;
  const target = parseInt(numEl.dataset.count, 10);
  const duration = 1600;
  const start = performance.now();
  function tick(now) {
    const p = Math.min(1, (now - start) / duration);
    const eased = 1 - Math.pow(1 - p, 3);
    const value = Math.floor(eased * target);
    numEl.textContent = value >= 1000000 ? (value / 1e9 >= 1 ? (value / 1e9).toFixed(1) + 'B' : (value / 1e6).toFixed(0) + 'M') : value.toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
    else numEl.textContent = target >= 1000000 ? (target / 1e9 >= 1 ? (target / 1e9).toFixed(1) + 'B' : (target / 1e6).toFixed(0) + 'M') : target.toLocaleString();
  }
  requestAnimationFrame(tick);
}

/* ==============================================================
   8. NAV scroll state
   ============================================================== */
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

/* ==============================================================
   9. PARALLAX in DNA section
   ============================================================== */
const parallax = document.querySelector('.parallax-bg');
window.addEventListener('scroll', () => {
  if (!parallax) return;
  const rect = parallax.getBoundingClientRect();
  const offset = (rect.top - innerHeight / 2) * 0.25;
  parallax.style.transform = `translateY(${offset}px)`;
});

/* ==============================================================
  10. LETTER GRID — every letter glitches on hover
   ============================================================== */
(function buildLetterGrid() {
  const grid = document.getElementById('letter-grid');
  const letters = ['A', 'T', 'C', 'G', 'U'];
  const cols = 16, rows = 6;
  const freqs = { A: 440, T: 523, C: 659, G: 784, U: 880 };

  function glitchCell(cell, origLetter) {
    if (cell.dataset.glitching === '1') return;
    cell.dataset.glitching = '1';
    cell.classList.add('glitching');
    const pool = letters;
    let i = 0;
    const iv = setInterval(() => {
      cell.textContent = pool[Math.floor(Math.random() * pool.length)];
      Sound.glitch();
      i++;
      if (i > 8) {
        clearInterval(iv);
        cell.textContent = origLetter;
        cell.classList.remove('glitching');
        cell.dataset.glitching = '0';
      }
    }, 45);
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const letter = letters[Math.floor(Math.random() * letters.length)];
      const cell = document.createElement('div');
      cell.className = 'letter-cell ' + letter;
      cell.textContent = letter;
      cell.style.animationDelay = ((r * cols + c) * 0.015) + 's';
      cell.addEventListener('mouseenter', () => glitchCell(cell, letter));
      cell.addEventListener('click', () => {
        Sound.click();
        glitchCell(cell, letter);
      });
      grid.appendChild(cell);
    }
  }
})();

/* ==============================================================
  11. HELIX DEMO (DNA section) — scroll-driven rung scaling
   ============================================================== */
(function buildHelixDemo() {
  const root = document.getElementById('helix-demo');
  if (!root) return;
  const seq = ['A','T','G','C','T','A','C','G','A','T','G','C','T','A'];
  const pair = { A:'T', T:'A', C:'G', G:'C' };
  seq.forEach((b, i) => {
    const rung = document.createElement('div');
    rung.className = 'helix-rung';
    const y = 10 + i * 28;
    rung.style.top = y + 'px';
    rung.innerHTML = `
      <div class="helix-base ${b}">${b}</div>
      <div class="helix-bond"></div>
      <div class="helix-base ${pair[b]}">${pair[b]}</div>
    `;
    rung.addEventListener('mouseenter', () => Sound.bond());
    root.appendChild(rung);
  });
  // Rotate on scroll
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
  12. mRNA MAZE animation
   ============================================================== */
(function buildMaze() {
  const maze = document.getElementById('maze-grid');
  if (!maze) return;
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
  const path = [
    [0,0],[0,1],[0,2],[0,3],[0,4],[1,4],[2,4],[2,5],[3,5],[3,6],[3,7],
    [4,7],[5,7],[6,7],[7,7],[8,7],[8,8],[8,9],[9,9]
  ];
  let idx = 0;
  function step() {
    maze.querySelectorAll('.mrna').forEach(c => c.classList.remove('mrna'));
    const [r, c] = path[idx % path.length];
    const target = maze.children[r * 10 + c];
    target.classList.add('mrna');
    idx++;
    if (target.classList.contains('energy')) Sound.energy();
  }
  setInterval(step, 600);
})();

/* ==============================================================
  13. CODON INTERACTION
   ============================================================== */
document.querySelectorAll('.amino-card').forEach(card => {
  card.addEventListener('click', () => {
    const isCorrect = card.hasAttribute('data-correct');
    card.classList.remove('correct', 'wrong');
    void card.offsetWidth;
    if (isCorrect) { card.classList.add('correct'); Sound.correct(); }
    else { card.classList.add('wrong'); Sound.wrong(); }
    setTimeout(() => card.classList.remove('correct', 'wrong'), 600);
  });
});

/* ==============================================================
  14. CELL HEALTH DEMO
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
  15. TITLE-WORD HOVER GLITCH (hero)
   ============================================================== */
document.querySelectorAll('.title-word').forEach(w => {
  w.addEventListener('mouseenter', () => {
    Sound.glitch();
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
  16. HORIZONTAL PINNED SCROLL SECTION
   ============================================================== */
(function pinnedScroll() {
  const section = document.getElementById('pinned');
  const track = section ? section.querySelector('.pinned-track') : null;
  if (!section || !track) return;
  if (window.innerWidth <= 720) return; // mobile fallback: vertical stack

  function onScroll() {
    const rect = section.getBoundingClientRect();
    const total = section.offsetHeight - window.innerHeight;
    if (rect.top > 0 || rect.bottom < window.innerHeight) {
      // outside — clamp
      if (rect.top > 0) track.style.transform = 'translateX(0)';
      if (rect.bottom < window.innerHeight) track.style.transform = `translateX(-${300}vw)`;
      return;
    }
    const progress = Math.min(1, Math.max(0, -rect.top / total));
    // 4 panels → shift up to -300vw
    track.style.transform = `translateX(-${progress * 300}vw)`;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

/* ==============================================================
  17. GAMEPAD BUTTON SOUNDS
   ============================================================== */
document.querySelectorAll('.dpad-btn').forEach(b => b.addEventListener('click', Sound.click));
document.querySelector('.btn-a').addEventListener('click', () => Sound.correct());
document.querySelector('.btn-b').addEventListener('click', () => Sound.bond());

/* ==============================================================
  18. POLYMERASE DROPLET — click to test
   ============================================================== */
const polyTrack = document.querySelector('.poly-track');
if (polyTrack) {
  polyTrack.addEventListener('click', () => {
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

console.log('%cCELL STUDIO — DNA: Code of Life', 'color:#7cf9ff;font-weight:bold;font-size:14px;letter-spacing:4px;');
