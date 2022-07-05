import pygame , os
pygame.init()
curr_path = os.path.dirname(__file__)
image_path = os.path.join(curr_path,"images")



#FPS(frame per second)
clock = pygame.time.Clock()
#캐릭터 크기 맞추기
images = [pygame.image.load(os.path.join(image_path,"character_front.png")).convert_alpha(),
        pygame.image.load(os.path.join(image_path,"character_left.png")).convert_alpha(),
        pygame.image.load(os.path.join(image_path,"character_right.png")).convert_alpha()]
size = (33,60)
images = [pygame.transform.image(image,size) for image in images]

class Player(pygame.sprite.Sprite):
    def __init__(self,image = images[0]):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.left_to_x = 0
        self.right_to_x = 0
        self.to_y = 0
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x_pos = screen_width//2 - self.width//2
        self.y_pos = screen_height - stage_height - self.height
        self.speed = 30

    def draw(self,screen):
        screen.blit(self.image,(self.x_pos,self.y_pos))



#1.사용자 게임 초기화
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))


# 배경이미지 가져오기

background = pygame.image.load(os.path.join(image_path,"background.png"))


# 스테이지 이미지 가져오기
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_height = stage.get_rect().size[1] #캐릭터 위치 위해서 필요

#캐릭터 만들기
player = Player()

#2.이벤트 처리
running = True
while running:
    #clock.tick은 각 루프를 도는 시간 반환 
    #mt = clock.tick(60)/1000 #루프 한번 도는 시간(ms->s)
    events = pygame.event.get()
    clock.tick(60)
    for eve in events:
        if eve.type == pygame.QUIT:
            running = False
    
        if eve.type == pygame.KEYDOWN:
            if eve.key == pygame.K_LEFT:
                player.image = pygame.image.load(os.path.join(image_path,"7.png")).convert_alpha()
                player.left_to_x -= player.speed
            elif eve.key == pygame.K_RIGHT:
                player.image = pygame.image.load(os.path.join(image_path,"right.png")).convert_alpha()
                player.right_to_x += player.speed
            
        if eve.type == pygame.KEYUP:
            
            if eve.key == pygame.K_LEFT:
                player.left_to_x = 0
            elif eve.key == pygame.K_RIGHT:
                player.right_to_x = 0
        
        player.x_pos += player.left_to_x + player.right_to_x

#3.캐릭터 위치 정의   
    if player.x_pos <= 0 :
        player.x_pos = 0
    elif player.x_pos >= screen_width - player.width:
        player.x_pos = screen_width - player.width

    #4.충돌 처리
    # 공과 캐릭터 충돌
    

    #5.화면에 그리기
    screen.blit(background,(0,0))
   
    
    screen.blit(stage,(0,screen_height- stage_height))
    player.draw(screen)
    pygame.display.update()
    


pygame.quit()
