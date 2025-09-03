import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.size = 20
    
    def flap(self):
        self.velocity = -8
    
    def update(self, score=0):
        # Gravity increases with score
        gravity = 0.5 + score * 0.02
        self.velocity += gravity
        self.y += self.velocity
    
    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)

class Pipe:
    def __init__(self, x, score=0):
        self.x = x
        # Gap gets smaller as score increases (minimum 180)
        self.gap = max(180, 250 - score * 5)
        self.top = random.randint(50, HEIGHT - self.gap - 100)
        self.bottom = self.top + self.gap
        self.width = 50
        # Speed increases with score
        self.speed = 2 + score * 0.1
    
    def update(self):
        self.x -= self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, self.width, HEIGHT - self.bottom))
    
    def collides(self, bird):
        if bird.x + bird.size > self.x and bird.x - bird.size < self.x + self.width:
            if bird.y - bird.size < self.top or bird.y + bird.size > self.bottom:
                return True
        return False

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    
    bird = Bird()
    pipes = [Pipe(WIDTH + i * 200, 0) for i in range(3)]
    score = 0
    font = pygame.font.Font(None, 36)
    game_over = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    bird = Bird()
                    pipes = [Pipe(WIDTH + i * 200, 0) for i in range(3)]
                    score = 0
                    game_over = False
        
        if not game_over:
            bird.update(score)
            
            # Check boundaries
            if bird.y < 0 or bird.y > HEIGHT:
                game_over = True
            
            # Update pipes
            for pipe in pipes[:]:
                pipe.update()
                if pipe.collides(bird):
                    game_over = True
                if pipe.x + pipe.width < 0:
                    pipes.remove(pipe)
                    rightmost_x = max(p.x for p in pipes) if pipes else WIDTH
                    # Pipes get closer together as score increases (minimum 150)
                    pipe_spacing = max(150, 200 - score * 2)
                    pipes.append(Pipe(rightmost_x + pipe_spacing, score))
                    score += 1
        
        # Draw everything
        screen.fill(WHITE)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("GAME OVER", True, BLACK)
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            restart_text = font.render("Press R to restart", True, BLACK)
            
            screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 60))
            screen.blit(final_score_text, (WIDTH//2 - 90, HEIGHT//2 - 20))
            screen.blit(restart_text, (WIDTH//2 - 100, HEIGHT//2 + 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
