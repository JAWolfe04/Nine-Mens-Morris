import pygame, sys
from pygame.locals import *

# Colors
#-------------------------------------------------
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize pygame
#-------------------------------------------------
pygame.init()

# Font
#-------------------------------------------------
small_font = pygame.font.SysFont("Verdana", 20)

class Game:
    def __init__(self, screen):
        # Screen Attibutes
        #-------------------------------------------------
        self.screen = screen

        # Game Attibutes
        #-------------------------------------------------
        self.use_ai = True
        self.player_turn = 1
        self.placing_phase = True
        self.removing_phase = False
        self.pieces_count = [[9, 0], [9, 0]]
        self.selected_piece = -1

        # Board Attributes
        #-------------------------------------------------
        # Radius of the game pieces
        self.piece_size = 15
        # Center of the board in the screen. Adjust multiplier to
        # reposition in screen
        self.board_center = (int(self.screen.get_width() * 0.3),
                             int(self.screen.get_height() * 0.5))

        ## Sizes of squares of the board
        # Size of the inner square of the game board
        self.inner_square_size = 125
        # Size of the outer square of the game board
        self.outer_square_size = 425
        # Size of the middle square centered between the inner and outer squares
        self.mid_square_size = int((self.outer_square_size -
                        self.inner_square_size) / 2) + self.inner_square_size

        ## Points of the squares of the board
        # Start points
        #Start point(x,y) of the outer square
        self.outer_start_pos = (self.board_center[0] - int(self.outer_square_size / 2),
                           self.board_center[1] - int(self.outer_square_size / 2))
        #Start point(x,y) of the middle square
        self.mid_start_pos = (self.board_center[0] - int(self.mid_square_size / 2),
                         self.board_center[1] - int(self.mid_square_size / 2))
        #Start point(x,y) of the inner square
        self.inner_start_pos = (self.board_center[0] - int(self.inner_square_size / 2),
                           self.board_center[1] - int(self.inner_square_size / 2))

        # End points
        #End point(x,y) of the outer square
        self.outer_end_pos = (self.board_center[0] + int(self.outer_square_size / 2),
                         self.board_center[1] + int(self.outer_square_size / 2))
        #End point(x,y) of the middle square
        self.mid_end_pos = (self.board_center[0] + int(self.mid_square_size / 2),
                       self.board_center[1] + int(self.mid_square_size / 2))
        #End point(x,y) of the inner square
        self.inner_end_pos = (self.board_center[0] + int(self.inner_square_size / 2),
                         self.board_center[1] + int(self.inner_square_size / 2))

        # Game Grid
        #-------------------------------------------------
            #0----------1-----------2
            #|          |           |
            #|   3------4-------5   |
            #|   |      |       |   |
            #|   |   6--7---8   |   |
            #|   |   |      |   |   |
            #9---10--11    12--13--14
            #|   |   |      |   |   |
            #|   |   15-16-17   |   |
            #|   |      |       |   |
            #|   18-----19------20  |
            #|          |           |
            #21---------22----------23

        # Array of int indicating piece type: 0 for none, 1 or 2 for player
        self.slot_pieces = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Tuple x and y of the slot on the screen
        self.slot_coord = [(self.outer_start_pos[0], self.outer_start_pos[1]),
                      (self.board_center[0], self.outer_start_pos[1]),
                      (self.outer_end_pos[0], self.outer_start_pos[1]),
                      (self.mid_start_pos[0], self.mid_start_pos[1]),
                      (self.board_center[0], self.mid_start_pos[1]),
                      (self.mid_end_pos[0], self.mid_start_pos[1]),
                      (self.inner_start_pos[0], self.inner_start_pos[1]),
                      (self.board_center[0], self.inner_start_pos[1]),
                      (self.inner_end_pos[0], self.inner_start_pos[1]),
                      (self.outer_start_pos[0], self.board_center[1]),
                      (self.mid_start_pos[0], self.board_center[1]),
                      (self.inner_start_pos[0], self.board_center[1]),
                      (self.inner_end_pos[0], self.board_center[1]),
                      (self.mid_end_pos[0], self.board_center[1]),
                      (self.outer_end_pos[0], self.board_center[1]),
                      (self.inner_start_pos[0], self.inner_end_pos[1]),
                      (self.board_center[0], self.inner_end_pos[1]),
                      (self.inner_end_pos[0], self.inner_end_pos[1]),
                      (self.mid_start_pos[0], self.mid_end_pos[1]),
                      (self.board_center[0], self.mid_end_pos[1]),
                      (self.mid_end_pos[0], self.mid_end_pos[1]),
                      (self.outer_start_pos[0], self.outer_end_pos[1]),
                      (self.board_center[0], self.outer_end_pos[1]),
                      (self.outer_end_pos[0], self.outer_end_pos[1])]

        # Indices of adjacent slots
        self.slot_adj =[[1, 9],              #0
                        [0, 2, 4],           #1
                        [1, 14],             #2
                        [4, 10],             #3
                        [1, 3, 5, 7],        #4
                        [4, 13],             #5
                        [7, 11],             #6
                        [4, 6, 8],           #7
                        [7, 12],             #8
                        [0, 10, 21],         #9
                        [3, 9, 11, 18],      #10
                        [6, 10, 15],         #11
                        [8, 13, 17],         #12
                        [5, 12, 14, 20],     #13
                        [2, 13, 23],         #14
                        [11, 16],            #15
                        [15, 17, 19],        #16
                        [12, 16],            #17
                        [10, 19],            #18
                        [16, 18, 20, 22],    #19
                        [13, 19],            #20
                        [9, 22],             #21
                        [19, 21, 23],        #22
                        [14, 22]]            #23

        # Array of arrays of indices of slots involving mills for each slot
        self.slot_mills = [[[0, 1, 2],[0, 9, 21]],      #0
                           [[0, 1, 2],[1, 4, 7]],       #1
                           [[0, 1, 2],[2, 14, 23]],     #2
                           [[3, 4, 5],[3, 10, 18]],     #3
                           [[3, 4, 5],[1, 4, 7]],       #4
                           [[3, 4, 5],[5, 13, 20]],     #5
                           [[6, 7, 8],[6, 11, 15]],     #6
                           [[6, 7, 8],[1, 4, 7]],       #7
                           [[6, 7, 8],[8, 12, 17]],     #8
                           [[9, 10, 11],[0, 9, 21]],    #9
                           [[9, 10, 11],[3, 10, 18]],   #10
                           [[9, 10, 11],[6, 11, 15]],   #11
                           [[12, 13, 14],[8, 12, 17]],  #12
                           [[12, 13, 14],[5, 13, 20]],  #13
                           [[12, 13, 14],[2, 14, 23]],  #14
                           [[15, 16, 17],[6, 11, 15]],  #15
                           [[15, 16, 17],[16, 19, 22]], #16
                           [[15, 16, 17],[8, 12, 17]],  #17
                           [[18, 19, 20],[3, 10, 18]],  #18
                           [[18, 19, 20],[16, 19, 22]], #19
                           [[18, 19, 20],[5, 13, 20]],  #20
                           [[21, 22, 23],[0, 9, 21]],   #21
                           [[21, 22, 23],[16, 19, 22]], #22
                           [[21, 22, 23],[2, 14, 23]]]  #23

    # Draw Game
    #-------------------------------------------------
    # Draws a filled color circle with a color border
    # outline_color: Color of the border around the circle
    # fill_color: Color of the circle
    # center: x and y tuple of the screen position of the circle
    # radius: radius of circle including the border
    # border: width of the border
    def filled_circle(self, outline_color, fill_color, center, radius, border):
        pygame.draw.circle(self.screen, outline_color,
                           (center[0] + 1, center[1] + 1), radius, 0)
        pygame.draw.circle(self.screen, fill_color,
                           (center[0] + 1, center[1] + 1), radius - border, 0)

    # Draws the current game board state with pieces
    def draw_board(self):
        # Clear screen
        self.screen.fill(WHITE)

        # Draw text indicating whose turn it is and info about pieces
        turn_txt = ""
        blue_pieces_txt = ""
        red_pieces_txt = ""
        if(self.removing_phase):
            if(self.use_ai):
                if(self.player_turn == 1):
                    turn_txt = "Player Removing"
                else:
                    turn_txt = "Computer Removing"
            else:
                if(self.player_turn == 1):
                    turn_txt = "Blue Removing"
                else:
                    turn_txt = "Red Removing"
            if(self.placing_phase):
                blue_pieces_txt = "Placing {} Blue Pieces" \
                    .format(self.pieces_count[0][0])
                red_pieces_txt = "Placing {} Red Pieces" \
                    .format(self.pieces_count[1][0])
            else:
                blue_pieces_txt = "{} Blue Pieces Remaining" \
                .format(self.pieces_count[0][1])
                red_pieces_txt = "{} Red Pieces Remaining" \
                    .format(self.pieces_count[1][1])
                
        elif(self.placing_phase):
            if(self.use_ai):
                if(self.player_turn == 1):
                    turn_txt = "Player Placing"
                else:
                    turn_txt = "Computer Placing"
            else:
                if(self.player_turn == 1):
                    turn_txt = "Blue Placing"
                else:
                    turn_txt = "Red Placing"
                    
            blue_pieces_txt = "Placing {} Blue Pieces" \
                .format(self.pieces_count[0][0])
            red_pieces_txt = "Placing {} Red Pieces" \
                .format(self.pieces_count[1][0])
        else:
            if(self.use_ai):
                if(self.player_turn == 1):
                    turn_txt = "Player Moving"
                else:
                    turn_txt = "Computer Moving"
            else:
                if(self.player_turn == 1):
                    turn_txt = "Blue Moving"
                else:
                    turn_txt = "Red Moving"
                    
            blue_pieces_txt = "{} Blue Pieces Remaining" \
                .format(self.pieces_count[0][1])
            red_pieces_txt = "{} Red Pieces Remaining" \
                .format(self.pieces_count[1][1])
            

        turn_pos = (int(self.screen.get_width() * 0.6),
                    int(self.screen.get_height() * 0.1))
        self.screen.blit(small_font.render(turn_txt, True, BLACK), turn_pos)

        blue_render = small_font.render(blue_pieces_txt, True, BLACK)
        blue_pos = (int(self.screen.get_width() * 0.6),
                    int(self.screen.get_height() * 0.3))
        self.screen.blit(blue_render, blue_pos)

        red_render = small_font.render(red_pieces_txt, True, BLACK)
        red_pos = (int(self.screen.get_width() * 0.6),
                    int(self.screen.get_height() * 0.35))
        self.screen.blit(red_render, red_pos)
        
        # Draw inner square
        pygame.draw.rect(self.screen, BLACK, (self.slot_coord[6][0],
                        self.slot_coord[6][1], self.inner_square_size,
                        self.inner_square_size), 2)
        # Draw middle square
        pygame.draw.rect(self.screen, BLACK, (self.slot_coord[3][0],
                        self.slot_coord[3][1], self.mid_square_size,
                        self.mid_square_size), 2)
        # Draw outer square
        pygame.draw.rect(self.screen, BLACK, (self.slot_coord[0][0],
                        self.slot_coord[0][1], self.outer_square_size,
                        self.outer_square_size), 2)

        # Draw lines connecting squares
        pygame.draw.line(self.screen, BLACK, self.slot_coord[1],
                         self.slot_coord[7], 2)
        pygame.draw.line(self.screen, BLACK, self.slot_coord[9],
                         self.slot_coord[11], 2)
        pygame.draw.line(self.screen, BLACK, self.slot_coord[12],
                         self.slot_coord[14], 2)
        pygame.draw.line(self.screen, BLACK, self.slot_coord[16],
                         self.slot_coord[22], 2)

        # Draw pieces and slots
        for i in range(0, 24):
            color = WHITE

            # Change color for a player piece
            if self.slot_pieces[i] == 1:
                color = BLUE
            elif self.slot_pieces[i] == 2:
                color = RED

            self.filled_circle(BLACK, color, self.slot_coord[i],
                               self.piece_size, 2)

        pygame.display.update()

    
    # Returns the index of a clicked slot
    # x: the x coordinate of the mouse click
    # y: y coordinate of the mouse click
    # Returns -1 if the mouse click was not in a slot
    def get_slot(self, x, y):
        radius = self.piece_size + 1
        for i in range(0, 24):
          if((self.slot_coord[i][0] - radius) <= x <= (self.slot_coord[i][0] + radius) and 
             (self.slot_coord[i][1] - radius) <= y <= (self.slot_coord[i][1] + radius)):
            return i
        return -1

    # Returns if the indicated slot is a mill
    # position: index of the slot to check
    # Returns true if it is a mill otherwise false
    def is_mill(self, position):
        # Check 1st possible mill of the slot
        if(self.slot_pieces[self.slot_mills[position][0][0]] == 
           self.slot_pieces[self.slot_mills[position][0][1]] == 
           self.slot_pieces[self.slot_mills[position][0][2]] 
           or
           # Check 2nd mill
           self.slot_pieces[self.slot_mills[position][1][0]] == 
           self.slot_pieces[self.slot_mills[position][1][1]] == 
           self.slot_pieces[self.slot_mills[position][1][2]]):
            return True
        return False

    # Check each piece for any pieces of the opponent that
    # is not part of a mill
    # Enables the rule of non-mill pieces must be removed first
    # player: interger(1,2) of player to check
    # Returns true if there are non-mill pieces for the player
    def has_non_mill_pieces(self, player):
        for i in range(0, len(self.slot_pieces)):
            if(self.slot_pieces[i] == player and not self.is_mill(i)):
                return True
        return False

    # Checks if player has any remaining moves
    # player: 1 or 2 indicating the player to check
    # Returns true if player can move otherwise false
    def has_remaining_moves(self, player):
        # If a player still has more pieces to place then they can move
        if(self.pieces_count[player - 1][0] > 0):
            return True
        
        # If the player has only 3 pieces, then they can fly
        if(self.pieces_count[player - 1][1] + \
           self.pieces_count[player - 1][0]  == 3):
            return True

        # Cycle through each slot looking for the player's pieces, if
        # one is found check the adjacent slots are open
        for i in range(0, len(self.slot_pieces)):
            if(self.slot_pieces[i] == player):
                for a in self.slot_adj[i]:
                    if(self.slot_pieces[a] == 0):
                        return True
        return False

    # Checks if a player has won
    # player(Optional): 1 or 2 for player to check
    # Returns 0 if a player has not won, otherwise 1 or 2 for a player
    def has_won(self, player = 0):
        if(player != 0):
            # Check if a specific player has won
            opponent = 2 if player == 1 else 1
            if((self.pieces_count[opponent - 1][1] +
                self.pieces_count[opponent - 1][0]) <= 2 or
               not self.has_remaining_moves(opponent)):
                return player
            return 0
        else:
            # Check if any player has won and return that player
            for p in range(1, 3):
                if(self.has_won(p) != 0):
                    return p
            return 0
            

    # Checks if the selected piece can be removed
    # position: index of the piece to remove
    # player: interger(1,2) of player whose piece is being removed
    # Returns true if the piece can be removed otherwise false
    def can_remove_piece(self, position, player):
        # Cannot be your own piece and non-mill pieces must be removed first
        return (self.slot_pieces[position] == player and
           not (self.has_non_mill_pieces(player) and self.is_mill(position)))

    # Checks if move from position to new_position is valid
    # position: index of the current location of the piece
    # new_position: index of the proposed move
    # Returns true is move is valid, otherwise false
    def is_valid_move(self, position, new_position):
        # Allow flying if the current player has 3 pieces
        if((self.player_turn and
            self.pieces_count[self.player_turn - 1][1] == 3)):
            return True
        # Make sure the slot is empty
        if(self.slot_pieces[position] == 0):
            return False
    
        return new_position in self.slot_adj[position]

    # Place a piece at the position by the player
    # position: Slot index of the piece to place
    # player: integer(1, 2) of the place placing the piece
    # Returns if the piece was successfully placed
    def place_piece(self, position, player):
        if(self.slot_pieces[position] == 0):
            self.slot_pieces[position] = player
            return True
        return False

    # Remove an indicated piece
    # position: index of the piece to remove
    def remove_piece(self, position):
        self.slot_pieces[position] = 0

    # Selects a players piece by providing a yellow border
    # position: index of piece to select
    # Returns True if piece was selected, false otherwise
    def select_piece(self, position):
        if(self.slot_pieces[position] == 0 or
           self.slot_pieces[position] != self.player_turn or
           self.selected_piece == position):
            return False
    
        color = BLUE

        if(self.player_turn == 2):
            color = RED

        # Draw highlight
        self.filled_circle(YELLOW, color, self.slot_coord[position],
                           self.piece_size - 1, 2)
        pygame.display.update()
        return True

    # Unselects a players piece by removing a yellow border
    # position: piece to remove the selected drawing
    def unselect_piece(self, position):
        # Determine the color of the piece
        color = BLUE
    
        if(self.slot_pieces[position] == 2):
            color = RED

        # Draw piece without highlight
        self.filled_circle(BLACK, color, self.slot_coord[position],
                           self.piece_size, 2)
        pygame.display.update()

    # Resets game
    def reset(self):
        self.slot_pieces = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.player_turn = 1
        self.placing_phase = True
        self.removing_phase = False
        self.pieces_count = [[9, 0], [9, 0]]
        self.selected_piece = -1

    # Handles logic for placing a player piece
    # slot_idx: index for the slot to place the piece
    # Returns 0 if no one has won otherwise 1 or 2 for a player
    def handle_player_placing(self, slot_idx):
        # Attempt to place a piece checking if it valid
        if(self.place_piece(slot_idx, self.player_turn)):
            # Decrement remaining pieces to place and
            # increment placed pieces counts for the player
            self.pieces_count[self.player_turn - 1][0] -= 1
            self.pieces_count[self.player_turn - 1][1] += 1

            # End placing phase when both player have placed all
            # of their pieces
            if(self.pieces_count[1][0] == 0):
                self.placing_phase = False

            # Check if mill is created from placing the piece
            # if so allow player to remove opponent piece
            if(self.is_mill(slot_idx)):
                self.removing_phase = True
                self.draw_board()
                return 0

            # Check if a player has won
            win_result = self.has_won()
            if(win_result != 0):
                return win_result

            # Switch turns
            self.player_turn = 2 if self.player_turn == 1 else 1

            self.draw_board()

            # Pass turn to AI
            if(self.use_ai and self.player_turn == 2):
                self.handle_ai_placing()

            return 0

    # Handles logic for removing a piece
    # slot_idx: index for the piece to remove
    # Returns 0 if no one has won otherwise 1 or 2 for a player
    def handle_player_removing(self, slot_idx):
        # Attempt to remove the piece
        opponent = 2 if self.player_turn == 1 else 1
        if(self.can_remove_piece(slot_idx, opponent)):
            # Remove piece and decrease piece count
            self.remove_piece(slot_idx)
            self.pieces_count[opponent - 1][1] -= 1

            # Check for a winner
            if(self.has_won(self.player_turn)):
                return self.player_turn

            # Indicate removing is done
            self.removing_phase = False
            
            # Switch turns
            self.player_turn = 2 if self.player_turn == 1 else 1
            
            self.draw_board()

            # Pass turn to AI
            if(self.use_ai and self.player_turn == 2):
                # Pass AI to the correct phase
                if(self.placing_phase):
                    self.handle_ai_placing()
                else:
                    return self.handle_ai_movement()
                
        return 0

    def handle_player_movement(self, slot_idx):
        # Handle moves with a piece selected
        if(self.selected_piece > -1):
            # Check if move is valid and attempt to place
            if(self.is_valid_move(self.selected_piece, slot_idx) and
               self.place_piece(slot_idx, self.player_turn)):
                # Remove the old position and reset selection
                self.remove_piece(self.selected_piece)
                self.selected_piece = -1

                # Check if the movement wins the game
                if(self.has_won(self.player_turn)):
                    return self.player_turn

                # Check if mill is created from moving the piece
                # if so allow player to remove opponent piece
                if(self.is_mill(slot_idx)):
                    self.removing_phase = True
                    self.draw_board()
                    return 0

                #Switch player turns
                self.player_turn = 2 if self.player_turn == 1 else 1

                self.draw_board()

            # Select a different piece
            elif(self.select_piece(slot_idx)):
                self.unselect_piece(self.selected_piece)
                self.selected_piece = slot_idx
        # First Selection
        elif(self.select_piece(slot_idx)):
            self.selected_piece = slot_idx
            
        return 0

    def handle_ai_placing(self):
        pass

    def handle_ai_removing(self):
        pass

    def handle_ai_movement(self):
        pass

    # Handles mouse clicks for the game
    # Returns 0 if game is not over, 1 if player 1 wins and 2 if player 2 wins
    def handle_mouse_click(self, x, y):
        slot_idx = self.get_slot(x, y)
        # Handle player vs computer
        # Removing occurs during placing and moving phases
        # so process it before them to allow this behavior
        if(slot_idx != -1):
            if(self.removing_phase):
                return self.handle_player_removing(slot_idx)
            elif(self.placing_phase):
                return self.handle_player_placing(slot_idx)
            else:
                return self.handle_player_movement(slot_idx)
                     
        return 0
