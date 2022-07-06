import pygame
import os, math, random
pygame.init()

#스크린 설정
clock = pygame.time.Clock()
screen_width = 400
screen_height = 620
screen = pygame.display.set_mode((screen_width,screen_height))

def place_bubbles(bubble,row_idx,col_idx):
    global bubble_group
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble.set_map_index(row_idx,col_idx)
    bubble_group.add(bubble)
    
 

def remove_adjacent_bubbles(row_idx, col_idx,color):
    global visited
    visited.clear()

    visit(row_idx,col_idx,color)
    #버블 삭제하기
    if len(visited) >= 3:
        print(visited)
        remove_visited_bubbles()

    
def visit(row_idx, col_idx ,color):
    global visited
    if row_idx < 0 or row_idx > MAX_ROW_INDEX or col_idx < 0 or col_idx > MAX_COL_INDEX:
        return
    if map[row_idx][col_idx] != color:
        return
    if map[row_idx][col_idx] in ['.','/']:
        return
    if (row_idx,col_idx) in visited:
        return 
    visited.append((row_idx,col_idx))

    rows = [0, -1, -1, 0, 1, 1]
    cols = [-1, -1, 0, 1, 0, -1]
    if row_idx % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1, 1, 1, 0]

    for i in range(len(rows)):
        visit(row_idx + rows[i] ,col_idx + cols[i], color)

    

def remove_visited_bubbles():
    global bubble_group,visited
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx,b.col_idx) in visited]
    print(bubbles_to_remove)
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

    

    
def process_collision():
    global curr_bubble, fire
    hit_bubble = pygame.sprite.spritecollideany(curr_bubble,bubble_group,pygame.sprite.collide_mask)
    if hit_bubble:

        row_idx,col_idx = get_bubble_index(*curr_bubble.rect.center)
        
        place_bubbles(curr_bubble, row_idx,col_idx)
        remove_adjacent_bubbles(curr_bubble.row_idx,curr_bubble.col_idx,curr_bubble.color)
        curr_bubble = None
        fire= False
  

def get_bubble_index(x_pos,y_pos):
    row_idx = y_pos //CELLSIZE
    col_idx = x_pos //CELLSIZE

    if row_idx %2 ==1:
        col_idx = (x_pos - CELL_WIDTH//2) //CELLSIZE
        if col_idx <0 :
            col_idx = 0
        elif col_idx > MAX_COL_INDEX-1:
            col_idx =  MAX_COL_INDEX-1
        

    return row_idx,col_idx

def prepare_bubbles():
    global curr_bubble,next_bubble

    if not next_bubble:
        next_bubble = create_bubbles()
    curr_bubble = next_bubble
    curr_bubble.set_rect((screen_width//2,590))

    next_bubble = create_bubbles()
    next_bubble.set_rect((screen_width//4,600))

def create_bubbles():
    col = get_random_bubble_color()
    image = get_bubble_image(col)
    
    return Bubble(image,col)

def get_random_bubble_color():
    global map
    colors =[]
    for row in map:
        for col in row:
            if col not in ['.','/']:
                if col not in colors:
                    colors.append(col)
    return random.choice(colors)

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
    def __init__(self,image,col,position=(0,0),row_idx=0,col_idx=0):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)
        self.angle = 0
        self.rad_angle = 0
        self.radius = 18
        self.position = position
        self.color = col
        self.row_idx = row_idx
        self.col_idx = col_idx

    def set_angle(self ,angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle)
    def set_rect(self,position):
        self.rect = self.image.get_rect(center = position)
    def move(self):
        global curr_bubble,fire
        to_x = math.cos(self.rad_angle) * self.radius
        to_y = math.sin(self.rad_angle) * self.radius * -1
        
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180-self.angle)
            to_x = math.cos(self.rad_angle) * self.radius
        if self.rect.top < 0:
            curr_bubble = None
            fire = False

        self.rect.x += to_x
        self.rect.y += to_y  

    def set_map_index(self,row,col):
        self.row_idx = row
        self.col_idx = col
    def draw(self,screen):
        screen.blit(self.image,self.rect)


        
    



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

#배경화면 불러오기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path,"background.png"))
#버블 그룹 
bubble_group = pygame.sprite.Group()
#버블 이미지
images = [pygame.image.load(os.path.join(current_path,"blue.png")).convert_alpha(),
            pygame.image.load(os.path.join(current_path,"green.png")).convert_alpha(),
            pygame.image.load(os.path.join(current_path,"red.png")).convert_alpha(),
            pygame.image.load(os.path.join(current_path,"yellow.png")).convert_alpha(),
            pygame.image.load(os.path.join(current_path,"purple.png")).convert_alpha(),
            pygame.image.load(os.path.join(current_path,"black.png")).convert_alpha()
]
#포인터 이미지
pointer_img = pygame.image.load(os.path.join(current_path,"pointer.png"))
pointer_width = pointer_img.get_rect().size[0]
pointer_height = pointer_img.get_rect().size[1]
to_angle_left = 0
to_angle_right =0
angle_speed = 5

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
CELLSIZE = 50
CELL_WIDTH = 50
CELL_HEIGHT = 56
to_angle_left = 0
to_angle_right = 0
fire = False
curr_bubble = None
next_bubble = None
MAX_ROW_INDEX = 9
MAX_COL_INDEX = 7
visited = []
#화면에 버블 그리기
def setup():
    global map
    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col not in ['.','/']:
                position = get_bubble_position(row_idx, col_idx)
                image = get_bubble_image(col)
            bubble_group.add(Bubble(image,col,position,row_idx,col_idx))

setup()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle_left += angle_speed
            if event.key == pygame.K_RIGHT:
                to_angle_right -= angle_speed
            if event.key == pygame.K_SPACE:
                curr_bubble.set_angle(pointer.angle)
                fire = True

            pointer.rotate(to_angle_left + to_angle_right)  

        if event.type ==pygame.KEYUP:
            to_angle_left = 0
            to_angle_right =0
         

    if not curr_bubble:
        prepare_bubbles()
            
    if fire:
        process_collision()
            
            
    
    screen.blit(background,(0,0))
    screen.blit(pointer.image,pointer.rect)
    bubble_group.draw(screen)
    if curr_bubble:
        if fire:
            curr_bubble.move()
        curr_bubble.draw(screen)
    if next_bubble:
        next_bubble.draw(screen)
    
    pygame.display.update()
        
           
pygame.quit()