import pygame
import os
#스크린 설정
screen_width = 448
screen_height = 620
screen = pygame.display.set_mode((screen_width,screen_height))
#배경화면 불러오기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path,"background.png"))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
           
pygame.quit()