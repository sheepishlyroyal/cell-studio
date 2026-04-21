# ==============================================================
#  DNA: CODE OF LIFE  —  v2 FULL REWRITE
#  Educational biology adventure for Microsoft MakeCode Arcade
#  https://arcade.makecode.com/
#
#  HOW TO IMPORT:
#    1. Open https://arcade.makecode.com/ and click "New Project"
#    2. Top-right, switch language from Blocks to PYTHON
#    3. Paste this ENTIRE file
#    4. Press the green play button
#
#  LEVELS (harder, meaner, more fun):
#    L1 - DNA BUILDING      Drag & drop nucleotides into the template
#                           strand with a cursor. Hydrogen bonds snap
#                           closed on correct pairs (2 for A-T, 3 for
#                           C-G). Mutations damage the cell; 3 triggers
#                           "DNA DAMAGE DETECTED" and the strand
#                           collapses. 60s timer before degradation.
#
#    L2 - TRANSCRIPTION     A fast-moving RNA polymerase droplet
#                           oscillates above the DNA, accelerating
#                           with every attempt. Drop it onto the
#                           glowing TATA promoter with A. Miss too
#                           many times and transcription shuts down.
#                           On success: strands split, mRNA auto-builds.
#
#    L3 - mRNA MAZE         Real tile maze. Collect energy orbs,
#                           dodge chasing RNase enzymes, touch SAFE
#                           ZONES to stabilize (buys time), reach the
#                           ribosome with enough energy. Timer ticks
#                           down; three hits = mRNA degraded.
#
#  GLOBAL:
#    One shared Cell Health bar (info.set_life). Every mistake in
#    every level hits the same bar. Zero = game over.
# ==============================================================


# ==============================================================
#  1. COLOR / LETTER MAPPING
# ==============================================================
# MakeCode Arcade palette indices
A_COLOR = 2    # red      - adenine
T_COLOR = 9    # blue     - thymine
C_COLOR = 7    # green    - cytosine
G_COLOR = 5    # yellow   - guanine
U_COLOR = 11   # purple   - uracil
INK_COLOR = 1  # white
DARK_BG  = 15  # black
GLOW     = 9   # light blue accent


# ==============================================================
#  2. PIXEL ART — NUCLEOTIDES & GAME PIECES
# ==============================================================
# Larger 10x10 nucleotides for better readability

def nuc_img(letter):
    if letter == "A":
        return img("""
            . . 2 2 2 2 2 2 . .
            . 2 2 2 2 2 2 2 2 .
            2 2 1 1 2 2 1 1 2 2
            2 2 1 1 2 2 1 1 2 2
            2 2 2 2 2 2 2 2 2 2
            2 2 1 1 1 1 1 1 2 2
            2 2 1 1 1 1 1 1 2 2
            2 2 2 2 2 2 2 2 2 2
            . 2 2 2 2 2 2 2 2 .
            . . 2 2 2 2 2 2 . .
        """)
    if letter == "T":
        return img("""
            . . 9 9 9 9 9 9 . .
            . 9 9 9 9 9 9 9 9 .
            9 9 1 1 9 9 1 1 9 9
            9 9 1 1 9 9 1 1 9 9
            9 9 9 9 9 9 9 9 9 9
            9 9 1 1 1 1 1 1 9 9
            9 9 1 1 1 1 1 1 9 9
            9 9 9 9 9 9 9 9 9 9
            . 9 9 9 9 9 9 9 9 .
            . . 9 9 9 9 9 9 . .
        """)
    if letter == "C":
        return img("""
            . . 7 7 7 7 7 7 . .
            . 7 7 7 7 7 7 7 7 .
            7 7 1 1 7 7 1 1 7 7
            7 7 1 1 7 7 1 1 7 7
            7 7 7 7 7 7 7 7 7 7
            7 7 1 1 1 1 1 1 7 7
            7 7 1 1 1 1 1 1 7 7
            7 7 7 7 7 7 7 7 7 7
            . 7 7 7 7 7 7 7 7 .
            . . 7 7 7 7 7 7 . .
        """)
    if letter == "G":
        return img("""
            . . 5 5 5 5 5 5 . .
            . 5 5 5 5 5 5 5 5 .
            5 5 1 1 5 5 1 1 5 5
            5 5 1 1 5 5 1 1 5 5
            5 5 5 5 5 5 5 5 5 5
            5 5 1 1 1 1 1 1 5 5
            5 5 1 1 1 1 1 1 5 5
            5 5 5 5 5 5 5 5 5 5
            . 5 5 5 5 5 5 5 5 .
            . . 5 5 5 5 5 5 . .
        """)
    # U (RNA)
    return img("""
        . . 11 11 11 11 11 11 . .
        . 11 11 11 11 11 11 11 11 .
        11 11 1 1 11 11 1 1 11 11
        11 11 1 1 11 11 1 1 11 11
        11 11 11 11 11 11 11 11 11 11
        11 11 1 1 1 1 1 1 11 11
        11 11 1 1 1 1 1 1 11 11
        11 11 11 11 11 11 11 11 11 11
        . 11 11 11 11 11 11 11 11 .
        . . 11 11 11 11 11 11 . .
    """)

# Slot outline (empty slot in template strand)
def slot_empty_img():
    return img("""
        1 1 1 1 1 1 1 1 1 1
        1 . . . . . . . . 1
        1 . . . . . . . . 1
        1 . . . . . . . . 1
        1 . . . . . . . . 1
        1 . . . . . . . . 1
        1 . . . . . . . . 1
        1 . . . . . . . . 1
        1 . . . . . . . . 1
        1 1 1 1 1 1 1 1 1 1
    """)

