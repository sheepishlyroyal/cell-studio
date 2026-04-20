# ============================================================
#  DNA: THE CODE OF LIFE
#  An educational biology game for Microsoft MakeCode Arcade
#  https://arcade.makecode.com/
#
#  HOW TO IMPORT:
#    1. Go to https://arcade.makecode.com/
#    2. Click "New Project"
#    3. Switch language from Blocks to PYTHON (top right)
#    4. Paste the ENTIRE contents of this file into the editor
#    5. Press the play button to run
#
#  LEVELS:
#    1 - DNA BUILDING   : Match the complementary base pairs (A-T, C-G)
#    2 - TRANSCRIPTION  : Drop RNA polymerase onto the promoter zone
#    3 - mRNA MAZE      : Dodge enzymes and collect energy
#    4 - TRANSLATION    : Choose the right amino acid for each codon
#
#  GLOBAL LOSE MECHANIC:
#    A Cell Health bar tracks mistakes across every level.
#    Zero health = cell death.
# ============================================================

# ---------- GLOBAL STATE ----------
current_level = 0
cell_health = 100
mutations = 0
energy = 0
score = 0
game_running = False
game_active_sprite = None
paused_input = False

# ---------- COLOR / LETTER MAPPING ----------
# A=red   T=blue   C=green   G=yellow   U=purple
# This links each letter to a color across the whole game
A_COLOR = 2   # red
T_COLOR = 8   # blue
C_COLOR = 7   # green
G_COLOR = 5   # yellow
U_COLOR = 11  # purple

# ---------- PIXEL ART IMAGES ----------
# Each nucleotide is drawn as a tiny sprite of the right color

def nucleotide_img(letter):
    if letter == "A":
        return img("""
            . . 2 2 2 2 . .
            . 2 2 2 2 2 2 .
            2 2 1 2 2 1 2 2
            2 2 2 2 2 2 2 2
            2 2 1 1 1 1 2 2
            2 2 2 2 2 2 2 2
            . 2 2 2 2 2 2 .
            . . 2 2 2 2 . .
        """)
    if letter == "T":
        return img("""
            . . 8 8 8 8 . .
            . 8 8 8 8 8 8 .
            8 8 1 8 8 1 8 8
            8 8 8 8 8 8 8 8
            8 8 1 1 1 1 8 8
            8 8 8 8 8 8 8 8
            . 8 8 8 8 8 8 .
            . . 8 8 8 8 . .
        """)
    if letter == "C":
        return img("""
            . . 7 7 7 7 . .
            . 7 7 7 7 7 7 .
            7 7 1 7 7 1 7 7
            7 7 7 7 7 7 7 7
            7 7 1 1 1 1 7 7
            7 7 7 7 7 7 7 7
            . 7 7 7 7 7 7 .
            . . 7 7 7 7 . .
        """)
    if letter == "G":
        return img("""
            . . 5 5 5 5 . .
            . 5 5 5 5 5 5 .
            5 5 1 5 5 1 5 5
            5 5 5 5 5 5 5 5
            5 5 1 1 1 1 5 5
            5 5 5 5 5 5 5 5
            . 5 5 5 5 5 5 .
            . . 5 5 5 5 . .
        """)
    # U (RNA)
    return img("""
        . . 11 11 11 11 . .
        . 11 11 11 11 11 11 .
        11 11 1 11 11 1 11 11
        11 11 11 11 11 11 11 11
        11 11 1 1 1 1 11 11
        11 11 11 11 11 11 11 11
        . 11 11 11 11 11 11 .
        . . 11 11 11 11 . .
    """)

def polymerase_img():
    return img("""
        . . 4 4 4 4 . .
        . 4 4 4 4 4 4 .
        4 4 4 1 1 4 4 4
        4 4 1 4 4 1 4 4
        4 4 1 4 4 1 4 4
        4 4 4 1 1 4 4 4
        . 4 4 4 4 4 4 .
        . . 4 4 4 4 . .
    """)

