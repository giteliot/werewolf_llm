import pygame
import sys
import math
from const import *
from io_utils import load_game_log

class WerewolfGame:
    def __init__(self, log_file_path):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Werewolf Game Replay")
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.clock = pygame.time.Clock()
        
        self.background_day = pygame.image.load('./img/background_day.png').convert()
        self.background_day = pygame.transform.scale(self.background_day, (WIDTH, HEIGHT))
        self.background_night = pygame.image.load('./img/background_night.png').convert()
        self.background_night = pygame.transform.scale(self.background_night, (WIDTH, HEIGHT))
        
        self.game_log = load_game_log(log_file_path)
        self.setup_players()
        self.setup_game_state()
        self.is_night = True
        
    def setup_players(self):
        self.players = ["deepseek", "grok", "sonnet", "gemini", "gpt4"]
        self.num_players = len(self.players)
        self.circle_center = (WIDTH // 2, HEIGHT // 2 + 150)
        self.circle_radius = 200
        self.player_positions = self.compute_player_positions()
        
    def compute_player_positions(self):
        positions = {}
        angle_offset = -math.pi / 2
        for i, name in enumerate(self.players):
            angle = angle_offset + (2 * math.pi * i / self.num_players)
            x = self.circle_center[0] + self.circle_radius * math.cos(angle)
            y = self.circle_center[1] + self.circle_radius * math.sin(angle) - 100
            positions[name.lower()] = (int(x), int(y))
        return positions
    
    def setup_game_state(self):
        self.current_line_index = 0
        self.time_per_line = 2000
        self.last_update = pygame.time.get_ticks()
        
    def draw_text_box(self, text, box_rect, text_color, box_color, padding=10):
        pygame.draw.rect(self.screen, box_color, box_rect, border_radius=5)
        
        words = text.split(' ')
        lines = []
        current_line = ""
        max_text_width = box_rect.width - 2 * padding
        
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] > max_text_width:
                lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line = test_line
        lines.append(current_line.strip())
        
        y_offset = box_rect.top + padding
        for line in lines:
            rendered = self.font.render(line, True, text_color)
            self.screen.blit(rendered, (box_rect.left + padding, y_offset))
            y_offset += self.font.get_linesize()
            
    def draw_players(self):
        for name, pos in self.player_positions.items():
            pygame.draw.circle(self.screen, PLAYER_COLOR, pos, PLAYER_RADIUS)
            name_text = self.font.render(name.capitalize(), True, WHITE)
            text_rect = name_text.get_rect(center=(pos[0], pos[1] + PLAYER_RADIUS + 15))
            self.screen.blit(name_text, text_rect)
            
    def get_text_box_position(self, speaker):
        if speaker.lower() == "narrator":
            box_width = 400
            box_height = 100
            box_x = WIDTH // 2 - box_width // 2
            box_y = HEIGHT // 2 - box_height // 2
        else:
            pos = self.player_positions.get(speaker.lower(), (WIDTH // 2, HEIGHT // 2))
            box_width = 300
            box_height = 80
            box_x = pos[0] - box_width // 2
            box_y = pos[1] - PLAYER_RADIUS - box_height - 10
            
        return pygame.Rect(box_x, box_y, box_width, box_height)
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.time_per_line:
            self.current_line_index = (self.current_line_index + 1) % len(self.game_log)
            if "The night falls." in self.game_log[self.current_line_index]:
                self.is_night = True
            elif "The day rises." in self.game_log[self.current_line_index]:
                self.is_night = False
            self.last_update = current_time
            
    def draw(self):
        if self.is_night:
            self.screen.blit(self.background_night, (0, 0))
        else:
            self.screen.blit(self.background_day, (0, 0))
        self.draw_players()
        
        line = self.game_log[self.current_line_index]
        if ":" in line:
            speaker, message = line.split(":", 1)
            speaker = speaker.strip()
            message = message.strip().strip('"')
        else:
            speaker = "Narrator"
            message = line
            
        text_box_rect = self.get_text_box_position(speaker)
        self.draw_text_box(message, text_box_rect, WHITE, BOX_COLOR, padding=10)
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.update()
            self.draw()
            self.clock.tick(60)
            
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_game_log>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    game = WerewolfGame(log_file_path)
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