# Target letter dimmed outline (shows what letter is expected)
def slot_target_img(letter):
    if letter == "A":
        return img("""
            1 1 1 1 1 1 1 1 1 1
            1 . 2 2 2 2 2 2 . 1
            1 2 . . . . . . 2 1
            1 2 . . 2 2 . . 2 1
            1 2 . . . . . . 2 1
            1 2 . 2 2 2 2 . 2 1
            1 2 . . . . . . 2 1
            1 2 . . . . . . 2 1
            1 . 2 2 2 2 2 2 . 1
            1 1 1 1 1 1 1 1 1 1
        """)
    if letter == "T":
        return img("""
            1 1 1 1 1 1 1 1 1 1
            1 . 9 9 9 9 9 9 . 1
            1 9 . . . . . . 9 1
            1 9 . . 9 9 . . 9 1
            1 9 . . . . . . 9 1
            1 9 . 9 9 9 9 . 9 1
            1 9 . . . . . . 9 1
            1 9 . . . . . . 9 1
            1 . 9 9 9 9 9 9 . 1
            1 1 1 1 1 1 1 1 1 1
        """)
    if letter == "C":
        return img("""
            1 1 1 1 1 1 1 1 1 1
            1 . 7 7 7 7 7 7 . 1
            1 7 . . . . . . 7 1
            1 7 . . 7 7 . . 7 1
            1 7 . . . . . . 7 1
            1 7 . 7 7 7 7 . 7 1
            1 7 . . . . . . 7 1
            1 7 . . . . . . 7 1
            1 . 7 7 7 7 7 7 . 1
            1 1 1 1 1 1 1 1 1 1
        """)
    # G
    return img("""
        1 1 1 1 1 1 1 1 1 1
        1 . 5 5 5 5 5 5 . 1
        1 5 . . . . . . 5 1
        1 5 . . 5 5 . . 5 1
        1 5 . . . . . . 5 1
        1 5 . 5 5 5 5 . 5 1
        1 5 . . . . . . 5 1
        1 5 . . . . . . 5 1
        1 . 5 5 5 5 5 5 . 1
        1 1 1 1 1 1 1 1 1 1
    """)

# Player cursor / hand
def cursor_img():
    return img("""
        . . 1 1 1 1 . . .
        . 1 . . . . 1 . .
        1 . . . . . . 1 .
        1 . . 9 9 . . 1 .
        1 . . 9 9 . . 1 .
        1 . . . . . . 1 .
        . 1 . . . . 1 . .
        . . 1 1 1 1 . . .
        . . . 1 1 . . . .
    """)

# Yellow "YOU" label that floats above the player sprite
def you_label_img():
    # 15x7 pixel-art "YOU" in color 5 (yellow) with black outline
    return img("""
        5 . 5 . 5 5 5 . 5 5 5
        5 . 5 . 5 . 5 . 5 . 5
        5 . 5 . 5 . 5 . 5 . 5
        . 5 . . 5 . 5 . 5 . 5
        . 5 . . 5 . 5 . 5 . 5
        . 5 . . 5 . 5 . 5 . 5
        . 5 . . 5 5 5 . 5 5 5
    """)

# Hydrogen bond (small dots)
def bond_dot_img():
    return img("""
        1 1
        1 1
    """)

# H-bond line between paired bases
def bond_line_img():
    return img("""
        1 1 1 1 1 1 1 1 1 1 1 1
    """)

# RNA polymerase droplet (moving object in Level 2)
def droplet_img():
    return img("""
        . . . 11 11 . . .
        . . 11 11 11 11 . .
        . 11 11 1 1 11 11 .
        11 11 1 1 1 1 11 11
        11 11 1 11 11 1 11 11
        11 11 11 11 11 11 11 11
        . 11 11 11 11 11 11 .
        . . 11 11 11 11 . .
        . . . 11 11 . . .
    """)

# DNA strand piece (for Level 2 background)
def strand_piece_top():
    return img("""
        8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
        8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8
        8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
    """)

def strand_piece_bot():
    return img("""
        2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
        2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
        2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
    """)

# TATA promoter box (glowing zone)
def tata_img():
    return img("""
        5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
        5 1 1 1 5 5 1 5 1 1 1 5 5 5 1 5 5 5 5 5
        5 1 5 5 5 5 1 5 5 1 5 5 5 1 5 1 5 5 5 5
        5 1 1 1 5 5 1 5 5 1 5 5 5 1 5 1 5 5 5 5
        5 1 5 5 5 5 1 5 5 1 5 5 5 1 1 1 5 5 5 5
        5 1 5 5 5 5 1 5 5 1 5 5 5 1 5 1 5 5 5 5
        5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
    """)

# Aim arrow (shown when trying to drop droplet)
def aim_line_img():
    return img("""
        1
        1
        1
        1
        1
        1
    """)

# mRNA player (Level 3)
def mrna_player_img():
    return img("""
        . 11 11 11 11 11 11 .
        11 1 11 11 11 11 1 11
        11 11 1 11 11 1 11 11
        11 11 11 1 1 11 11 11
        11 11 11 1 1 11 11 11
        11 11 1 11 11 1 11 11
        11 1 11 11 11 11 1 11
        . 11 11 11 11 11 11 .
    """)

# RNase enzyme (Level 3 enemy)
def rnase_img():
    return img("""
        . 2 2 2 2 2 2 .
        2 1 . 2 2 . 1 2
        2 . 2 2 2 2 . 2
        2 2 2 1 1 2 2 2
        2 2 2 1 1 2 2 2
        2 . 2 2 2 2 . 2
        2 1 . 2 2 . 1 2
        . 2 2 2 2 2 2 .
    """)

# ATP energy orb
def atp_img():
    return img("""
        . . 4 4 4 . .
        . 4 5 5 5 4 .
        4 5 5 1 5 5 4
        4 5 1 1 1 5 4
        4 5 5 1 5 5 4
        . 4 5 5 5 4 .
        . . 4 4 4 . .
    """)

# Ribosome (goal)
def ribosome_img():
    return img("""
        . 6 6 6 6 6 6 6 6 6 .
        6 6 7 7 6 6 6 7 7 6 6
        6 7 7 7 7 6 7 7 7 7 6
        6 7 7 1 7 7 7 7 1 7 6
        6 7 7 7 7 7 7 7 7 7 6
        6 6 7 7 7 7 7 7 7 6 6
        . 6 6 7 7 7 7 7 6 6 .
        . . 6 6 7 7 7 6 6 . .
        . . . 6 6 6 6 6 . . .
    """)

# Wall tile (maze)
def wall_img():
    return img("""
        10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
        10 11 11 11 11 11 11 11 11 11 11 11 11 11 11 10
        10 11 10 10 11 11 10 10 11 11 10 10 11 11 11 10
        10 11 11 11 11 11 11 11 11 11 11 11 11 11 11 10
        10 11 11 11 11 10 10 11 11 11 10 10 11 11 11 10
        10 10 10 11 11 10 10 11 11 11 10 10 11 11 11 10
        10 11 11 11 11 11 11 11 11 11 11 11 11 11 11 10
        10 11 11 10 10 11 11 10 10 11 11 10 10 11 11 10
        10 11 11 10 10 11 11 10 10 11 11 10 10 11 11 10
        10 11 11 11 11 11 11 11 11 11 11 11 11 11 11 10
        10 11 10 10 11 11 10 10 11 11 10 10 11 11 11 10
        10 11 11 11 11 11 11 11 11 11 11 11 11 11 11 10
        10 11 11 11 11 10 10 11 11 11 10 10 11 11 11 10
        10 10 10 11 11 10 10 11 11 11 10 10 11 11 11 10
        10 11 11 11 11 11 11 11 11 11 11 11 11 11 11 10
        10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
    """)

