import pygame
import sys
import os
import math
from const import *
from utils import load_game_log, get_eliminated_player, load_final_results
import hashlib
from tts_preprocess import preprocess_audio

class WerewolfGame:
    def __init__(self, log_file_path, players):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Werewolf Game Replay")
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.clock = pygame.time.Clock()
        
        self.players = players
        # Load background images
        self.background_day = pygame.image.load('./img/background_day.png').convert()
        self.background_day = pygame.transform.scale(self.background_day, (WIDTH, HEIGHT))
        self.background_night = pygame.image.load('./img/background_night.png').convert()
        self.background_night = pygame.transform.scale(self.background_night, (WIDTH, HEIGHT))
        
        # Load player images
        self.player_images = {}
        self.player_labels = {}
        self.player_eliminated = {}
        for player, size in zip(
            self.players, 
            [(128, 360), (196, 360), (128, 340), (128, 360), (128, 360)]
        ):
            image = pygame.image.load(f'./img/{player}.png').convert_alpha()
            self.player_images[player] = pygame.transform.scale(image, size)
            self.player_labels[player] = player
            self.player_eliminated[player] = False

        self.eliminated_image = pygame.image.load('./img/eliminated.png').convert_alpha()
        self.eliminated_image = pygame.transform.scale(self.eliminated_image, (ELIM_WIDTH, ELIM_HEIGHT))
        
        self.game_log = load_game_log(log_file_path)
        self.setup_players()
        self.setup_game_state()
        self.is_night = True
        self.is_game_over = False

        self.final_result = load_final_results(log_file_path)
        
    def setup_players(self):
        self.num_players = len(self.players)
        self.circle_center = (WIDTH // 2, HEIGHT // 2 + 150)
        self.circle_radius = 200
    
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
        for name, pos in player_positions.items():
            # Get the player image
            player_image = self.player_images[name]
            # Create a rect for positioning the image centered on the position
            image_rect = player_image.get_rect(center=pos)
            # Draw the image
            self.screen.blit(player_image, image_rect)

            if self.player_eliminated[name]:
                eliminated_rect = self.eliminated_image.get_rect(center=pos)
                self.screen.blit(self.eliminated_image, eliminated_rect)

            # Draw the name below the image
            name_text = self.font.render(self.player_labels[name].capitalize(), True, WHITE)
            text_rect = name_text.get_rect(center=(pos[0], pos[1] - 60))  # Adjust the 40 value as needed
            self.screen.blit(name_text, text_rect)
            
    def get_text_box_position(self, speaker, message):
        # Calculate box position and dimensions
        if speaker.lower() == "narrator":
            box_width = NBOX_WIDTH
            box_x = WIDTH // 2 - box_width // 2
            box_y = 10
            box_height = 50 + (len(message) // 50) * 25
        else:
            box_x, box_y = text_positions[speaker.lower()]
            box_width = TBOX_WIDTH
            box_height = 50 + (len(message) // 30) * 25

        return pygame.Rect(box_x, box_y, box_width, box_height)
    
    def update(self):
        speaker, message = self.game_log[self.current_line_index]

        if "The night falls" in message:
            self.is_night = True
        elif "The sun rises" in message:
            self.is_night = False
        self.current_line_index = self.current_line_index + 1

        if self.current_line_index >= len(self.game_log):
            self.is_game_over = True
            return
            
        eliminated_player = get_eliminated_player(speaker, message)
        if eliminated_player is not None:
            player, role, cause = eliminated_player
            self.player_labels[player] = f"{player} ({cause}, was {role})"
            self.player_eliminated[player] = True

    def draw(self):
        if self.is_night:
            self.screen.blit(self.background_night, (0, 0))
        else:
            self.screen.blit(self.background_day, (0, 0))
        self.draw_players()

        speaker, message = self.game_log[self.current_line_index]

        text_box_rect = self.get_text_box_position(speaker, message)
        self.draw_text_box(message, text_box_rect, WHITE, BOX_COLOR, padding=10)

        pygame.display.flip()

    def play_sound(self):
        speaker, message = self.game_log[self.current_line_index]
        text_hash = hashlib.md5(message.encode()).hexdigest()
        audio_file = f"{BASE_TTS}/{speaker}/{text_hash}.mp3"
        if os.path.exists(audio_file):
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def draw_final_screen(self):
        self.screen.fill(BG_COLOR)
        winner, townsfolks, werewolves, roles = self.final_result
        
        # Draw winner text
        big_font = pygame.font.SysFont("Arial", FONT_SIZE * 3)
        winner_text = big_font.render(f"{winner.capitalize()} wins!", True, WHITE)
        winner_rect = winner_text.get_rect(center=(WIDTH//2, 50))
        self.screen.blit(winner_text, winner_rect)
        
        # Display werewolf images in a row
        x_offset = WIDTH//2
        y_offset = 250
        image_spacing = 150
        for player in werewolves:
            # Scale down the player image for the final screen
            original_image = self.player_images[player]
            scaled_image = pygame.transform.scale(original_image, (original_image.get_width()//2, original_image.get_height()//2))
            image_rect = scaled_image.get_rect(center=(x_offset, y_offset))
            self.screen.blit(scaled_image, image_rect)

            if self.player_eliminated[player]:
                eliminated_rect = self.eliminated_image.get_rect(center=(x_offset, y_offset))
                self.screen.blit(self.eliminated_image, eliminated_rect)
            
            # Add player name below image
            name_text = self.font.render(roles[player].capitalize(), True, WHITE)
            name_rect = name_text.get_rect(center=(x_offset, y_offset + 70))
            self.screen.blit(name_text, name_rect)
        
            
            x_offset += image_spacing
        
        # Display townsfolk images in a row
        x_offset = WIDTH//4
        y_offset += 300
        for player in townsfolks:
            # Scale down the player image for the final screen
            original_image = self.player_images[player]
            scaled_image = pygame.transform.scale(original_image, (original_image.get_width()//2, original_image.get_height()//2))
            image_rect = scaled_image.get_rect(center=(x_offset, y_offset))
            self.screen.blit(scaled_image, image_rect)

            if self.player_eliminated[player]:
                eliminated_rect = self.eliminated_image.get_rect(center=(x_offset, y_offset))
                self.screen.blit(self.eliminated_image, eliminated_rect)
            
            # Add player name below image
            name_text = self.font.render(roles[player].capitalize(), True, WHITE)
            name_rect = name_text.get_rect(center=(x_offset, y_offset + 70))
            self.screen.blit(name_text, name_rect)
            
            x_offset += image_spacing


        pygame.display.flip()

    def run(self):
        starting = True
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            if self.is_game_over:
                self.draw_final_screen()
            else:
                self.draw()
                if starting:
                    # I just need this to give myself sometime if I need to record
                    # pygame.time.wait(15000)
                    starting = False
                self.play_sound()
                self.update()
                
            self.clock.tick(60)
            
def main():
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_game_log>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    preprocess_audio(log_file_path)
    game = WerewolfGame(
        log_file_path,
        ["deepseek", "grok", "sonnet", "gemini", "gpt4"]
    )
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