def mrna_img():
    return img("""
        . 11 11 . . 11 11 .
        11 11 11 11 11 11 11 11
        11 11 1 11 11 1 11 11
        11 11 11 11 11 11 11 11
        . 11 11 11 11 11 11 .
        . . 11 11 11 11 . .
    """)

def enzyme_img():
    return img("""
        . 10 10 10 10 10 10 .
        10 1 1 10 10 1 1 10
        10 1 1 10 10 1 1 10
        10 10 10 10 10 10 10 10
        10 10 1 10 10 1 10 10
        10 10 10 1 1 10 10 10
        . 10 10 10 10 10 10 .
        . . 10 10 10 10 . .
    """)

def energy_img():
    return img("""
        . . 4 4 4 . .
        . 4 5 5 5 4 .
        4 5 5 5 5 5 4
        4 5 1 5 1 5 4
        4 5 5 5 5 5 4
        . 4 5 5 5 4 .
        . . 4 4 4 . .
    """)

def ribosome_img():
    return img("""
        . 3 3 3 3 3 3 3 3 3 .
        3 3 6 6 3 3 3 6 6 3 3
        3 6 6 6 6 3 6 6 6 6 3
        3 6 6 6 6 6 6 6 6 6 3
        3 3 6 6 6 6 6 6 6 3 3
        . 3 3 6 6 6 6 6 3 3 .
        . . 3 3 6 6 6 3 3 . .
        . . . 3 3 3 3 3 . . .
    """)

def cell_img():
    return img("""
        . . . 6 6 6 6 6 6 . . .
        . 6 6 6 6 6 6 6 6 6 6 .
        6 6 6 6 6 6 6 6 6 6 6 6
        6 6 6 6 6 6 6 6 6 6 6 6
        6 6 6 6 6 6 6 6 6 6 6 6
        . 6 6 6 6 6 6 6 6 6 6 .
        . . . 6 6 6 6 6 6 . . .
    """)


# ---------- SOUND EFFECTS ----------
# MakeCode provides sound via music.play_melody and music.tone_playable
# We build our own library of tiny effect phrases

def sfx_correct():
    music.play(music.tone_playable(523, music.beat(BeatFraction.HALF)), music.PlaybackMode.IN_BACKGROUND)
    music.play(music.tone_playable(784, music.beat(BeatFraction.HALF)), music.PlaybackMode.IN_BACKGROUND)

def sfx_wrong():
    music.play(music.tone_playable(196, music.beat(BeatFraction.QUARTER)), music.PlaybackMode.UNTIL_DONE)
    music.play(music.tone_playable(147, music.beat(BeatFraction.QUARTER)), music.PlaybackMode.UNTIL_DONE)

def sfx_bond():
    music.play(music.tone_playable(880, music.beat(BeatFraction.EIGHTH)), music.PlaybackMode.IN_BACKGROUND)

def sfx_energy():
    music.play(music.tone_playable(1046, music.beat(BeatFraction.EIGHTH)), music.PlaybackMode.IN_BACKGROUND)

def sfx_damage():
    music.play(music.tone_playable(110, music.beat(BeatFraction.HALF)), music.PlaybackMode.UNTIL_DONE)

def sfx_level_up():
    music.play_melody("C5 E5 G5 C6", 200)

def sfx_death():
    music.play_melody("C5 B A G F E D C C3", 180)

def sfx_win():
    music.play_melody("C E G C5 E5 G5 C6", 160)

# Background loops -- each level gets its own vibe
def theme_level1():
    music.play_melody("C D E G - E D C - G E D C", 120)

def theme_level2():
    music.play_melody("E G B D5 - D5 B G E - G B D5", 150)

def theme_level3():
    music.play_melody("F A C5 F5 - F5 C5 A F - A C5 F5", 170)

def theme_level4():
    music.play_melody("G B D5 G5 - G5 D5 B G - B D5 G5", 140)


