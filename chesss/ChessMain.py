"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from chesss import ChessEngine
from chesss.ChessEngine import GameState


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}



def load_Images():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wp", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #We can access an image by saying IMAGES['wp']


# The main driver for our code. This will handle user input and updating the graphics.

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    load_Images() #only do this once, before the while loop
    running = True
    sqSelected = () # keep track of the last click of the player, (tuple: (row, col))
    playerClicks = []  # keep track of the player clicks (two tuples: (6,4), (6,3))

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # the user clicked the same square twice (undo)
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: # After second clicks
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # reset player clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # press "z" to undo move
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)  # Draw the squares on the board
    #add in piece highlighting or move suggestions (for later)
    drawPieces(screen, gs.board) # Draw the pieces on the board using the current GameState.board


# Draw the squares on the board
def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



# Draw the pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__":
    main()

