import pygame
import sudoku
from assets import *
import os, sys
from time import time

## sudoku board
'''board = [
    [4, 0, 6, 3, 8, 0, 0, 2, 0],
    [5, 0, 3, 7, 0, 4, 0, 0, 0],
    [0, 0, 0, 9, 0, 0, 8, 4, 3],
    [2, 3, 0, 0, 1, 0, 9, 0, 0],
    [0, 4, 0, 0, 0, 0, 5, 7, 1],
    [0, 5, 0, 6, 4, 7, 0, 0, 0],
    [9, 0, 1, 4, 0, 8, 3, 0, 0],
    [0, 6, 4, 0, 0, 0, 0, 0, 7],
    [8, 0, 5, 1, 0, 3, 0, 9, 2]
]'''

board = sudoku.generate_board()

pygame.init()

WIDTH, HEIGHT = 595, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

dark_mode_rect = pygame.Rect(130, 658, 36, 18)
theme_color = 30
dark_mode = True
dark_mode_switch = Switch(WIN, dark_mode_rect, 16, (255, 255, 255))
theme_transition_start = False
finish_rect = pygame.Rect(228, 650, 138, 33)

font_location = os.path.join(os.path.abspath("."), "Roboto-Bold.ttf")

font = pygame.font.Font(font_location, 30)
font2 = pygame.font.Font(font_location, 20)
font3 = pygame.font.Font(font_location, 19)

clock = pygame.time.Clock()
start = time()
minutes = 0
time_passed = "00:00"

start_solve = False
collision = False
done = False
finish = False
solve_loop = 5

grid = pygame.Rect(10, 60, 55, 55)
solve = sudoku.Solve(board, False)
solved_board = sudoku.Solve(board, True)

while sudoku.find_empty(solved_board.board):
    next(solved_board)

## stores temporary number entered by user
user_input = {}

boxes = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
]

lines = []

def location():
    ## stores location of every box in list boxes
    for i in range(len(board)):
        if i % 3 == 0:
            grid.y += 10
            lines.append(((11, grid.y - 9), (581, grid.y - 9)))

        for j in range(len(board[0])):
            if j % 3 == 0:
                grid.x += 10
            if i % 3 == 0 and j % 3 == 0 and i == j:
                lines.append(((grid.x - 8, 60), (grid.x - 8, 632)))
            boxes[i].append(pygame.Rect(grid.x, grid.y, 55, 55))
            grid.x += 60

        grid.x = 10
        grid.y += 60

    lines.append(((11, 632), (581, 632)))
    lines.append(((581, 60), (581, 632)))


location()
BouncyAnimation.initialize(boxes)

def draw_grid():
    ## render boxes and lines
    box_color = pygame.Color(88, 88, 88)
    line_color = pygame.Color(50, 150, 255)

    for i in range(len(board)):
        for j in range(len(board[0])):
            if collision == (i, j):
                draw_rounded_rect(WIN, box_collision_color, boxes[i][j], 4)
                continue
            pygame.draw.rect(WIN, box_color, boxes[i][j], 1)

    for i in range(len(lines)):
        pygame.draw.line(WIN, line_color, lines[i][0], lines[i][1], 3)