# Safe zone (Level 3 - heals mRNA / pauses timer)
def safe_zone_img():
    return img("""
        6 6 6 6 6 6 6 6
        6 1 6 6 6 6 1 6
        6 6 1 6 6 1 6 6
        6 6 6 1 1 6 6 6
        6 6 6 1 1 6 6 6
        6 6 1 6 6 1 6 6
        6 1 6 6 6 6 1 6
        6 6 6 6 6 6 6 6
    """)


# ==============================================================
#  3. GLOBAL STATE
# ==============================================================
current_level = 0
cell_health   = 100
score         = 0
game_running  = False

# Custom sprite kinds
WALL_KIND      = SpriteKind.create()
UI_KIND        = SpriteKind.create()
HELD_KIND      = SpriteKind.create()
SLOT_KIND      = SpriteKind.create()
BOND_KIND      = SpriteKind.create()
DROPLET_KIND   = SpriteKind.create()
TATA_KIND      = SpriteKind.create()
STRAND_KIND    = SpriteKind.create()
SAFE_KIND      = SpriteKind.create()
YOU_LABEL_KIND = SpriteKind.create()

# Global "YOU" label sprite that follows the current player sprite
you_label: Sprite = None


# ==============================================================
#  4. SOUND EFFECTS (non-blocking — never stalls the game)
# ==============================================================
def sfx_correct():
    music.play(music.tone_playable(523, music.beat(BeatFraction.EIGHTH)),
               music.PlaybackMode.IN_BACKGROUND)
    music.play(music.tone_playable(784, music.beat(BeatFraction.EIGHTH)),
               music.PlaybackMode.IN_BACKGROUND)

def sfx_wrong():
    music.play(music.tone_playable(196, music.beat(BeatFraction.QUARTER)),
               music.PlaybackMode.IN_BACKGROUND)
    music.play(music.tone_playable(147, music.beat(BeatFraction.QUARTER)),
               music.PlaybackMode.IN_BACKGROUND)

def sfx_bond():
    music.play(music.tone_playable(880, music.beat(BeatFraction.EIGHTH)),
               music.PlaybackMode.IN_BACKGROUND)

def sfx_pickup():
    music.play(music.tone_playable(659, music.beat(BeatFraction.SIXTEENTH)),
               music.PlaybackMode.IN_BACKGROUND)

def sfx_drop():
    music.play(music.tone_playable(392, music.beat(BeatFraction.SIXTEENTH)),
               music.PlaybackMode.IN_BACKGROUND)

def sfx_energy():
    music.play(music.tone_playable(1046, music.beat(BeatFraction.EIGHTH)),
               music.PlaybackMode.IN_BACKGROUND)

def sfx_damage():
    music.play(music.tone_playable(110, music.beat(BeatFraction.HALF)),
               music.PlaybackMode.IN_BACKGROUND)

def sfx_glitch():
    music.play(music.tone_playable(70, music.beat(BeatFraction.SIXTEENTH)),
               music.PlaybackMode.IN_BACKGROUND)
    music.play(music.tone_playable(140, music.beat(BeatFraction.SIXTEENTH)),
               music.PlaybackMode.IN_BACKGROUND)

def _melody_level_up():
    music.play_melody("C5 E5 G5 C6", 180)

def _melody_win():
    music.play_melody("C E G C5 E5 G5 C6 E6 G6", 150)

def _melody_death():
    music.play_melody("C5 B A G F E D C C3", 180)

def sfx_level_up():
    control.run_in_parallel(_melody_level_up)

def sfx_win():
    control.run_in_parallel(_melody_win)

def sfx_death():
    control.run_in_parallel(_melody_death)


