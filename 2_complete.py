import pygame , os , sys


pygame.init()




#1.사용자 게임 초기화
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

curr_path = os.path.dirname(__file__)
image_path = os.path.join(curr_path,"images")

# 배경이미지 가져오기

background = pygame.image.load(os.path.join(image_path,"background.png"))


# 스테이지 이미지 가져오기
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_height = stage.get_rect().size[1] #캐릭터 위치 위해서 필요

#무기 정의하기
weapon_speed = 30
weapons =[]
weapon_img = pygame.image.load(os.path.join(image_path,"arrow.png")).convert_alpha()

class Weapon(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.x_pos = 0
        self.y_pos = y_pos
        self.rect= image.get_rect()
        self.width = self.rect.size[0]


ball_images = [ pygame.image.load(os.path.join(image_path,"ball1.png")).convert_alpha(),
                pygame.image.load(os.path.join(image_path,"ball2.png")).convert_alpha(),
                pygame.image.load(os.path.join(image_path,"ball3.png")).convert_alpha(),
                pygame.image.load(os.path.join(image_path,"ball4.png")).convert_alpha(),]

balls = []
init_speed_y = [-18,-16,-14,-12]
#공 클래스 정의
class Ball(pygame.sprite.Sprite):
    def __init__(self,idx):
        super().__init__()
        self.image_idx = idx
        self.image = ball_images[self.image_idx]
        
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.x_pos = 50
        self.y_pos = 50

        self.to_x = 3
        self.to_y = -6


    def pop(self):
        if self.y_pos >= screen_height - stage_height - self.height :
            self.to_y = init_speed_y[self.image_idx]
        if self.x_pos <= 0 or self.x_pos >= screen_width - self.width:
            self.to_x = -1 * self.to_x
        self.to_y += 0.5
        #공 튕기기
        self.x_pos += self.to_x
        self.y_pos += self.to_y
        #rect정보 업데이트
        self.rect.left = self.x_pos
        self.rect.top = self.y_pos

    def draw(self,screen):
        screen.blit(self.image,(self.x_pos,self.y_pos))
    
    def left_small_ball(self,idx,x_pos,y_pos):
        global balls
        small_ball = Ball(idx)
        small_ball.to_x = -3
        small_ball.x_pos = x_pos
        small_ball.y_pos = y_pos
        small_ball.rect.left = small_ball.x_pos
        small_ball.rect.top = small_ball.y_pos
        
        balls.append(small_ball)
        
    def right_small_ball(self,idx,x_pos,y_pos):
        global balls
        small_ball = Ball(idx)
        small_ball.to_x = 3
        small_ball.x_pos = x_pos
        small_ball.y_pos = y_pos
        small_ball.rect.left = small_ball.x_pos
        small_ball.rect.top = small_ball.y_pos

        balls.append(small_ball)


        
character_height = 60
character_width = 33

#캐릭터 크기 맞추기
images = [pygame.image.load(os.path.join(image_path,"character_front.png")).convert_alpha(),
        pygame.image.load(os.path.join(image_path,"character_left.png")).convert_alpha(),
        pygame.image.load(os.path.join(image_path,"character_right.png")).convert_alpha()]
size = (character_width,character_height)
images = [pygame.transform.scale(image,size) for image in images]
# 캐릭터 클래스 정의
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





#공 만들기
ball= Ball(0)

balls.append(ball)

#캐릭터 만들기
player = Player()

#FPS(frame per second)
clock = pygame.time.Clock()
#제거될 공과 무기
ball_to_remove = -1
weapon_to_remove = -1
#총 시간
total_time = 30
start_ticks = pygame.time.get_ticks()
#폰트
game_font = pygame.font.SysFont("arial",40)
game_result = "Game Over"
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
                player.image = images[1]
                player.left_to_x -= player.speed
                player.x_pos += player.left_to_x
                
                 
            elif eve.key == pygame.K_RIGHT:
                player.image = images[2]
                player.right_to_x += player.speed
                player.x_pos += player.right_to_x
                
            elif eve.key == pygame.K_SPACE:
                x_pos = player.x_pos + player.width//2 
                y_pos = player.y_pos
                weapons.append([x_pos,y_pos])
               

        

        if eve.type == pygame.KEYUP:
 
            player.left_to_x = 0
            player.right_to_x = 0
        
         

        
    #3.캐릭터 위치 정의   
    if player.x_pos <= 0 :
        player.x_pos = 0
    elif player.x_pos >= screen_width - player.width :
        player.x_pos = screen_width - player.width 
    #무기 위치 
    weapons = [[w[0], w[1]-weapon_speed] for w in weapons]
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
    #

    #4.충돌 처리
    for ball_idx,ball in enumerate(balls):
        #화면에 공 튕기기
        ball.x_pos += ball.to_x
        ball.y_pos += ball.to_y
        ball.to_y += 0.5

        if ball.y_pos >= screen_height - stage_height - ball.height:
            ball.to_y = init_speed_y[ball.image_idx]
        if ball.x_pos <= 0 or ball.x_pos >= screen_width - ball.width:
            ball.to_x = -1 * ball.to_x

        ball.rect.left = ball.x_pos
        ball.rect.top = ball.y_pos
        #캐릭터 위치 정보 업데이트
        player.rect.left = player.x_pos
        player.rect.top = player.y_pos
        #충돌처리
        #공과 캐릭터 충돌
        if pygame.sprite.collide_mask(player,ball):
            game_result = "Game Over"
            running = False
            break

  
        # 공과 무기 충돌
        for w_idx,w_val in enumerate(weapons):
            ball.rect.left = ball.x_pos
            ball.rect.top = ball.y_pos
            #무기 정보 업데이트
            weapon = Weapon(weapon_img)  
            weapon.x_pos = w_val[0]
            weapon.y_pos = w_val[1]
            weapon.rect.left = weapon.x_pos
            weapon.rect.top = weapon.y_pos
            event = pygame.sprite.collide_mask(ball , weapon)
            if event :
                #공 두개로 나누기
                if ball_to_remove < 0 and ball.image_idx < 3:
                     
                    ball_to_remove = ball_idx
                    weapon_to_remove = w_idx
                    x_pos = ball.x_pos + ball.width//2 - ball.width//4
                    y_pos = ball.y_pos
                    ball.left_small_ball(ball.image_idx+1, x_pos,y_pos)
                    ball.right_small_ball(ball.image_idx+1, x_pos,y_pos)
                if ball.image_idx == 3:
                    del balls[ball_idx]
        #충돌한 공과 무기 삭제
        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

    
    if len(balls) == 0 :
        game_result = "Mission Complete"
        running = False

    #5.화면에 그리기
    screen.blit(background,(0,0))
   
    screen.blit(stage,(0,screen_height- stage_height))
    player.draw(screen)
    
    for ball in balls:
        screen.blit(ball.image,(ball.x_pos,ball.y_pos))
    
    #무기 그리기

    for w in weapons:
        screen.blit(weapon_img, (w[0],w[1]))
    WHITE = (255,255,255)
    elapsed_time = (pygame.time.get_ticks() - start_ticks)//1000 #ms -> s
    if total_time - elapsed_time < 0:
        game_result = "Time Over"
        running = False
    timer = game_font.render("TIme : {}".format(total_time - elapsed_time),True,WHITE)

    screen.blit(timer,(10,10))
    pygame.display.update()
    
msg = game_font.render(game_result,True,WHITE)
msg_size = msg.get_rect().size
msg_width = msg_size[0]
msg_height = msg_size[1]
screen.blit(msg,(screen_width//2 - msg_width//2, screen_height//2 - msg_height//2))

pygame.display.update()
pygame.time.delay(3000)
pygame.quit()