# ---------- HUD / CELL HEALTH ----------
def update_hud():
    info.set_score(score)
    info.set_life(cell_health // 10)

def take_damage(amount):
    global cell_health
    cell_health = cell_health - amount
    sfx_damage()
    scene.camera_shake(6, 400)
    if cell_health <= 0:
        cell_health = 0
        update_hud()
        game_over()
    else:
        update_hud()

def heal(amount):
    global cell_health
    cell_health = cell_health + amount
    if cell_health > 100:
        cell_health = 100
    update_hud()


# ---------- GAME OVER ----------
def game_over():
    global game_running
    game_running = False
    sfx_death()
    scene.set_background_color(2)
    game.set_game_over_effect(False, effects.dissolve)
    game.game_over(False)


# ---------- LEVEL 1: DNA BUILDING ----------
# Player sees a left strand (template) and must pick the
# complementary base for each slot on the right strand.

template_sequence = ["A", "T", "C", "G", "A", "T"]
expected_pairs = {"A": "T", "T": "A", "C": "G", "G": "C"}
selected_index = 0
cursor_sprite = None
level1_slots = []
level1_placed = []
available_bases = ["A", "T", "C", "G"]
current_pick = 0
pick_sprite = None
bond_sprites = []

def start_level1():
    global current_level, selected_index, current_pick
    current_level = 1
    selected_index = 0
    current_pick = 0
    scene.set_background_color(15)
    game.splash("LEVEL 1", "Build the DNA strand")
    game.splash("A pairs with T", "C pairs with G")
    theme_level1()
    build_level1_board()

def build_level1_board():
    global cursor_sprite, pick_sprite, level1_slots, level1_placed, bond_sprites
    scene.set_background_color(15)
    # Clear any old sprites
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    level1_slots = []
    level1_placed = []
    bond_sprites = []

    # Draw the template strand on the left
    y = 20
    for i in range(len(template_sequence)):
        base = template_sequence[i]
        s = sprites.create(nucleotide_img(base), SpriteKind.food)
        s.x = 40
        s.y = y + i * 15
        level1_slots.append(s)

        # Empty placeholder on the right
        slot = sprites.create(img("""
            1 1 1 1 1 1 1 1
            1 . . . . . . 1
            1 . . . . . . 1
            1 . . . . . . 1
            1 . . . . . . 1
            1 . . . . . . 1
            1 . . . . . . 1
            1 1 1 1 1 1 1 1
        """), SpriteKind.enemy)
        slot.x = 120
        slot.y = y + i * 15
        level1_placed.append(None)

    # Cursor marker
    cursor_sprite = sprites.create(img("""
        . . 5 5 . .
        . 5 5 5 5 .
        5 5 5 5 5 5
        5 5 5 5 5 5
        . 5 5 5 5 .
        . . 5 5 . .
    """), SpriteKind.projectile)
    cursor_sprite.x = 120
    cursor_sprite.y = 20

    # Pick menu (cycles through A/T/C/G)
    pick_sprite = sprites.create(nucleotide_img(available_bases[current_pick]), SpriteKind.player)
    pick_sprite.x = 80
    pick_sprite.y = 110

    game.show_long_text("Left + Right to change base.  A to cycle.  B to place.", DialogLayout.BOTTOM)


def level1_change_slot(direction):
    global selected_index
    selected_index = selected_index + direction
    if selected_index < 0:
        selected_index = 0
    if selected_index >= len(template_sequence):
        selected_index = len(template_sequence) - 1
    cursor_sprite.y = 20 + selected_index * 15

def level1_cycle_pick():
    global current_pick
    current_pick = (current_pick + 1) % len(available_bases)
    pick_sprite.set_image(nucleotide_img(available_bases[current_pick]))
    music.play(music.tone_playable(440, music.beat(BeatFraction.SIXTEENTH)), music.PlaybackMode.IN_BACKGROUND)

def level1_place():
    global score, mutations
    if level1_placed[selected_index] is not None:
        return
    chosen = available_bases[current_pick]
    template = template_sequence[selected_index]
    correct = expected_pairs[template]
    if chosen == correct:
        # Place the correct sprite
        placed = sprites.create(nucleotide_img(chosen), SpriteKind.food)
        placed.x = 120
        placed.y = 20 + selected_index * 15
        level1_placed[selected_index] = placed
        score = score + 10
        sfx_correct()
        # Animate hydrogen bond
        bond = sprites.create(img("""
            1 1 1 1 1 1 1 1
        """), SpriteKind.projectile)
        bond.x = 80
        bond.y = 20 + selected_index * 15
        bond_sprites.append(bond)
        sfx_bond()
        update_hud()
        if all_slots_filled():
            sfx_level_up()
            heal(10)
            pause(800)
            start_level2()
    else:
        mutations = mutations + 1
        take_damage(15)
        game.show_long_text("MUTATION! " + template + " does not pair with " + chosen, DialogLayout.BOTTOM)
        if mutations >= 3:
            game.show_long_text("DNA DAMAGE DETECTED", DialogLayout.CENTER)
            take_damage(30)

def all_slots_filled():
    for p in level1_placed:
        if p is None:
            return False
    return True


# ---------- LEVEL 2: TRANSCRIPTION ----------
# A moving RNA-polymerase droplet bounces across the screen.
# Player must press A when it overlaps the glowing promoter zone.

polymerase_sprite = None
promoter_zone = None
polymerase_speed = 60
level2_attempts = 0
level2_hits = 0

def start_level2():
    global current_level, polymerase_sprite, promoter_zone, polymerase_speed
    global level2_attempts, level2_hits
    current_level = 2
    level2_attempts = 0
    level2_hits = 0
    polymerase_speed = 60
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.projectile)
    scene.set_background_color(9)
    game.splash("LEVEL 2", "Transcription")
    game.splash("Press A when the droplet", "crosses the promoter zone!")
    theme_level2()

    # Promoter zone
    promoter_zone = sprites.create(img("""
        5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
        5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
        5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
    """), SpriteKind.food)
    promoter_zone.x = 80
    promoter_zone.y = 60

    # DNA background strand
    y = 55
    for i in range(10):
        s = sprites.create(nucleotide_img(template_sequence[i % len(template_sequence)]), SpriteKind.enemy)
        s.x = 10 + i * 15
        s.y = y

    # Polymerase droplet
    polymerase_sprite = sprites.create(polymerase_img(), SpriteKind.projectile)
    polymerase_sprite.y = 30
    polymerase_sprite.x = 10
    polymerase_sprite.vx = polymerase_speed
    polymerase_sprite.set_bounce_on_wall(True)