# ==============================================================
#  5. HUD & HEALTH HELPERS
# ==============================================================
def update_hud():
    info.set_life(max(1, cell_health // 10))
    info.set_score(score)

def take_damage(amount):
    global cell_health
    cell_health = cell_health - amount
    if cell_health < 0:
        cell_health = 0
    update_hud()
    scene.camera_shake(4, 300)
    if cell_health <= 0:
        lose_game("CELL FLATLINED")

def heal(amount):
    global cell_health
    cell_health = cell_health + amount
    if cell_health > 100:
        cell_health = 100
    update_hud()

def add_score(amount):
    global score
    score = score + amount
    update_hud()

def clear_gameplay_sprites():
    global you_label
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.projectile)
    sprites.destroy_all_sprites_of_kind(WALL_KIND)
    sprites.destroy_all_sprites_of_kind(HELD_KIND)
    sprites.destroy_all_sprites_of_kind(SLOT_KIND)
    sprites.destroy_all_sprites_of_kind(BOND_KIND)
    sprites.destroy_all_sprites_of_kind(DROPLET_KIND)
    sprites.destroy_all_sprites_of_kind(TATA_KIND)
    sprites.destroy_all_sprites_of_kind(STRAND_KIND)
    sprites.destroy_all_sprites_of_kind(SAFE_KIND)
    sprites.destroy_all_sprites_of_kind(YOU_LABEL_KIND)
    you_label = None

# Create/position a yellow "YOU" label above the given player sprite.
# Call once after the player sprite exists, then reposition it every
# frame from the per-level on_update.
def spawn_you_label():
    global you_label
    if you_label is not None:
        you_label.destroy()
    you_label = sprites.create(you_label_img(), YOU_LABEL_KIND)
    you_label.set_flag(SpriteFlag.GHOST, True)
    you_label.z = 100

def position_you_label(target: Sprite):
    if you_label is None or target is None:
        return
    you_label.set_position(target.x, target.y - 10)


# ==============================================================
#  6. SCREEN EFFECTS (glitch, damage flash, level splash)
# ==============================================================
def glitch_screen():
    scene.camera_shake(6, 400)
    effects.dissolve.start_screen_effect(180)
    sfx_glitch()


# ==============================================================
#  7. LEVEL 1 — DNA BUILDING (drag & drop nucleotides)
# ==============================================================
# 10 template slots at top. Nucleotide palette (A T C G) at bottom.
# Cursor moves freely with joystick. Press A near a palette tile to
# pick up; press A near a slot to drop. Correct placement triggers
# hydrogen-bond animation. Wrong = mutation. 3 mutations = collapse.
# Timer: 60s before strand degrades.

LEVEL1_SLOTS = 10
LEVEL1_MUTATION_LIMIT = 3
LEVEL1_TIME = 60

level1_template   = ["T","A","C","G","A","T","G","C","T","A"]
level1_targets    = ["A","T","G","C","T","A","C","G","A","T"]
level1_filled     = [False, False, False, False, False, False, False, False, False, False]
level1_mutations  = 0
level1_correct    = 0
level1_held       = ""
level1_cursor: Sprite = None
level1_held_sprite: Sprite = None
level1_palette_sprites: List[Sprite] = []
level1_slot_sprites: List[Sprite] = []
level1_template_sprites: List[Sprite] = []
level1_timer_sprite: Sprite = None

# Slot geometry — 10 slots across top, 12px wide with 2px gaps
LEVEL1_SLOT_Y = 22
LEVEL1_SLOT_START_X = 14
LEVEL1_SLOT_STRIDE = 14

LEVEL1_TEMPLATE_Y = 8

# Palette geometry — 4 nucleotides at bottom
LEVEL1_PALETTE_Y = 104
LEVEL1_PALETTE_XS = [30, 60, 90, 120]
LEVEL1_PALETTE_LETTERS = ["A", "T", "C", "G"]

def level1_slot_x(idx):
    return LEVEL1_SLOT_START_X + idx * LEVEL1_SLOT_STRIDE

def start_level1():
    global current_level, game_running
    global level1_mutations, level1_correct, level1_held
    global level1_cursor, level1_held_sprite
    global level1_palette_sprites, level1_slot_sprites, level1_template_sprites
    global level1_filled
    current_level = 1
    game_running = True
    clear_gameplay_sprites()
    scene.set_background_color(15)

    level1_mutations = 0
    level1_correct = 0
    level1_held = ""
    level1_held_sprite = None
    level1_filled = [False, False, False, False, False, False, False, False, False, False]

    game.splash("LEVEL 1", "DNA BUILDING")
    game.splash("Match bases:", "A-T  and  C-G")
    game.splash("Pick with A", "Drop with A in slot")
    game.splash("3 mutations =", "DNA COLLAPSE!")

    # Template strand at top (shows what each slot needs to pair with)
    level1_template_sprites = []
    for i in range(LEVEL1_SLOTS):
        s = sprites.create(nuc_img(level1_template[i]), SLOT_KIND)
        s.set_position(level1_slot_x(i), LEVEL1_TEMPLATE_Y)
        level1_template_sprites.append(s)

    # Empty slots just below (where player places complements)
    level1_slot_sprites = []
    for i in range(LEVEL1_SLOTS):
        s = sprites.create(slot_target_img(level1_targets[i]), SLOT_KIND)
        s.set_position(level1_slot_x(i), LEVEL1_SLOT_Y)
        level1_slot_sprites.append(s)

    # Palette at bottom
    level1_palette_sprites = []
    for i in range(4):
        s = sprites.create(nuc_img(LEVEL1_PALETTE_LETTERS[i]), SLOT_KIND)
        s.set_position(LEVEL1_PALETTE_XS[i], LEVEL1_PALETTE_Y)
        level1_palette_sprites.append(s)

    # Cursor (player) — start near the palette so the user sees the
    # affordance immediately. Faster move speed + STAY_IN_SCREEN.
    level1_cursor = sprites.create(cursor_img(), SpriteKind.player)
    level1_cursor.set_position(30, 90)
    controller.move_sprite(level1_cursor, 140, 140)
    level1_cursor.set_flag(SpriteFlag.STAY_IN_SCREEN, True)
    spawn_you_label()

    game.splash("Move with D-pad", "A = pick / place")
    game.splash("Start at PALETTE", "Go UP to slot")

    # Start countdown
    info.start_countdown(LEVEL1_TIME)
    info.on_countdown_end(on_level1_time_out)
    update_hud()
    sfx_level_up()

def on_level1_time_out():
    if current_level == 1 and game_running:
        game.splash("DEGRADATION!", "Strand dissolved.")
        lose_game("TIME RAN OUT")

def level1_nearest_palette_index():
    # Return palette idx if cursor is near a palette nucleotide, else -1.
    # Generous thresholds so the user can easily grab a base.
    if level1_cursor is None:
        return -1
    cy = level1_cursor.y
    if abs(cy - LEVEL1_PALETTE_Y) > 20:
        return -1
    best = -1
    best_d = 9999
    for i in range(4):
        d = abs(level1_cursor.x - LEVEL1_PALETTE_XS[i])
        if d < 16 and d < best_d:
            best = i
            best_d = d
    return best

def level1_nearest_slot_index():
    # Return slot idx if cursor is over a slot, else -1.
    # Pick the slot closest to the cursor x, not just one within range.
    if level1_cursor is None:
        return -1
    cy = level1_cursor.y
    if abs(cy - LEVEL1_SLOT_Y) > 20:
        return -1
    best = -1
    best_d = 9999
    for i in range(LEVEL1_SLOTS):
        d = abs(level1_cursor.x - level1_slot_x(i))
        if d < 12 and d < best_d:
            best = i
            best_d = d
    return best

def level1_pick_up(letter):
    global level1_held, level1_held_sprite
    level1_held = letter
    if level1_held_sprite is not None:
        level1_held_sprite.destroy()
    level1_held_sprite = sprites.create(nuc_img(letter), HELD_KIND)
    sfx_pickup()

def level1_drop_held():
    global level1_held, level1_held_sprite
    level1_held = ""
    if level1_held_sprite is not None:
        level1_held_sprite.destroy()
    level1_held_sprite = None

def level1_attempt_place(slot_idx):
    global level1_correct, level1_mutations
    if level1_filled[slot_idx]:
        return
    target = level1_targets[slot_idx]
    if level1_held == target:
        # correct placement!
        placed = sprites.create(nuc_img(level1_held), SLOT_KIND)
        placed.set_position(level1_slot_x(slot_idx), LEVEL1_SLOT_Y)
        level1_filled[slot_idx] = True
        level1_correct = level1_correct + 1
        add_score(15)
        sfx_correct()
        # Hydrogen bonds: 2 for A-T, 3 for C-G
        nbonds = 2
        if target == "C" or target == "G":
            nbonds = 3
        for b in range(nbonds):
            bd = sprites.create(bond_dot_img(), BOND_KIND)
            bd.set_position(level1_slot_x(slot_idx) - 2 + b * 2,
                            (LEVEL1_TEMPLATE_Y + LEVEL1_SLOT_Y) // 2)
            bd.lifespan = 9999
        sfx_bond()
        level1_drop_held()
        # win check
        if level1_correct >= LEVEL1_SLOTS:
            info.stop_countdown()
            level1_win()
    else:
        # wrong placement!
        level1_mutations = level1_mutations + 1
        take_damage(10)
        sfx_wrong()
        glitch_screen()
        # visual: shake the camera to emphasize the error
        scene.camera_shake(4, 220)
        game.splash("MUTATION!", "Wrong base.")
        if level1_mutations >= LEVEL1_MUTATION_LIMIT:
            info.stop_countdown()
            game.splash("DNA DAMAGE", "DETECTED!")
            game.splash("Strand collapsed!", "")
            lose_game("TOO MANY MUTATIONS")
        else:
            level1_drop_held()

def level1_on_a():
    # Priority: if holding -> try drop in slot. If empty -> try pickup.
    if level1_held == "":
        pi = level1_nearest_palette_index()
        if pi >= 0:
            level1_pick_up(LEVEL1_PALETTE_LETTERS[pi])
    else:
        si = level1_nearest_slot_index()
        if si >= 0:
            level1_attempt_place(si)

def level1_on_b():
    # B: drop current held back
    if level1_held != "":
        level1_drop_held()
        sfx_drop()

def level1_on_update():
    if current_level != 1 or not game_running:
        return
    if level1_held_sprite is not None and level1_cursor is not None:
        level1_held_sprite.set_position(level1_cursor.x, level1_cursor.y - 10)
    position_you_label(level1_cursor)

def level1_win():
    game.splash("LEVEL 1", "CLEAR!")
    game.splash("All 10 bases", "paired.")
    add_score(100)
    heal(15)
    effects.confetti.start_screen_effect(1200)
    sfx_level_up()
    control.wait_micros(100000)

    # ---- Educational debrief: DNA base pairing ----
    game.splash("WHAT JUST HAPPENED?", "DNA Base Pairing")
    game.splash("DNA stores info in", "A-T and C-G pairs.")
    game.splash("A bonds with T", "via 2 H-bonds.")
    game.splash("C bonds with G", "via 3 H-bonds.")
    game.splash("That is why C-G", "regions are stronger.")
    game.splash("Each human cell has", "~3 billion base pairs.")
    game.splash("Stretched out:", "2 meters of DNA!")

    game.splash("REAL-WORLD USE #1:", "DNA Forensics")
    game.splash("Crime labs match", "DNA at crime scenes")
    game.splash("using the same", "pairing rules.")

    game.splash("REAL-WORLD USE #2:", "Ancestry Testing")
    game.splash("23andMe reads your", "base-pair sequence")
    game.splash("to trace your", "genetic heritage.")

    game.splash("REAL-WORLD USE #3:", "CRISPR gene editing")
    game.splash("Scientists re-pair", "bases to cure")
    game.splash("sickle cell, cancer,", "blindness, and more.")

    game.splash("FUN FACT:", "DNA is so dense,")
    game.splash("1 gram could store", "215 petabytes of data.")

    game.splash("NEXT UP...", "TRANSCRIPTION!")
    start_level2()


# ==============================================================
#  8. LEVEL 2 — TRANSCRIPTION (drop droplet on TATA)
# ==============================================================
# A fast-moving purple polymerase droplet bounces left-right above
# the DNA strand. Press A to drop it. If it lands on the glowing
# TATA zone, transcription initiates: strands separate visually
# and mRNA auto-builds. Misses speed up the droplet and cost
# attempts. 3 successful drops = level complete. 3 misses = fail.

LEVEL2_SUCCESSES_NEEDED = 3
LEVEL2_MAX_MISSES = 3
LEVEL2_TIME = 45

level2_droplet: Sprite = None
level2_droplet_x      = 10
level2_droplet_dir    = 1
level2_droplet_speed  = 2.2  # pixels per frame
level2_successes      = 0
level2_misses         = 0
level2_can_drop       = True
level2_strand_top: Sprite = None
level2_strand_bot: Sprite = None
level2_tata: Sprite = None
level2_tata_x         = 80
level2_tata_width     = 22
level2_mrna_sprites: List[Sprite] = []

LEVEL2_DROPLET_Y = 28
LEVEL2_STRAND_Y  = 64

def start_level2():
    global current_level, game_running
    global level2_droplet, level2_droplet_x, level2_droplet_dir, level2_droplet_speed
    global level2_successes, level2_misses, level2_can_drop
    global level2_strand_top, level2_strand_bot, level2_tata, level2_tata_x
    global level2_mrna_sprites
    current_level = 2
    game_running = True
    clear_gameplay_sprites()
    scene.set_background_color(11)  # deep purple

    level2_droplet_x = 10.0
    level2_droplet_dir = 1
    level2_droplet_speed = 2.2
    level2_successes = 0
    level2_misses = 0
    level2_can_drop = True
    level2_mrna_sprites = []

    game.splash("LEVEL 2", "TRANSCRIPTION")
    game.splash("Drop polymerase", "onto TATA box!")
    game.splash("A = DROP", "3 hits = WIN")
    game.splash("3 misses = FAIL", "Speed rises!")

    # DNA strand — top half (blue) and bottom half (red)
    level2_strand_top = sprites.create(strand_piece_top(), STRAND_KIND)
    level2_strand_top.set_position(80, LEVEL2_STRAND_Y - 3)

    level2_strand_bot = sprites.create(strand_piece_bot(), STRAND_KIND)
    level2_strand_bot.set_position(80, LEVEL2_STRAND_Y + 3)

    # TATA promoter box — randomize location between attempts
    level2_tata_x = randint(50, 110)
    level2_tata = sprites.create(tata_img(), TATA_KIND)
    level2_tata.set_position(level2_tata_x, LEVEL2_STRAND_Y - 16)

    # Droplet
    level2_droplet = sprites.create(droplet_img(), DROPLET_KIND)
    level2_droplet.set_position(int(level2_droplet_x), LEVEL2_DROPLET_Y)
    spawn_you_label()

    info.start_countdown(LEVEL2_TIME)
    info.on_countdown_end(on_level2_time_out)
    update_hud()
    sfx_level_up()

def on_level2_time_out():
    if current_level == 2 and game_running:
        game.splash("TRANSCRIPTION", "TIMED OUT!")
        lose_game("TRANSCRIPTION FAIL")

def level2_on_update():
    global level2_droplet_x, level2_droplet_dir
    if current_level != 2 or not game_running:
        return
    if level2_droplet is None:
        return
    if not level2_can_drop:
        return
    # Oscillate droplet horizontally, bounce at walls
    level2_droplet_x = level2_droplet_x + level2_droplet_dir * level2_droplet_speed
    if level2_droplet_x > 150:
        level2_droplet_x = 150
        level2_droplet_dir = -1
    if level2_droplet_x < 10:
        level2_droplet_x = 10
        level2_droplet_dir = 1
    level2_droplet.set_position(int(level2_droplet_x), LEVEL2_DROPLET_Y)
    position_you_label(level2_droplet)

def level2_on_a():
    global level2_can_drop, level2_successes, level2_misses, level2_droplet_speed
    global level2_tata_x
    if current_level != 2 or not game_running:
        return
    if not level2_can_drop or level2_droplet is None:
        return
    level2_can_drop = False
    # Drop the droplet straight down and check
    drop_x = int(level2_droplet_x)
    # Animate falling
    level2_droplet.set_velocity(0, 160)
    # Wait for it to arrive at strand
    _level2_resolve_drop(drop_x)

def _level2_resolve_drop(drop_x):
    global level2_successes, level2_misses, level2_droplet_speed, level2_tata_x
    # Check if over TATA
    hit = abs(drop_x - level2_tata_x) <= (level2_tata_width // 2)
    if hit:
        sfx_correct()
        add_score(30)
        level2_successes = level2_successes + 1
        _level2_split_strands(drop_x)
        _level2_build_mrna_animated(drop_x)
        game.splash("PROMOTER HIT!", "Strands split.")
        if level2_successes >= LEVEL2_SUCCESSES_NEEDED:
            info.stop_countdown()
            level2_win()
            return
    else:
        sfx_wrong()
        take_damage(12)
        level2_misses = level2_misses + 1
        game.splash("MISSED!", "Wrong zone.")
        glitch_screen()
        if level2_misses >= LEVEL2_MAX_MISSES:
            info.stop_countdown()
            game.splash("TRANSCRIPTION", "SHUTDOWN!")
            lose_game("TOO MANY MISSES")
            return
    # Reset droplet for next attempt; speed ramps up
    _level2_reset_droplet()

def _level2_split_strands(drop_x):
    # Quick animation: top strand jumps up, bot stays
    if level2_strand_top is not None:
        level2_strand_top.set_velocity(0, -20)
        level2_strand_top.start_effect(effects.bubbles, 300)
    if level2_strand_bot is not None:
        level2_strand_bot.set_velocity(0, 10)
    control.wait_micros(250000)
    if level2_strand_top is not None:
        level2_strand_top.set_velocity(0, 0)
    if level2_strand_bot is not None:
        level2_strand_bot.set_velocity(0, 0)

def _level2_build_mrna_animated(start_x):
    # Spawn a little row of U nucleotides building from start_x rightward
    count = 5
    for i in range(count):
        u = sprites.create(nuc_img("U"), SLOT_KIND)
        u.set_position(start_x + (i + 1) * 6, LEVEL2_STRAND_Y + 12)
        u.start_effect(effects.cool_radial, 200)
        level2_mrna_sprites.append(u)
        sfx_bond()
        control.wait_micros(60000)

def _level2_reset_droplet():
    global level2_can_drop, level2_droplet_x, level2_droplet_dir, level2_droplet_speed
    global level2_tata_x
    control.wait_micros(400000)
    if level2_droplet is None:
        return
    level2_droplet.set_velocity(0, 0)
    level2_droplet_x = 10.0
    level2_droplet_dir = 1
    level2_droplet_speed = level2_droplet_speed + 0.6   # SPEED RAMP!
    level2_droplet.set_position(int(level2_droplet_x), LEVEL2_DROPLET_Y)
    # Reposition TATA for next attempt
    level2_tata_x = randint(40, 120)
    if level2_tata is not None:
        level2_tata.set_position(level2_tata_x, LEVEL2_STRAND_Y - 16)
    # restore split strands
    if level2_strand_top is not None:
        level2_strand_top.set_position(80, LEVEL2_STRAND_Y - 3)
    if level2_strand_bot is not None:
        level2_strand_bot.set_position(80, LEVEL2_STRAND_Y + 3)
    level2_can_drop = True

def level2_win():
    game.splash("LEVEL 2", "CLEAR!")
    game.splash("mRNA ready", "for export.")
    add_score(150)
    heal(20)
    effects.confetti.start_screen_effect(1200)
    sfx_level_up()
    control.wait_micros(100000)

    # ---- Educational debrief: Transcription ----
    game.splash("WHAT JUST HAPPENED?", "Transcription")
    game.splash("RNA polymerase", "read your DNA")
    game.splash("and copied it into", "messenger RNA.")
    game.splash("TATA box = the", "promoter landing pad.")
    game.splash("Without TATA,", "no transcription!")
    game.splash("RNA uses URACIL (U)", "instead of T.")

    game.splash("SPEED FACT:", "Polymerase reads")
    game.splash("about 40 bases", "per SECOND.")

    game.splash("REAL-WORLD USE #1:", "mRNA Vaccines")
    game.splash("COVID vaccines from", "Pfizer and Moderna")
    game.splash("are lab-made mRNA", "that trains your cells.")

    game.splash("REAL-WORLD USE #2:", "Cancer Research")
    game.splash("Tumors often hijack", "transcription.")
    game.splash("Drugs that block RNA", "polymerase stop tumors.")

    game.splash("REAL-WORLD USE #3:", "Antibiotics")
    game.splash("Rifampin kills TB", "by jamming bacterial")
    game.splash("RNA polymerase.", "Your human one is safe!")

    game.splash("FUN FACT:", "Your body transcribes")
    game.splash("about 75,000 mRNA", "molecules every second.")

    game.splash("NEXT UP...", "mRNA DELIVERY!")
    start_level3()


# ==============================================================
#  9. LEVEL 3 — mRNA MAZE
# ==============================================================
# Tile-based maze. Player = mRNA. Goal = ribosome. Collect >=5 ATP
# orbs and avoid 4 patrolling RNase enzymes. Safe zones restore time
# and briefly make the player invulnerable. Timer ticks down; hitting
# 3 enzymes or the timer reaching 0 degrades the mRNA.

LEVEL3_COLS = 10
LEVEL3_ROWS = 7
LEVEL3_TILE = 16
LEVEL3_ORIGIN_X = 8     # first tile center x
LEVEL3_ORIGIN_Y = 10    # first tile center y
LEVEL3_TIME = 50
LEVEL3_ENERGY_NEEDED = 3
LEVEL3_HIT_LIMIT = 4

# Legend: '.' path  '#' wall  'S' start  'R' ribosome  'E' energy  'V' safe zone
level3_layout = [
    "S.........",
    ".##.###.#.",
    ".E...#...V",
    ".###.#.##.",
    ".....V..E.",
    "E##.###...",
    "..E....#.R",
]

level3_walls: List[Sprite] = []
level3_enemies: List[Sprite] = []
level3_energies: List[Sprite] = []
level3_safes: List[Sprite] = []
level3_player: Sprite = None
level3_ribosome: Sprite = None
level3_hits      = 0
level3_energy_collected = 0
level3_invuln_until = 0

def level3_tile_center(r, c):
    x = LEVEL3_ORIGIN_X + c * LEVEL3_TILE
    y = LEVEL3_ORIGIN_Y + r * LEVEL3_TILE
    return x, y

def start_level3():
    global current_level, game_running
    global level3_walls, level3_enemies, level3_energies, level3_safes
    global level3_player, level3_ribosome
    global level3_hits, level3_energy_collected
    global level3_invuln_until
    current_level = 3
    game_running = True
    clear_gameplay_sprites()
    scene.set_background_color(12)  # deep wine

    level3_walls = []
    level3_enemies = []
    level3_energies = []
    level3_safes = []
    level3_hits = 0
    level3_energy_collected = 0
    level3_invuln_until = 0

    game.splash("LEVEL 3", "mRNA MAZE")
    game.splash("Collect 3 ATP", "Reach ribosome!")
    game.splash("Avoid RNase", "Safe zones heal")
    game.splash("3 hits = FAIL", "Clock is ticking")

    # Build the maze
    for r in range(LEVEL3_ROWS):
        for c in range(LEVEL3_COLS):
            ch = level3_layout[r][c]
            x, y = level3_tile_center(r, c)
            if ch == "#":
                w = sprites.create(wall_img(), WALL_KIND)
                w.set_position(x, y)
                w.set_flag(SpriteFlag.GHOST, False)
                level3_walls.append(w)
            elif ch == "S":
                level3_player = sprites.create(mrna_player_img(), SpriteKind.player)
                level3_player.set_position(x, y)
                controller.move_sprite(level3_player, 70, 70)
                level3_player.set_flag(SpriteFlag.STAY_IN_SCREEN, True)
            elif ch == "R":
                level3_ribosome = sprites.create(ribosome_img(), SpriteKind.food)
                level3_ribosome.set_position(x, y)
                level3_ribosome.data = "ribosome"
            elif ch == "E":
                e = sprites.create(atp_img(), SpriteKind.food)
                e.set_position(x, y)
                e.data = "energy"
                level3_energies.append(e)
            elif ch == "V":
                v = sprites.create(safe_zone_img(), SAFE_KIND)
                v.set_position(x, y)
                v.set_flag(SpriteFlag.GHOST, True)
                level3_safes.append(v)

    # Spawn 4 patrolling enzymes in specific open tiles
    enemy_spawn_rows = [0, 4, 6, 2]
    enemy_spawn_cols = [9, 1, 5, 4]
    for i in range(len(enemy_spawn_rows)):
        r = enemy_spawn_rows[i]
        c = enemy_spawn_cols[i]
        x, y = level3_tile_center(r, c)
        e = sprites.create(rnase_img(), SpriteKind.enemy)
        e.set_position(x, y)
        level3_enemies.append(e)

    # Yellow YOU label follows the mRNA player
    spawn_you_label()

    info.start_countdown(LEVEL3_TIME)
    info.on_countdown_end(on_level3_time_out)
    update_hud()
    sfx_level_up()

def on_level3_time_out():
    if current_level == 3 and game_running:
        game.splash("mRNA DEGRADED!", "Time's up.")
        lose_game("mRNA DEGRADATION")

def _level3_is_wall_tile(r, c):
    if r < 0 or c < 0 or r >= LEVEL3_ROWS or c >= LEVEL3_COLS:
        return True
    return level3_layout[r][c] == "#"

def level3_on_enemy_tick():
    # Each enzyme steps one tile toward the player along open paths
    if current_level != 3 or not game_running:
        return
    if level3_player is None:
        return
    for e in sprites.all_of_kind(SpriteKind.enemy):
        # Convert positions to tile indices
        er = int((e.y - LEVEL3_ORIGIN_Y + LEVEL3_TILE // 2) / LEVEL3_TILE)
        ec = int((e.x - LEVEL3_ORIGIN_X + LEVEL3_TILE // 2) / LEVEL3_TILE)
        pr = int((level3_player.y - LEVEL3_ORIGIN_Y + LEVEL3_TILE // 2) / LEVEL3_TILE)
        pc = int((level3_player.x - LEVEL3_ORIGIN_X + LEVEL3_TILE // 2) / LEVEL3_TILE)
        # BFS (simple greedy — try horizontal then vertical)
        dc = 0
        dr = 0
        if pc > ec and not _level3_is_wall_tile(er, ec + 1):
            dc = 1
        elif pc < ec and not _level3_is_wall_tile(er, ec - 1):
            dc = -1
        elif pr > er and not _level3_is_wall_tile(er + 1, ec):
            dr = 1
        elif pr < er and not _level3_is_wall_tile(er - 1, ec):
            dr = -1
        else:
            # try alternate axis if primary blocked
            if pr > er and not _level3_is_wall_tile(er + 1, ec):
                dr = 1
            elif pr < er and not _level3_is_wall_tile(er - 1, ec):
                dr = -1
        nx = e.x + dc * LEVEL3_TILE
        ny = e.y + dr * LEVEL3_TILE
        e.set_position(nx, ny)

def _safe_zone_step():
    # If player is standing on a safe zone, consume it: heal, +time, invuln.
    # Used safes are destroyed, so iterating sprites.all_of_kind(SAFE_KIND)
    # naturally skips them the next tick.
    global level3_invuln_until
    if level3_player is None:
        return
    for s in sprites.all_of_kind(SAFE_KIND):
        if abs(level3_player.x - s.x) < 8 and abs(level3_player.y - s.y) < 8:
            info.change_countdown_by(5)
            level3_invuln_until = game.runtime() + 1500
            heal(10)
            sfx_level_up()
            game.splash("SAFE ZONE", "+5s +10 HP")
            s.destroy(effects.cool_radial, 400)
            return

def level3_on_update():
    if current_level != 3 or not game_running:
        return
    _safe_zone_step()
    position_you_label(level3_player)

def on_mrna_hits_enzyme(sprite, other):
    global level3_hits, level3_invuln_until
    if current_level != 3:
        return
    # invulnerable window from safe zone?
    if game.runtime() < level3_invuln_until:
        return
    level3_hits = level3_hits + 1
    other.destroy(effects.fire, 400)
    take_damage(18)
    sfx_damage()
    game.splash("RNase HIT!", str(LEVEL3_HIT_LIMIT - level3_hits) + " hits left")
    if level3_hits >= LEVEL3_HIT_LIMIT:
        info.stop_countdown()
        game.splash("mRNA DEGRADED!", "Too many hits.")
        lose_game("mRNA DESTROYED")

def on_mrna_grabs_food(sprite, other):
    global level3_energy_collected
    if current_level != 3:
        return
    if other.data == "ribosome":
        if level3_energy_collected >= LEVEL3_ENERGY_NEEDED:
            info.stop_countdown()
            level3_win()
        else:
            needed = LEVEL3_ENERGY_NEEDED - level3_energy_collected
            sprite.say("need " + str(needed) + "!", 900)
        return
    if other.data == "energy":
        level3_energy_collected = level3_energy_collected + 1
        add_score(10)
        sfx_energy()
        other.destroy(effects.cool_radial, 250)

def level3_win():
    win_game()


# ==============================================================
#  10. WIN / LOSE SCREENS
# ==============================================================
def win_game():
    global game_running
    game_running = False
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(SpriteKind.projectile)
    scene.set_background_color(9)
    effects.confetti.start_screen_effect(3000)
    sfx_win()
    game.splash("* * * * * * *", "* YOU WIN! *")
    game.splash("CELL ALIVE!", "mRNA delivered.")

    # ---- Educational debrief: mRNA delivery & translation ----
    game.splash("WHAT JUST HAPPENED?", "mRNA Delivery")
    game.splash("mRNA travels from", "nucleus to ribosome")
    game.splash("dodging RNase enzymes", "that would chew it up.")
    game.splash("ATP orbs = energy", "your cell burns.")
    game.splash("Ribosome reads mRNA", "and builds PROTEINS.")
    game.splash("Proteins do", "EVERYTHING in you:")
    game.splash("hemoglobin, insulin,", "antibodies, muscle!")

    game.splash("REAL-WORLD USE #1:", "mRNA Therapeutics")
    game.splash("Scientists deliver", "custom mRNA to cells")
    game.splash("to make missing", "proteins on demand.")
    game.splash("Already used for:", "COVID, cancer, flu.")

    game.splash("REAL-WORLD USE #2:", "Gene Therapy")
    game.splash("For kids with SMA,", "a single dose delivers")
    game.splash("working mRNA and", "saves their lives.")

    game.splash("REAL-WORLD USE #3:", "Sickle Cell Cure")
    game.splash("FDA-approved 2023:", "Casgevy edits mRNA")
    game.splash("production to end", "sickle cell disease.")

    game.splash("THE CENTRAL DOGMA:", "DNA -> RNA -> Protein")
    game.splash("Every cell you have", "runs on this loop")
    game.splash("trillions of times", "every single day.")

    game.splash("FUN FACT:", "Your body makes")
    game.splash("about 2 million", "new proteins PER SECOND.")

    game.splash("FINAL SCORE", str(score))
    game.splash("Cell health", str(cell_health) + " / 100")
    game.splash("You are a cell!", "Keep it alive.")
    game.splash("Thanks for playing!", "- Cell Studio -")
    game.set_game_over_effect(True, effects.confetti)
    game.game_over(True)

def lose_game(reason):
    global game_running
    game_running = False
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(SpriteKind.projectile)
    scene.set_background_color(2)
    effects.dissolve.start_screen_effect(1200)
    sfx_death()
    game.splash("GAME OVER", reason)
    game.splash("FINAL SCORE", str(score))
    game.splash("Cell health", str(cell_health) + " / 100")
    game.set_game_over_effect(False, effects.dissolve)
    game.game_over(False)


# ==============================================================
#  11. CONTROLLER HANDLERS
# ==============================================================
def on_a():
    if current_level == 1:
        level1_on_a()
    elif current_level == 2:
        level2_on_a()

def on_b():
    if current_level == 1:
        level1_on_b()

controller.A.on_event(ControllerButtonEvent.PRESSED, on_a)
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b)


# ==============================================================
#  12. COLLISION HOOKS
# ==============================================================
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_mrna_hits_enzyme)
sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_mrna_grabs_food)

# Player vs walls in Level 3 — block movement
def on_player_wall(sprite, wall):
    # Push player back to previous tile center
    dx = sprite.x - wall.x
    dy = sprite.y - wall.y
    if abs(dx) > abs(dy):
        if dx > 0:
            sprite.x = wall.x + wall.width / 2 + sprite.width / 2 + 1
        else:
            sprite.x = wall.x - wall.width / 2 - sprite.width / 2 - 1
    else:
        if dy > 0:
            sprite.y = wall.y + wall.height / 2 + sprite.height / 2 + 1
        else:
            sprite.y = wall.y - wall.height / 2 - sprite.height / 2 - 1

sprites.on_overlap(SpriteKind.player, WALL_KIND, on_player_wall)


# ==============================================================
#  13. TIMERS / UPDATES
# ==============================================================
def on_update_tick():
    if current_level == 1:
        level1_on_update()
    elif current_level == 2:
        level2_on_on_update()
    elif current_level == 3:
        level3_on_update()

def level2_on_on_update():
    # alias — just calls level2_on_update
    level2_on_update()

game.on_update(on_update_tick)
game.on_update_interval(600, level3_on_enemy_tick)


# ==============================================================
#  14. INTRO + MAIN ENTRY
# ==============================================================
def intro():
    scene.set_background_color(1)
    game.splash("CELL STUDIO", "'A' to START")
    game.splash("You ARE a cell.", "Keep it alive.")
    game.splash("Three levels:", "Build - Transcribe - Deliver")
    game.splash("Controls:", "D-pad + A/B")
    sfx_level_up()

update_hud()
intro()
start_level1()
