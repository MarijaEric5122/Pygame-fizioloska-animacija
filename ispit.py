import pygame
import random
from pylsl import StreamInlet, resolve_streams
import time
import math

# Inicijalizacija pygame
pygame.init()

# Dimenzije ekrana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ispitni projekat - animacija sa cvecem")

# Definisanje boja
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)  
SPLASH_COLOR = (173, 216, 230)  
YELLOW = (255, 255, 0)  
PINK = (255, 105, 180)  

# Klasa za crtanje i animaciju cveta
class Flower:
    def __init__(self, x, y, base_width=80, base_height=200):
        self.x = x
        self.y = y
        self.base_width = base_width
        self.base_height = base_height
        self.width = base_width
        self.height = base_height
        self.hits = 0.0  # Broj pogodaka kapljica
        self.max_hits = 15.0  # Maksimalni broj pogodaka
        self.hits_decay_rate = 30.0  # Brzina opadanja efekta pogodaka

    # Crtanje cveta na ekranu
    def draw(self, surface):

        # Stablo cveta
        trunk_width = max(5, int(self.width / 3))
        trunk_height = int(self.height / 2)
        trunk_rect = pygame.Rect(self.x - trunk_width // 2, self.y - trunk_height, trunk_width, trunk_height)
        pygame.draw.rect(surface, GREEN, trunk_rect)  

        # Centar cveta
        center_radius = int(self.width * 0.3)
        pygame.draw.circle(surface, YELLOW, (self.x, self.y - trunk_height), center_radius)

        # Latice cveta
        num_petals = 6
        petal_radius = int(self.width * 0.4)
        for i in range(num_petals):
            angle_deg = i * (360 / num_petals)
            angle_rad = math.radians(angle_deg)
            petal_x = self.x + int((center_radius + petal_radius) * math.cos(angle_rad))
            petal_y = self.y - trunk_height + int((center_radius + petal_radius) * math.sin(angle_rad))
            pygame.draw.circle(surface, PINK, (petal_x, petal_y), petal_radius)

        additional_petals = [
            (-int(self.width * 0.4), -int(self.width * 0.4)),
            (int(self.width * 0.4), -int(self.width * 0.4)),
            (0, -int(self.width * 0.7))
        ]

        for offset in additional_petals:
            pygame.draw.circle(surface, PINK, (self.x + offset[0], self.y - trunk_height + offset[1]), int(petal_radius * 0.8))

    # Azuriranje velicine cveta na osnovu broja pogodaka kapljica
    def update(self, delta_time):
        # Smanji kapljice na osnovu vremena
        self.hits -= self.hits_decay_rate * delta_time
        if self.hits < 0.0:
            self.hits = 0.0

        # Racunanje nove velicine cveta
        target_scale = 1 + (self.hits / self.max_hits)  # Skaliranje izmedjuu 1 i 2
        target_width = self.base_width * target_scale
        target_height = self.base_height * target_scale

        # Postepena promena velicine cveta
        self.width += (target_width - self.width) * 0.1
        self.height += (target_height - self.height) * 0.1

        # Ogranicenje velicine cveta
        self.width = max(self.base_width * 0.5, min(self.base_width * 2, self.width))
        self.height = max(self.base_height * 0.5, min(self.base_height * 2, self.height))

# Maksimalan broj kapljica na ekranu
MAX_RAINDROPS = 1500  

# Kreiranje cvetova
num_flowers = 4  
flowers = []
spacing = SCREEN_WIDTH // (num_flowers + 1)

for i in range(num_flowers):
    x = spacing * (i + 1)
    y = SCREEN_HEIGHT - 100 
    flower = Flower(x, y)
    flowers.append(flower)

# Funkcija za kreiranje kapljica kise
def create_raindrop():
    x_position = random.randint(0, SCREEN_WIDTH)
    speed = random.randint(5, 15)  
    return {'x': x_position, 'y': 0, 'speed': speed}

# Funkcija za crtanje splash efekta
def draw_splash(surface, pos):
    pygame.draw.circle(surface, SPLASH_COLOR, pos, 5)
    pygame.draw.circle(surface, SPLASH_COLOR, pos, 3)
    pygame.draw.circle(surface, SPLASH_COLOR, pos, 1)

# Trazi LSL stream-ove
print("Tražim LSL streamove...")
streams = resolve_streams()

# Filtriranje stream-ova po imenu
target_stream = None
for stream in streams:
    if stream.name() == 'BreathingSignal':  
        target_stream = stream
        break

# Provera da li je pronadjen odgovarajuci stream
if target_stream:
    inlet = StreamInlet(target_stream)
    print("Prikljucen na stream:", target_stream.name())
else:
    print("Stream 'BreathingSignal' nije pronadjen!")
    pygame.quit()
    exit()

# Timer za ogranicavanje citanja LSL podataka
last_breath_time = time.time()
breath_interval = 0.25  

# Glavna petlja za animaciju
running = True
clock = pygame.time.Clock()
raindrops = []
splashes = []
while running:
    # Kontrola brzine petlje (60 FPS)
    delta_time = clock.tick(60) / 1000.0  

    current_time = time.time()
    # Azuriranje disajnog ritma
    if current_time - last_breath_time >= breath_interval:
        last_breath_time = current_time
        # Citanje podataka sa stream-a 
        try:
            sample, timestamp = inlet.pull_sample(timeout=0.0)  
            breathing_rate = sample[0]  # Koristi prvi uzorak kao indikator disajnog ritma
            print(f"Breathing Rate: {breathing_rate}")  
        except Exception as e:
            print(f"Greška pri citanju LSL signala: {e}")
            breathing_rate = 0  

        # Mapiranje disajnog ritma na broj kapljica
        raindrop_spawn_rate = max(0, int(breathing_rate * 1.5)) 
        raindrop_spawn_rate = min(raindrop_spawn_rate, 15)  # Maksimalno 15 kapljica po intervalu

        print(f"Raindrop Spawn Rate: {raindrop_spawn_rate}") 

        for _ in range(raindrop_spawn_rate):
            if len(raindrops) < MAX_RAINDROPS:
                raindrops.append(create_raindrop())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)  # Pozadinska boja

    # Azuriranje kapljica
    for drop in raindrops[:]:
        drop['y'] += drop['speed']  
        pygame.draw.circle(screen, BLUE, (drop['x'], drop['y']), 5) 

        # Provera "udara" sa cvecem
        hit_flower = False
        for flower in flowers:
            foliage_radius = flower.width
            foliage_center = (flower.x, flower.y - int(flower.height / 2))
            distance = math.hypot(drop['x'] - foliage_center[0], drop['y'] - foliage_center[1])
            if distance <= foliage_radius:
                # Simuliraj "udar" kapljice u cvece
                flower.hits += 2.0  
                flower.hits = min(flower.hits, flower.max_hits)  
                raindrops.remove(drop) 
                splashes.append({'pos': (drop['x'], drop['y'])})  
                hit_flower = True
                break  

        if not hit_flower and drop['y'] > SCREEN_HEIGHT:
            raindrops.remove(drop)

    # Azuriranje splash efekta
    for splash in splashes[:]:
        draw_splash(screen, splash['pos'])
        splashes.remove(splash)

    # Azuriranje cvetova
    for flower in flowers:
        flower.update(delta_time)
        flower.draw(screen)

    # Ogranici broj kapljica na ekranu
    if len(raindrops) > MAX_RAINDROPS:
        raindrops.pop(0)  

    # Osvezavanje ekrana
    pygame.display.flip()

pygame.quit()