def level2_check_drop():
    global level2_attempts, level2_hits, polymerase_speed
    level2_attempts = level2_attempts + 1
    if polymerase_sprite is None:
        return
    diff = polymerase_sprite.x - promoter_zone.x
    if diff < 0:
        diff = -diff
    if diff < 20:
        level2_hits = level2_hits + 1
        sfx_correct()
        # Visual: strands separate
        effects.star_field.start_screen_effect(1000)
        polymerase_speed = polymerase_speed + 20
        polymerase_sprite.vx = polymerase_speed
        if level2_hits >= 3:
            sfx_level_up()
            heal(15)
            pause(800)
            start_level3()
    else:
        take_damage(15)
        game.show_long_text("Missed the promoter!", DialogLayout.BOTTOM)
        if level2_attempts - level2_hits >= 3:
            game.show_long_text("Transcription failed — cell is shutting down", DialogLayout.CENTER)
            take_damage(25)


# ---------- LEVEL 3: mRNA MAZE ----------
# The mRNA sprite travels from the nucleus (top) down to the ribosome (bottom)
# while the player dodges enzyme hazards and collects energy points.

mrna_sprite = None
ribosome_sprite = None
enzyme_spawner = None
energy_spawner = None
level3_timer = 30
level3_energy_required = 5
level3_energy_collected = 0

def start_level3():
    global current_level, mrna_sprite, ribosome_sprite
    global level3_timer, level3_energy_required, level3_energy_collected
    current_level = 3
    level3_timer = 30
    level3_energy_required = 5
    level3_energy_collected = 0
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.projectile)
    scene.set_background_color(11)
    game.splash("LEVEL 3", "mRNA Maze")
    game.splash("Reach the ribosome!", "Dodge enzymes, grab energy.")
    theme_level3()

    mrna_sprite = sprites.create(mrna_img(), SpriteKind.player)
    mrna_sprite.x = 80
    mrna_sprite.y = 20
    controller.move_sprite(mrna_sprite, 100, 100)

    ribosome_sprite = sprites.create(ribosome_img(), SpriteKind.food)
    ribosome_sprite.x = 80
    ribosome_sprite.y = 110

    info.start_countdown(level3_timer)

