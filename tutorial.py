import pygame as pg
from random import randint

pg.init() # initialize pg modules. Returns a tuple of (succesful, unsuccesful) initializations

white = (255, 255, 255) # RGB value of the color
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 140, 0)

display_width = 800
display_height = 600

program_surface = pg.display.set_mode((display_width,display_height)) # returns a surface object with (w,h) wxh pixels
pg.display.set_caption('Slither')

clock = pg.time.Clock() # pg clock object used to set fps
fps = 15

block_size = 10
font = pg.font.SysFont(None, 25) # size 25

def snake(block_size, snake_list):
    for x_and_y in snake_list:
        pg.draw.rect(program_surface, green, [x_and_y[0],x_and_y[1],block_size,block_size]) # parameters: surface, color, [x,y,width,height]

def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color) # render message, True (for anti-aliasing), color
    program_surface.blit(screen_text, [display_width//2, display_height//2]) # show screen_text on [coords]

def game_loop():
    program_exit = False
    game_over = False

    lead_x = display_width//2
    lead_y = display_height//2
    lead_x_change = 0
    lead_y_change = 0
    snake_list = [] # list of all squares occupied by the snake
    snake_length = 1 # max allowed length of danger noodle

    # randint(0,display_width) could return display_width, meaning we would get an apple with coordinates
    # [display_width, display_height, block_size, block_size], which would appear offscreen
    rand_apple_x = round(randint(0, display_width - block_size)) # / 10) * 10 # round to nearest 10
    rand_apple_y = round(randint(0, display_height - block_size)) # / 10) * 10 # round to nearest 10

    while not program_exit:
        while game_over:
            program_surface.fill(white)
            message_to_screen("Game over. Press C to play again or Q to quit", red)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    program_exit = True
                    game_over = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        program_exit = True
                        game_over = False
                    if event.key == pg.K_c:
                        game_loop()

        for event in pg.event.get(): # gets all events (mouse movenent, key press/release, quit etc)
            if event.type == pg.QUIT:
                program_exit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                if event.key == pg.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                if event.key == pg.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                if event.key == pg.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0: # add boundaries
            game_over = True
        
        lead_x += lead_x_change
        lead_y += lead_y_change

        program_surface.fill(white)
        apple_thickness = 30
        pg.draw.rect(program_surface, red, [rand_apple_x, rand_apple_y, apple_thickness, apple_thickness]) # draw apple
        
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        
        if len(snake_list) >  snake_length:
            del snake_list[0] # remove the first (oldest) element of the list
        
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True


        snake(block_size, snake_list)
        pg.display.update() # update the display

        # Collision for small snake, big apple
        if lead_x >= rand_apple_x and lead_x <= rand_apple_x + apple_thickness:
            if lead_y >= rand_apple_y and lead_y <= rand_apple_y + apple_thickness:
                rand_apple_x = round(randint(0, display_width - block_size)) # / 10) * 10 # round to nearest 10
                rand_apple_y = round(randint(0, display_height - block_size)) # / 10) * 10 # round to nearest 10
                snake_length += 1

        clock.tick(fps) # tick(x) for a game of x frames per second, put this after display.update()

    pg.quit() # uninitialize pygame
    quit() # quit the program

game_loop()