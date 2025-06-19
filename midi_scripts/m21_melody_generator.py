import random
import music21 as m21
import os

# === MOTIF & RHYTHM HELPERS ===

def generate_motif(scale_pitches, length=3):
    motif = []
    current_pitch = random.choice(scale_pitches)
    motif.append(current_pitch)
    for _ in range(length - 1):
        step = random.choice([-2, -1, 1, 2])
        next_pitch = current_pitch + step
        while next_pitch not in scale_pitches:
            step = random.choice([-2, -1, 1, 2])
            next_pitch = current_pitch + step
        motif.append(next_pitch)
        current_pitch = next_pitch
    return motif

def generate_rhythm_pattern():
    return random.choice([
        [1, 1, 2],
        [0.5, 0.5, 1, 2],
        [0.25, 0.25, 0.5, 1],
        [1, 0.5, 1.5, 1]
    ])

def generate_chord_progression(key):
    tonic = key.tonic
    scale = key.getScale()
    degrees = [1, 4, 5, 1]

    chords = []
    for deg in degrees:
        pitch = scale.pitchFromDegree(deg)
        triad = m21.chord.Chord([
            pitch,
            pitch.transpose('M3') if key.mode == 'major' else pitch.transpose('m3'),
            pitch.transpose('P5')
        ])
        chords.append(triad)

    return chords

# === MAIN MELODY GENERATOR ===

def generate_melody_v2(
    bars=4,
    scale_name="C major",
    energy=0.5,
    output_file="improved_melody.mid"
):
    # Parse key and scale
    parts = scale_name.split()
    key_name = parts[0]
    mode_name = 'major' if len(parts) == 1 else ' '.join(parts[1:])
    key = m21.key.Key(key_name, mode_name)
    scale = key.getScale()
    scale_pitches = [p.midi for p in scale.getPitches('C3', 'C6')]

    # Start stream
    melody = m21.stream.Stream()
    melody.append(m21.meter.TimeSignature('4/4'))
    melody.append(key)
    tempo = 60 + energy * 80
    melody.append(m21.tempo.MetronomeMark(number=tempo))

    # Harmony and rhythm
    progression = generate_chord_progression(key)
    current_position = 0
    total_length = bars * 4

    while current_position < total_length:
        chord = progression[int(current_position // 4) % len(progression)]
        melody.append(m21.chord.Chord(chord.pitches))


        motif = generate_motif(scale_pitches, length=3)
        rhythm = generate_rhythm_pattern()
        for pitch, dur in zip(motif, rhythm):
            if current_position + dur > total_length:
                break

            note = m21.note.Note(pitch)
            note.quarterLength = dur

            # Phrasing
            if dur >= 1 and random.random() < 0.5:
                note.dynamic = m21.dynamics.Dynamic('mf')
            elif random.random() < 0.3:
                note.articulations.append(m21.articulations.Staccato())

            # Velocity variation
            base_velocity = 64 + int(energy * 30)
            variation = int(random.uniform(-10, 10))
            note.volume.velocity = max(0, min(127, base_velocity + variation))

            melody.append(note)
            current_position += dur

    # Expand the output file path
    if output_file:
        output_file = os.path.expanduser(output_file)
        melody.write('midi', fp=output_file)

    return melody

# === DEMO ===

def demo_melody_generator_v2():
    print("Generating calm melody...")
    generate_melody_v2(
        bars=8,
        scale_name="C major",
        energy=0.2,
        output_file="C:/Users/Kenrm/repositories/music-prod/midi_scripts/py_midi_files/calm_melody_v2.mid"
    )

    print("Generating energetic melody...")
    generate_melody_v2(
        bars=8,
        scale_name="A minor",
        energy=0.85,
        output_file="C:/Users/Kenrm/repositories/music-prod/midi_scripts/py_midi_files/energetic_melody_v2.mid"
    )

    print("Generating dreamy lydian melody...")
    generate_melody_v2(
        bars=8,
        scale_name="F lydian",
        energy=0.4,
        output_file="C:/Users/Kenrm/repositories/music-prod/midi_scripts/py_midi_files/lydian_dream_v2.mid"
    )

if __name__ == "__main__":
    demo_melody_generator_v2()