def spawn_enzyme():
    e = sprites.create(enzyme_img(), SpriteKind.enemy)
    e.x = randint(10, 150)
    e.y = 0
    e.vy = randint(30, 70)
    e.set_flag(SpriteFlag.AUTO_DESTROY, True)

def spawn_energy():
    e = sprites.create(energy_img(), SpriteKind.food)
    e.x = randint(10, 150)
    e.y = randint(20, 100)
    e.set_flag(SpriteFlag.GHOST, False)


# ---------- LEVEL 4: TRANSLATION ----------
# Show a codon (3 nucleotides), present 3 amino-acid options.
# Player picks the correct one. Three correct picks = protein formed.

codon_table = [
    ["AUG", "Met"],
    ["UUU", "Phe"],
    ["CAU", "His"],
    ["GCA", "Ala"],
    ["UAC", "Tyr"],
]
level4_round = 0
level4_correct = 0
level4_options = []
level4_codon_sprites = []
level4_option_sprites = []
level4_selected_option = 0
level4_highlight_sprite = None

fake_amino_pool = ["Met", "Phe", "His", "Ala", "Tyr", "Leu", "Ser", "Val", "Gly", "Lys"]

def start_level4():
    global current_level, level4_round, level4_correct
    current_level = 4
    level4_round = 0
    level4_correct = 0
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.projectile)
    scene.set_background_color(4)
    game.splash("LEVEL 4", "Translation")
    game.splash("Match codons to amino acids", "Left/Right to choose, A to pick")
    theme_level4()
    next_translation_round()

def next_translation_round():
    global level4_options, level4_selected_option, level4_codon_sprites, level4_option_sprites, level4_round, level4_highlight_sprite
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.projectile)
    if level4_round >= len(codon_table):
        win_game()
        return

    codon_str = codon_table[level4_round][0]
    correct_amino = codon_table[level4_round][1]

    # Draw the 3 codon nucleotides
    level4_codon_sprites = []
    for i in range(3):
        letter = codon_str[i]
        s = sprites.create(nucleotide_img(letter), SpriteKind.enemy)
        s.x = 50 + i * 20
        s.y = 40
        level4_codon_sprites.append(s)

    # Build options (1 correct + 2 fake)
    options = [correct_amino]
    tries = 0
    while len(options) < 3 and tries < 20:
        tries = tries + 1
        pick = fake_amino_pool[randint(0, len(fake_amino_pool) - 1)]
        if pick not in options:
            options.append(pick)
    # Shuffle
    for i in range(len(options)):
        j = randint(0, len(options) - 1)
        tmp = options[i]
        options[i] = options[j]
        options[j] = tmp
    level4_options = options
    level4_selected_option = 0
    level4_option_sprites = []

    # Render option text boxes as colored tiles; text via console-overlay
    for i in range(3):
        tile = sprites.create(img("""
            1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 6 6 6 6 6 6 6 6 6 6 6 6 1
            1 6 6 6 6 6 6 6 6 6 6 6 6 1
            1 6 6 6 6 6 6 6 6 6 6 6 6 1
            1 6 6 6 6 6 6 6 6 6 6 6 6 1
            1 6 6 6 6 6 6 6 6 6 6 6 6 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1
        """), SpriteKind.food)
        tile.x = 30 + i * 50
        tile.y = 90
        tile.say(options[i], 0)
        level4_option_sprites.append(tile)

    # Create a bright highlight arrow that sits above the selected option
    level4_highlight_sprite = sprites.create(img("""
        . . 5 5 5 5 . .
        . 5 5 5 5 5 5 .
        5 5 5 5 5 5 5 5
        . 5 5 5 5 5 5 .
        . . 5 5 5 5 . .
        . . . 5 5 . . .
    """), SpriteKind.projectile)
    level4_highlight_sprite.y = 75
    level4_highlight_option()

