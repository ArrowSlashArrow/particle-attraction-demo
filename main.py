import pygame
import numpy as np
import sys

# initialize pygame modules
pygame.init()
pygame.font.init()

# more init and global vars
WIDTH, HEIGHT = 800, 450 # 16:9 aspect ratio
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 30
font_size = 20
font = pygame.font.SysFont(pygame.font.get_fonts()[0], font_size)
num_particles = 2500

# gravitational constant for this sim
grav = 0.001 / (FPS*FPS)

# pointsof gravity
grav_points = []

# event handler function
def handle_events():
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key down event
        if event.type == pygame.KEYDOWN:
            match event.key:
                case _:
                    pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                grav_points.append(pygame.mouse.get_pos())

# particle class
class Particle:
    def __init__(self, pos, vel=[0, 0]):
        self.x, self.y = pos  # position of particle
        self.x_v, self.y_v = vel  # velocity of particle [currently only 0 at init]

    def update(self):
        # update with gravity using LODS
        total_gravity = [0, 0]

        # TODO: gravity
        
        
        # position of particle relative to cursor
        for pos in grav_points:
            rel_pos = [pos[0] - self.x, pos[1] - self.y]
            # get distance between particle and cursor
            dist = np.sqrt(rel_pos[0]**2 + rel_pos[1]**2)
            # compute force
            temp = max(float(dist) * float(dist), 1e-5)
            force = grav / temp
    
            # normal position to range of [-1, 1] for x and y force component
            factor = max(max(abs(rel_pos[0]), abs(rel_pos[1])), 1e-5)
            total_gravity[0] += rel_pos[0] / factor
            total_gravity[1] += rel_pos[1] / factor

        total_gravity[0] /= max(len(grav_points), 1)
        total_gravity[1] /= max(len(grav_points), 1)
    
        self.x_v += total_gravity[0]
        self.y_v += total_gravity[1]
        self.x += self.x_v
        self.y += self.y_v

    def render(self):
        screen.set_at((int(self.x), int(self.y)), (255, 255, 255))


# array of particles with random positions

particles = [Particle((np.random.randint(100, 120), np.random.randint(100, 120)), [1, 0]) for i in range(num_particles)]

# TODO: on click, place a point at location of mouse that attracts particles
# TODO #2: port to rust

# main loop
while True:
    # handle events
    handle_events()
    
    # clear screen
    screen.fill((0, 0, 0))

    # render grav_points
    for point in grav_points:
        pygame.draw.circle(screen, (255, 255, 255), point, 5)
    
    # update particles
    for particle in particles:
        particle.update()
        particle.render()

    # update screen
    pygame.display.flip()
    clock.tick(FPS)


"""
paper from which I learned to compute gravity:
https://www.sciencedirect.com/science/article/pii/0021999187901409

"""