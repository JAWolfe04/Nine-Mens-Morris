import pygame, sys
from pygame.locals import *
from Game import *

# Setup Screen
#-------------------------------------------------
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nine Men's Morris")

# Setup Fonts
#-------------------------------------------------
large_font = pygame.font.SysFont("Verdana", 60)
med_font = pygame.font.SysFont("Verdana", 40)

# Button Coordinates, Size and text
#-------------------------------------------------
pvp_txt = med_font.render("Player vs Player", True, BLACK)
pve_txt = med_font.render("Player vs Computer", True, BLACK)
exit_txt = med_font.render("Quit", True, BLACK)

pvp_txt_hgl = med_font.render("Player vs Player", True, YELLOW)
pve_txt_hgl = med_font.render("Player vs Computer", True, YELLOW)
exit_txt_hgl = med_font.render("Quit", True, YELLOW)

pvp_size = med_font.size("Player vs Player")
pvp_rect = Rect((int(WIDTH * 0.5) - int(pvp_size[0] / 2),
            int(HEIGHT * 0.4) - int(pvp_size[1] / 2)), pvp_size)

pve_size = med_font.size("Player vs Computer")
pve_rect = Rect((int(WIDTH * 0.5) - int(pve_size[0] / 2),
            int(HEIGHT * 0.6) - int(pve_size[1] / 2)), pve_size)

exit_size = med_font.size("Quit")
exit_rect = Rect((int(WIDTH * 0.5) - int(exit_size[0] / 2),
            int(HEIGHT * 0.8) - int(exit_size[1] / 2)), exit_size)

# Setup FPS
#-------------------------------------------------
FPS = 10
FramePerSec = pygame.time.Clock()

# Menu State
#-------------------------------------------------
# Indicator for if the game is running
in_menu = True
# Indicates a winner, 0 for none, and 1 or 2 for a player
winner = 0

# Setup Game
#-------------------------------------------------
game = Game(screen)

# Draw Start Menu
#-------------------------------------------------
def draw_menu():
    screen.fill(WHITE)

    # Draw Heading for the menu
    heading_text = ""
    if(winner == 0):
        heading_text = "Nine Men's Game"
    else:
        heading_text = "Player {} Wins".format(winner)

    heading = large_font.render(heading_text, True, BLACK)
    heading_size = large_font.size(heading_text)
    heading_pos = (int(WIDTH * 0.5) - int(heading_size[0] / 2),
                       int(HEIGHT * 0.2) - int(heading_size[1] / 2))
    screen.blit(heading, heading_pos)

    # Draw highlight if mouse is over an option
    mouse_pos = pygame.mouse.get_pos()
    if(pvp_rect.collidepoint(mouse_pos)):
        screen.blit(pvp_txt_hgl, (pvp_rect.x, pvp_rect.y))
    else:
        screen.blit(pvp_txt, (pvp_rect.x, pvp_rect.y))
        
    if(pve_rect.collidepoint(mouse_pos)):
        screen.blit(pve_txt_hgl, (pve_rect.x, pve_rect.y))
    else:
        screen.blit(pve_txt, (pve_rect.x, pve_rect.y))
        
    if(exit_rect.collidepoint(mouse_pos)):
        screen.blit(exit_txt_hgl, (exit_rect.x, exit_rect.y))
    else:
        screen.blit(exit_txt, (exit_rect.x, exit_rect.y))

    pygame.display.update()
    
#Game Loop
#-------------------------------------------------
draw_menu()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle Menu Logic
            if(in_menu):
                pos = (event.pos[0], event.pos[1])
                if(pvp_rect.collidepoint(pos)):
                    in_menu = False
                    game.use_ai = False
                    game.draw_board()
                elif(pve_rect.collidepoint(pos)):
                    in_menu = False
                    game.use_ai = True
                    game.draw_board()
                elif(exit_rect.collidepoint(pos)):
                    pygame.quit()
                    sys.exit()
            # Handle Game Logic
            elif(not in_menu):
                result = game.handle_mouse_click(event.pos[0], event.pos[1])

                if(result != 0):
                    in_menu = True
                    winner = result
                    game.reset()
                            
    # Enables Menu Option Highlighting   
    if(in_menu):
        draw_menu()

    # Slows cycle to the indicated FPS
    FramePerSec.tick(FPS)
