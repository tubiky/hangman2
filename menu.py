import time
import pygame
from pygame.constants import KEYDOWN
import pygame.freetype
pygame.freetype.init()

pygame.init()

WIDTH = 800
HEIGHT = 600

menu = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

menu_font = pygame.font.Font(None, 100)

active_color = pygame.Color('red')
inactive_color = pygame.Color(0, 100, 100)
color = active_color

txt_start = menu_font.render("Start", True, color)
start_rect = txt_start.get_rect()
start_rect[0], start_rect[1] = 400, 200
start_rect[2] += 10
start_rect[3] += 10

txt_add_words = menu_font.render("Add Words", True, color)
add_words_rect = txt_add_words.get_rect()
add_words_rect[0], add_words_rect[1] = 400, 300

txt_quit = menu_font.render("Quit", True, color)
quit_rect = txt_quit.get_rect()
quit_rect[0], quit_rect[1] = 400, 400


screen.fill((255, 255, 255))

pygame.draw.rect(screen, color, start_rect, 3, border_radius = 10)
pygame.draw.rect(screen, color, add_words_rect, 3, border_radius = 10)
pygame.draw.rect(screen, color, quit_rect, 3, border_radius = 10)


screen.blit(txt_start, start_rect)
screen.blit(txt_add_words, add_words_rect)
screen.blit(txt_quit, quit_rect)

while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if start_rect.collidepoint(event.pos):
                txt_start = menu_font.render("Start", True, inactive_color)
                print(type(txt_start))
                screen.blit(txt_start, start_rect)
                print("Start button has been clicked!!")

            elif add_words_rect.collidepoint(event.pos):
                txt_add_words = menu_font.render("Add Words", True, inactive_color)
                screen.blit(txt_add_words, add_words_rect)
                print("Add button has been clicked!!")

            elif quit_rect.collidepoint(event.pos):
                txt_quit = menu_font.render("Quit", True, inactive_color)
                screen.blit(txt_quit, quit_rect)
                print("Quit button has been clicked!!")

    clock.tick(30)
    pygame.display.flip()
