import pygame
import os, math, random
pygame.init()
def get_bubble_position(row_idx,col_idx):
    x_pos = col_idx * CELLSIZE + CELL_WIDTH//2
    y_pos = row_idx * CELLSIZE + CELL_HEIGHT//2
    if row_idx %2 == 1:
        x_pos += CELL_WIDTH//2
    
    return x_pos , y_pos



def get_bubble_image(col):
    if col == 'B':
        return images[0]
    elif col == 'G':
        return images[1]
    elif col == 'R':
        return images[2]
    elif col == 'Y':
        return images[3]
    elif col == 'P':
        return images[4]
    

class Bubble(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)

#맵 그리기
    #lv3
map = [
    list("G......G"),
    list("RGBYRGB/"),
    list("Y......Y"),
    list("BYRGBYR/"),
    list("...R...."),
    list("...G.../"),
    list("...R...."),
    list("......./"),
    list("........"),
    list("......./"),
    list("........")
]
#스크린 설정
screen_width = 426
screen_height = 620
screen = pygame.display.set_mode((screen_width,screen_height))
#배경화면 불러오기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path,"background.png"))
#버블 그룹 
bubble_group = pygame.sprite.Group()
#버블 이미지
images = [pygame.image.load(os.path.join(current_path,"blue.png")),
            pygame.image.load(os.path.join(current_path,"green.png")),
            pygame.image.load(os.path.join(current_path,"red.png")),
            pygame.image.load(os.path.join(current_path,"yellow.png")),
            pygame.image.load(os.path.join(current_path,"purple.png")),
            pygame.image.load(os.path.join(current_path,"black.png"))
]
#포인터 이미지
pointer_img = pygame.image.load(os.path.join(current_path,"pointer.png"))
pointer_width = pointer_img.get_rect().size[0]
pointer_height = pointer_img.get_rect().size[1]
to_angle_left = 0
to_angle_right =0
angle_speed = 1.5

class Pointer(pygame.sprite.Sprite):
    def __init__(self ,image):
        super().__init__()
        self.image = image#전역변수 
        self.original_image = image
        self.position = (screen_width//2 , 590)
        self.rect = image.get_rect(center = self.position)
        self.angle = 0
        
    def rotate(self, to_angle):
        self.angle += to_angle

        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center = self.position)
#게임 관련 변수
pointer = Pointer(pointer_img)
CELLSIZE = 52
CELL_WIDTH = 52
CELL_HEIGHT = 56
to_angle_left = 0
to_angle_right = 0

#화면에 버블 그리기
def setup():
    global map
    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col not in ['.','/']:
                position = get_bubble_position(row_idx, col_idx)
                image = get_bubble_image(col)
            bubble_group.add(Bubble(image ,position))

setup()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle_left += angle_speed
            if event.key == pygame.K_RIGHT:
                to_angle_right -= angle_speed
        if event.type ==pygame.KEYUP:
            to_angle_left = 0
            to_angle_right =0
        pointer.rotate(to_angle_left + to_angle_right)   


    
    screen.blit(background,(0,0))
    screen.blit(pointer.image,pointer.rect)
    bubble_group.draw(screen)
    
    pygame.display.update()
        
           
pygame.quit()