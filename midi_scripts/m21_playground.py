from music21 import stream, note, chord, scale
import random

# Create a C major scale to pick notes from
c_major = scale.MajorScale('C')
scale_notes = c_major.getPitches('C4', 'C5')  # One octave of notes

# Create a stream to hold our music
melody = stream.Stream()

# Generate a simple melody with 16 notes
for i in range(16):
    # Pick a random note from our scale
    random_note = random.choice(scale_notes)
    
    # Create a note with quarter note duration
    n = note.Note(random_note)
    n.quarterLength = 0.5  # Eighth notes
    
    # Add note to our melody
    melody.append(n)

# Save as MIDI file
melody.write('midi', fp=r'.mid')