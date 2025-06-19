import pygame
import numpy as np
from pygame import gfxdraw
import librosa
import random
import math
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EDM Visualizer")

# Load and process audio
def load_audio(file_path):
    # Load the audio file with librosa
    y, sr = librosa.load(file_path)
    
    # Get various audio features
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    
    # Extract onset strength (for detecting "hits" in the music)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    
    # Get spectral features 
    spectral = np.abs(librosa.stft(y))
    
    return {
        'y': y,
        'sr': sr,
        'tempo': tempo,
        'beat_times': beat_times,
        'onset_env': onset_env,
        'spectral': spectral
    }

# Particle class for visual effects
class Particle:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.life = 255
        self.decay = random.uniform(1, 5)
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= self.decay
        self.size *= 0.98
        
    def draw(self, surface):
        if self.life > 0 and self.size > 0.5:
            alpha = int(self.life)
            color = (self.color[0], self.color[1], self.color[2], alpha)
            gfxdraw.filled_circle(surface, int(self.x), int(self.y), int(self.size), color)
            
    def is_dead(self):
        return self.life <= 0 or self.size <= 0.5

# Main visualization function
def visualize_music(audio_file):
    # Load audio data
    audio_data = load_audio(audio_file)
    
    # Create pygame mixer to play the audio
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    
    # Setup visualization elements
    spectrum_bars = 64
    particles = []
    
    # Create a transparent surface for particles
    particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Start the music
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Calculate current position in the song
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        if current_time >= len(audio_data['y']) / audio_data['sr']:
            running = False
            continue
        
        # Find current frame in audio data
        frame_idx = int(current_time * audio_data['sr'] / 512)  # Assuming hop_length of 512
        if frame_idx >= len(audio_data['onset_env']):
            frame_idx = len(audio_data['onset_env']) - 1
            
        # Get current spectrum data and onset strength
        if frame_idx < audio_data['spectral'].shape[1]:
            spectrum = audio_data['spectral'][:, frame_idx]
            spectrum = librosa.amplitude_to_db(spectrum, ref=np.max)
            spectrum = np.interp(spectrum, [np.min(spectrum), np.max(spectrum)], [0, HEIGHT/2])
        else:
            spectrum = np.zeros(spectrum_bars)
            
        onset = audio_data['onset_env'][frame_idx] if frame_idx < len(audio_data['onset_env']) else 0
        
        # Check if we're on a beat
        on_beat = False
        for beat_time in audio_data['beat_times']:
            if abs(current_time - beat_time) < 0.05:
                on_beat = True
                break
                
        # Clear the screen
        screen.fill((0, 0, 0))
        particle_surface.fill((0, 0, 0, 0))
        
        # Draw spectrum analyzer
        bar_width = WIDTH // spectrum_bars
        for i in range(spectrum_bars):
            if i < len(spectrum):
                bar_height = max(5, int(spectrum[i]))
                # Calculate color based on height (blue to pink gradient)
                hue = int(180 + (bar_height / (HEIGHT/2) * 60))
                color = pygame.Color(0, 0, 0)
                color.hsva = (hue % 360, 80, 90, 100)
                
                pygame.draw.rect(screen, color, 
                                (i * bar_width, HEIGHT - bar_height, 
                                 bar_width - 2, bar_height))
        
        # Create particles on beats or high onset strength
        if on_beat or onset > np.mean(audio_data['onset_env']) * 1.5:
            particle_count = int(onset * 5 * 0.5)  # Reduce particle count by 50%
            for _ in range(particle_count):
                # Random colors that match EDM aesthetic
                colors = [
                    (255, 0, 220, 255),  # Magenta
                    (0, 255, 220, 255),  # Cyan
                    (255, 220, 0, 255),  # Yellow
                    (120, 0, 255, 255),  # Purple
                ]
                color = random.choice(colors)
                
                # Create particles from center or from bars
                if random.random() > 0.5:
                    x, y = WIDTH // 2, HEIGHT // 2
                else:
                    bar_idx = random.randint(0, spectrum_bars - 1)
                    if bar_idx < len(spectrum):
                        x = bar_idx * bar_width + bar_width // 2
                        y = HEIGHT - int(spectrum[bar_idx])
                    else:
                        x, y = WIDTH // 2, HEIGHT // 2
                
                size = random.randint(5, 15)
                speed = random.uniform(2, 8)
                particles.append(Particle(x, y, size, color, speed))
        
        # Update and draw particles
        for p in particles[:]:
            p.update()
            p.draw(particle_surface)
            if p.is_dead():
                particles.remove(p)
        
        # Draw the particle surface
        screen.blit(particle_surface, (0, 0))
        
        # Draw a center circle that pulses with the music
        circle_radius = 50 + int(onset * 10)
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), circle_radius, 2)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

    
# Run the visualization (replace with your EDM track)
if __name__ == "__main__":
    audio_file = "C:/Users/Kenrm/repositories/music-prod/vis_scripts/1541365_Move_For_Me_DJ_Hero_Mix.mp3"
    visualize_music(audio_file)