def render_numbers():
    ## render numbers inside boxes
    global dark_mode
    x = 38
    y = 80

    if dark_mode:
        text_color = (225, 225, 225)
    else:
        text_color = (40, 40, 40)

    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            y += 10
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                x += 10
            if board[i][j] == 0:
                num = ""
            else:
                num = str(board[i][j])
            number = font.render(num, 1, text_color)
            WIN.blit(number, (x, y))
            x += 60
        x = 38
        y += 60

    for item in user_input:
        ## renders the temporary numbers entered by user
        if board[item[0]][item[1]] != 0:
            continue
        position, num = user_input[item]
        number = font.render(str(num), 1, (80, 80, 80))
        WIN.blit(number, (position.center[0] - number.get_width()//2, position.center[1] - number.get_height()//2))


def calculate_time():
    ## shows the time
    global start, minutes
    seconds = int(time() - start)
    if seconds > 59:
        seconds = 0
        start = time()
        minutes = int(minutes)
        minutes += 1
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)
    if len(str(seconds)) == 1:
        seconds = "0" + str(seconds)
    return f"Time:  {minutes}:{seconds}"


def redraw():
    ## render whole application
    global time_passed, dark_mode, theme_transition_start, theme_color

    if dark_mode:
        text_color = (255, 255, 255)

    else:
        text_color = (0, 0, 0)

    if theme_transition_start:
        theme_color += next(theme_transition)
        if theme_transition.i == 21:
            theme_transition_start = False
    
    WIN.fill((theme_color, theme_color, theme_color))

    if not finish:
        time_passed = calculate_time()

    if start_solve:
        solving_font= font2.render("sToP being LaZy!", 1, text_color)
        WIN.blit(solving_font, ((WIDTH - solving_font.get_width())//2, 655))
    elif finish:
        finish_font= font2.render("Finished!", 1, text_color)
        draw_rounded_rect(WIN, pygame.Color('dodgerblue'), finish_rect, 4)
        WIN.blit(finish_font, ((WIDTH - finish_font.get_width())//2, 655))

    sudoko_font = font.render("Sudoku", 1, text_color)
    timer = font2.render(time_passed, 1, text_color)
    dark_mode_font = font3.render("Dark Mode", 1, (text_color))

    WIN.blit(sudoko_font, ((WIDTH - sudoko_font.get_width())//2, 15))
    WIN.blit(dark_mode_font, (20, 656))
    WIN.blit(timer, (WIDTH - timer.get_width() - 25, 655))
    
    dark_mode_switch.rect.x = dark_mode_font.get_width() + 36
    
    dark_mode_switch.background_color = (theme_color, theme_color, theme_color)
    dark_mode_switch.toggle(dark_mode)

    draw_grid()
    render_numbers()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            ## starts solving automatically on hitting tab
            if event.key == pygame.K_TAB:
                start_solve = not start_solve
            
            ## change the theme on hitting space
            if event.key == pygame.K_SPACE:
                dark_mode = not dark_mode
                theme_transition_start = True
                if dark_mode:
                    theme_transition = LinearAnimation(25 - theme_color)
                else:
                    theme_transition = LinearAnimation(255 - theme_color)

            if event.key == pygame.K_RETURN:
                if collision:
                    BouncyAnimation(8, collision)
                ## makes number permanent if it is correct on hitting enter
                if collision in user_input:
                    number = user_input[collision][1]
                    if solved_board.board[collision[0]][collision[1]] == number:
                        board[collision[0]][collision[1]] = number
                        box_collision_color = pygame.Color(50, 160, 255)
                        del user_input[collision]
                    else:
                        box_collision_color = pygame.Color(220, 50, 50)

            if event.key == pygame.K_BACKSPACE:
                ## erase the temporary number on hitting backspace
                if collision in user_input:
                    del user_input[collision]

            if not start_solve and collision:
                ## enters the temporary number in selected box
                if event.unicode in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    number = int(event.unicode)
                    if board[collision[0]][collision[1]] == 0:
                        user_input[collision] = (boxes[collision[0]][collision[1]], number)

                ## moves the box on hitting arrow keys
                if event.key == pygame.K_UP:
                    if collision[0] != 0:
                        collision = (collision[0] - 1, collision[1])
                    box_collision_color = pygame.Color(50, 150, 255)
                    BouncyAnimation(8, collision)

                if event.key == pygame.K_DOWN:
                    if collision[0] < len(board) - 1:
                        collision = (collision[0] + 1, collision[1])
                    box_collision_color = pygame.Color(50, 150, 255)
                    BouncyAnimation(8, collision)

                if event.key == pygame.K_RIGHT:
                    if collision[1] < len(board[0]) - 1:
                        collision = (collision[0], collision[1] + 1)
                    box_collision_color = pygame.Color(50, 150, 255)
                    BouncyAnimation(8, collision)

                if event.key == pygame.K_LEFT:
                    if collision[1] != 0:
                        collision = (collision[0], collision[1] - 1)
                    box_collision_color = pygame.Color(50, 150, 255)
                    BouncyAnimation(8, collision)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if dark_mode_rect.collidepoint(pos):
                ## turns dark mode on or off on hitting switch
                dark_mode = not dark_mode
                theme_transition_start = True
                if dark_mode:
                    theme_transition = LinearAnimation(30 - theme_color)
                else:
                    theme_transition = LinearAnimation(255 - theme_color)
            
            if finish and finish_rect.collidepoint(pos):
                ## generates new sudoku board
                board = sudoku.generate_board()
                finish = False
                solve = sudoku.Solve(board, False)
                solved_board = sudoku.Solve(board, True)
                start = time()

                while sudoku.find_empty(solved_board.board):
                    next(solved_board)

                ## stores temporary number entered by user
                user_input = {}
            
            if not start_solve:
                for i in range(len(board)):
                    for j in range(len(board[0])):
                        if boxes[i][j].collidepoint(pos):
                            ## activates the selected box to take input
                            collision = (i, j)
                            box_collision_color = pygame.Color(50, 150, 255)
                            BouncyAnimation(8, collision)
                            done = True
                            break
                        else:
                            collision = False
                    if done:
                        done = False
                        break

    BouncyAnimation.animation()

    if start_solve:
        if solve_loop == 5:
            collision = next(solve)
            BouncyAnimation(8, collision)
            box_collision_color = pygame.Color(50, 150, 255)
            solve_loop = 0
        solve_loop += 1

    if not sudoku.find_empty(board):
        ## checks if board is finished or not
        ## if it is finished then timer stops
        start_solve = False
        finish = True
        user_input.clear()

    redraw()
    pygame.display.update()
    clock.tick(60)