def level4_highlight_option():
    # Move the highlight arrow over the currently selected option.
    # Avoids set_scale, which is unreliable in some MakeCode Arcade builds.
    if level4_highlight_sprite is None:
        return
    if level4_selected_option < 0 or level4_selected_option >= len(level4_option_sprites):
        return
    target = level4_option_sprites[level4_selected_option]
    level4_highlight_sprite.x = target.x
    level4_highlight_sprite.y = target.y - 16

def level4_move_option(direction):
    global level4_selected_option
    level4_selected_option = level4_selected_option + direction
    if level4_selected_option < 0:
        level4_selected_option = 0
    if level4_selected_option >= 3:
        level4_selected_option = 2
    level4_highlight_option()
    music.play(music.tone_playable(440, music.beat(BeatFraction.SIXTEENTH)), music.PlaybackMode.IN_BACKGROUND)

def level4_confirm():
    global level4_round, level4_correct, score
    correct_amino = codon_table[level4_round][1]
    chosen = level4_options[level4_selected_option]
    if chosen == correct_amino:
        sfx_correct()
        level4_correct = level4_correct + 1
        score = score + 20
        update_hud()
        level4_round = level4_round + 1
        pause(500)
        next_translation_round()
    else:
        sfx_wrong()
        take_damage(20)
        game.show_long_text(chosen + " does not code for " + correct_amino, DialogLayout.BOTTOM)


# ---------- WIN ----------
def win_game():
    global game_running
    game_running = False
    sfx_win()
    scene.set_background_color(5)
    game.show_long_text("Protein synthesized!", DialogLayout.CENTER)
    game.show_long_text("You have traveled the Central Dogma:", DialogLayout.CENTER)
    game.show_long_text("DNA -> RNA -> Protein.  Final score: " + str(score), DialogLayout.CENTER)
    game.set_game_over_effect(True, effects.confetti)
    game.game_over(True)


# ---------- CONTROLLER HANDLERS ----------
def on_left():
    if current_level == 1:
        level1_change_slot(-1)
    if current_level == 4:
        level4_move_option(-1)

def on_right():
    if current_level == 1:
        level1_change_slot(1)
    if current_level == 4:
        level4_move_option(1)

def on_a():
    if current_level == 1:
        level1_cycle_pick()
    if current_level == 2:
        level2_check_drop()
    if current_level == 4:
        level4_confirm()

def on_b():
    if current_level == 1:
        level1_place()

controller.left.on_event(ControllerButtonEvent.PRESSED, on_left)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a)
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b)


# ---------- COLLISION HANDLERS (Level 3) ----------
def on_mrna_hits_enzyme(sprite, other):
    other.destroy(effects.fire, 300)
    take_damage(20)
    sfx_damage()

def on_mrna_grabs_energy(sprite, other):
    global level3_energy_collected, score
    if current_level != 3:
        return
    if other == ribosome_sprite:
        if level3_energy_collected >= level3_energy_required:
            sfx_level_up()
            heal(20)
            start_level4()
        else:
            game.show_long_text("Collect more energy first!", DialogLayout.BOTTOM)
        return
    level3_energy_collected = level3_energy_collected + 1
    score = score + 5
    update_hud()
    sfx_energy()
    other.destroy(effects.cool_radial, 200)

sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_mrna_hits_enzyme)
sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_mrna_grabs_energy)


# ---------- TIMERS ----------
def on_tick_spawn_enzyme():
    if current_level == 3:
        spawn_enzyme()

def on_tick_spawn_energy():
    if current_level == 3:
        spawn_energy()

game.on_update_interval(900, on_tick_spawn_enzyme)
game.on_update_interval(1500, on_tick_spawn_energy)


# ---------- MAIN INTRO ----------
def intro():
    scene.set_background_color(1)
    game.splash("DNA: CODE OF LIFE", "An educational biology game")
    game.splash("Cell health = lives.", "Mistakes damage the cell.")
    game.splash("Press any button to begin", "")
    sfx_level_up()

update_hud()
intro()
start_level1()
game_running = True
