# Importing all modules that we required
import random
import time
import pygame
pygame.init()
from pygame import mixer
mixer.init()

screen_b,screen_h = 1280,720     # DISPLAY RESOLUTION

screen = pygame.display.set_mode((screen_b,screen_h))
pygame.display.set_caption('Long Drive with Jayant')

# DISPLAY COLOR FILL = WHITE
screen.fill('#FFFFFF')
pygame.display.update()
clock=pygame.time.Clock()

# LOADING SOUNDS
click_s= mixer.Sound("sound/click.wav")
crash_s= mixer.Sound("sound/crash.wav")
loading_s= mixer.Sound("sound/loading.wav")
coundown_s= mixer.Sound("sound/countdowns.wav")
win1= mixer.Sound("sound/win1.wav")
win2= mixer.Sound("sound/win2.wav")
score_sound= mixer.Sound("sound/score.wav")
power_sound= mixer.Sound("sound/powers.wav")
change_sound= mixer.Sound("sound/change.wav")
gameover_sound= mixer.Sound("sound/game-over.wav")


# LOADING BACKGROUND MUSIC
bg_m=mixer.music.load("sound/bg_y.mp3")


# IMAGES OF HOME SCREEN
introImg = pygame.image.load("sprites/home/introimg.jpg").convert_alpha()
s1 = pygame.image.load("sprites/home/starty.jpg").convert_alpha()
s2 = pygame.image.load("sprites/home/startw.jpg").convert_alpha()
sett1 = pygame.image.load("sprites/home/settingsy.jpg").convert_alpha()
sett2 = pygame.image.load("sprites/home/settingsw.jpg").convert_alpha()
a1 = pygame.image.load("sprites/home/abouty.jpg").convert_alpha()
a2 = pygame.image.load("sprites/home/aboutw.jpg").convert_alpha()
e1 = pygame.image.load("sprites/home/exity.jpg").convert_alpha()
e2 = pygame.image.load("sprites/home/exitw.jpg").convert_alpha()


# GAME LOOP IMAGES
roadi = pygame.image.load("sprites/gameplay/roadi.jpg").convert_alpha()
bgimg = pygame.image.load("sprites/gameplay/bg1.jpg").convert_alpha()
loading_img = pygame.image.load("sprites/gameplay/loadingi.jpg").convert_alpha()
score_img = pygame.image.load("sprites/gameplay/score_img.png").convert_alpha()
speed_img = pygame.image.load("sprites/gameplay/speed_i.png").convert_alpha()
fuel_over_img = pygame.image.load("sprites/gameplay/fuel_over.png").convert_alpha()
crash_img = pygame.image.load("sprites/gameplay/crash.png").convert_alpha()
fuel_power_img = pygame.image.load("sprites/gameplay/fuel_power.png").convert_alpha()
pause1_img = pygame.image.load("sprites/gameplay/pause1.jpg").convert_alpha()
pause2_img = pygame.image.load("sprites/gameplay/pause2.jpg").convert_alpha()

# PAUSE LOOP IMAGES
p1_img = pygame.image.load("sprites/gameplay/p1.jpg").convert_alpha()
p2_img = pygame.image.load("sprites/gameplay/p2.jpg").convert_alpha()
p3_img = pygame.image.load("sprites/gameplay/p3.jpg").convert_alpha()
p4_img = pygame.image.load("sprites/gameplay/p4.jpg").convert_alpha()
p5_img = pygame.image.load("sprites/gameplay/p5.jpg").convert_alpha()
p6_img = pygame.image.load("sprites/gameplay/p6.jpg").convert_alpha()
pause_bg_img = pygame.image.load("sprites/gameplay/pause_bg.jpg").convert_alpha()

# SETTINGS IMAGES
settings_bg_img = pygame.image.load("sprites/setting/settingd_bg.jpg").convert_alpha()
r1 = pygame.image.load("sprites/setting/setting_button/r1.png").convert_alpha()
r2 = pygame.image.load("sprites/setting/setting_button/r2.png").convert_alpha()
l1 = pygame.image.load("sprites/setting/setting_button/l1.png").convert_alpha()
l2 = pygame.image.load("sprites/setting/setting_button/l2.png").convert_alpha()

difficulty_img = pygame.image.load("sprites/setting/difficulty.png").convert_alpha()
sensitivity_img = pygame.image.load("sprites/setting/sensitivity.png").convert_alpha()
save_img_1 = pygame.image.load("sprites/setting/save1.jpg").convert_alpha()
save_img_2 = pygame.image.load("sprites/setting/save2.jpg").convert_alpha()

# GAME OVER IMAGES
game_over_img = pygame.image.load("sprites/setting/game over bg_2.jpg").convert_alpha()
exit1_img = pygame.image.load("sprites/setting/exit1.jpg").convert_alpha()
exit2_img = pygame.image.load("sprites/setting/exit2.jpg").convert_alpha()



# ABOUT SECTION IMG
aboutimg = pygame.image.load("sprites/home/instructionimg.jpg").convert_alpha()
b1 = pygame.image.load("sprites/home/backy.jpg").convert_alpha()
b2 = pygame.image.load("sprites/home/backw.jpg").convert_alpha()



# GLOBAL VARIABLES
p_t=0  # CAR TYPE
player_x = 590
FPS=120  # ALL OVER GAME LOOP FPS
petrol=13
g_sensitivity=5   # FOR PLAYER CAR'S MOVEMENTS
enemy_speed=1     # ENEMY CAR'S SPEED COMING FROM OPPOSITE DIRECTION


def show_petrol(petrol):
    if petrol>=1:
        petrol_type = petrol
        petrol_img = pygame.image.load(f"sprites/petrol/{petrol_type}.png").convert_alpha()
        screen.blit(petrol_img, (1017, 370))



def show_level(level):
    if level<11:
        level_type = level
        level_i = pygame.image.load(f"sprites/levels/{level_type}.png").convert_alpha()
        screen.blit(level_i, (0, 0))
        pygame.display.update()
        mixer.Sound.play(click_s)
        time.sleep(2)



def show_score(score,level,car_speed):
    screen.blit(score_img,(0,10))

    # SCORE TEXT
    score_font=pygame.font.SysFont("NONE",85)
    score_fontr= score_font.render(f"{score}",1,(0,0,0))
    screen.blit(score_fontr,(190,22))

    # LEVEL TEXT
    level_font = pygame.font.SysFont("NONE", 65)
    level_fontr = level_font.render(f"{level}", 1, (0, 0, 0))
    screen.blit(level_fontr, (205, 113))

    # SPEED TEXT
    screen.blit(speed_img,(1125,200))
    speed_font = pygame.font.SysFont("NONE", 50)
    speed_fontr = speed_font.render(f"{car_speed*10}km/h", 1, (255,255,255))
    screen.blit(speed_fontr, (1133, 250))


def collison(ex,ey, player_x,px,py,score):
    global petrol
    # FOR ROAD BOUNDARIES
    if player_x > 870 or player_x < 315 or ey>2000:
        mixer.music.stop()
        mixer.Sound.play(crash_s)
        screen.blit(crash_img,(0,0))
        pygame.display.update()
        time.sleep(2)
        game_over(score)
    # FOR ENEMY CARS
    if ey+178 > 550:
        if player_x+80 > ex and player_x < ex+80:
            mixer.music.stop()
            mixer.Sound.play(crash_s)
            screen.blit(crash_img, (0, 0))
            pygame.display.update()
            time.sleep(2)
            game_over(score)
    # FOR LOW PETROL
    if petrol<1:
        mixer.music.stop()
        mixer.Sound.play(crash_s)
        screen.blit(fuel_over_img,(0,0))
        pygame.display.update()
        time.sleep(2)
        game_over(score)
    # FOR FUEL POWER
    if petrol<=7:
        if py + 178 > 550:
            if player_x + 80 > px and player_x < px + 80:
                mixer.Sound.play(power_sound)
                petrol=13




def create_enemy(ex, ey, et):
    enemy_type=et
    enemy = pygame.image.load(f"sprites/cars/{enemy_type}.png").convert_alpha()
    enemy = pygame.transform.rotate(enemy, 180)
    screen.blit(enemy, (ex, ey))


def create_fuel_power(px,py):
    screen.blit(fuel_power_img,(px,py))


def player_move(ml, mr):
    global player_x
    global g_sensitivity
    if ml:
        player_x-=g_sensitivity
    if mr:
        player_x+=g_sensitivity


def create_player(x,y,pt):
    player_type=pt
    player = pygame.image.load(f"sprites/cars/{player_type}.png").convert_alpha()
    screen.blit(player, (x, y))


def create_road(x,y):
    screen.blit(roadi, (x,y))


def create_trees(x,y,t):
    tree_type=t
    tree = pygame.image.load(f"sprites/trees/{tree_type}.png").convert_alpha()
    screen.blit(tree, (x, y))


def coundown():
    coundown_v=True
    i = 1
    # time.sleep(0.5)
    mixer.Sound.play(coundown_s)

    global p_t
    while coundown_v:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                coundown_v = False
                pygame.quit()
                quit()
        screen.blit(roadi, (0, 0))
        player = pygame.image.load(f"sprites/cars/{p_t}.png").convert_alpha()
        screen.blit(player,(590,530))

        if i<=15:
            ci = pygame.image.load("sprites/coundown/0.png").convert_alpha()
            screen.blit(ci, (0, 0))
        if i<=35 and i >15:
            ci = pygame.image.load("sprites/coundown/1.png").convert_alpha()
            screen.blit(ci, (0, 0))
        if i<=60 and i >35:
            ci = pygame.image.load("sprites/coundown/2.png").convert_alpha()
            screen.blit(ci, (0, 0))
        if i >60:
            ci = pygame.image.load("sprites/coundown/3.png").convert_alpha()
            screen.blit(ci, (0, 0))
        if i>100:
            coundown_v=False
        i+=1
        pygame.display.update()
        clock.tick(30)


def game_over(score):
    game_over_v = True
    mixer.Sound.play(gameover_sound)
    while game_over_v:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_v = False
                pygame.quit()
                quit()
        screen.blit(game_over_img, (0, 0))
        game_over_font = pygame.font.SysFont("NONE", 220)
        game_over_fontr = game_over_font.render(f"{score}", 1, (255, 255, 255))
        screen.blit(game_over_fontr, (18, 513))
        screen.blit(exit1_img,(1190,630))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 1270 > mouse[0] > 1190 and 710 > mouse[1] > 630:
            screen.blit(exit2_img, (1190,630))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                game_over_v=False
                intro_loop()
        pygame.display.update()
        clock.tick(30)

def pause_loop():
    pause_v = True
    while pause_v:
        screen.blit(pause_bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pause_v=False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mixer.music.play(15)
                    pause_v=False

        screen.blit(p3_img, (590, 360))
        screen.blit(p1_img, (320, 360))
        screen.blit(p5_img, (860, 360))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 420 > mouse[0] > 320 and 460 > mouse[1] > 360:
            screen.blit(p2_img, (320, 360))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                pause_v=False
                intro_loop()
        if 690 > mouse[0] > 590 and 460 > mouse[1] > 360:
            screen.blit(p4_img, (590, 360))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.50)
                mixer.music.play(15)
                pause_v = False
        if 960 > mouse[0] > 860 and 460 > mouse[1] > 360:
            screen.blit(p6_img, (860, 360))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                pause_v=False
                game_loop()
        pygame.display.update()
        clock.tick(30)

def game_loop():
    coundown()
    mixer.music.play(15)
    mixer.music.set_volume(0.5)
    game_v = True

    global FPS

    rx=0               # ROAD FRAME 1 & 2 X-COORDINATES
    ry1=-710           # ROAD FRAME 1 Y-COORDINATES
    ry2=0              # ROAD FRAME 2 Y-COORDINATES
    car_speed=0        # INITIAL PLAYER CAR SPEED
    car_speedlimit=7   # CAR SPEED LIMIT-80 km/h

    tlx=1              # LEFT SIDE TREES X-COORDINATES
    trx=1103           # RIGHT SIDE TREES X-COORDINATES
    tly1=-200          # LEFT SIDE TREES Y-COORDINATES
    try1=-500          # RIGHT SIDE TREES Y-COORDINATES

    # TREES TYPE SELECTION
    t1=random.randint(0,8)
    t2=random.randint(0,8)

    global p_t

    global player_x
    player_y=530       # PLAYER CAR CONSTANT X-COORDINATES
    player_x=590       # PLAYER CAR INITIAL X-COORDINATES
    ml=False           # MOVING LEFT VAR
    mr=False           # MOVING RIGHT VAR
    global enemy_speed
    enemy_speed=1

    # ENEMY CARS RANDOM POSITIONS
    ex=random.randint(330,855)
    ey=random.randint(180,screen_h)
    ey=-ey
    et=random.randint(0,17)


    score=0
    level=1
    level_check=250     # AFTER THE SCORE OF 250 LEVEL CHANGE
    copy_lc = 2         # CALCULATION VARIABLE

    global petrol
    petrol=13
    distance=0
    distance_lc=2
    petrol_check=2

    # FUEL CARS RANDOM POSITIONS
    px=random.randint(330,855)
    py=random.randint(180,screen_h)
    py=-py

    while game_v:
        screen.fill('#008f00')
        # screen.blit(bgimg,(0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_v = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if car_speed<=car_speedlimit:
                        car_speed+=1
                        enemy_speed+=1
                if event.key == pygame.K_DOWN:
                    if car_speed>0:
                        car_speed-=1
                        enemy_speed-=1

                if event.key == pygame.K_LEFT:
                    ml=True
                if event.key == pygame.K_RIGHT:
                    mr=True
                if event.key == pygame.K_SPACE:
                    mixer.music.stop()
                    pause_loop()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    ml=False
                if event.key == pygame.K_RIGHT:
                    mr=False


        ry1+=car_speed
        ry2+=car_speed
        if ry2>=screen_h :
            ry1= -screen_h
            ry2=0
            distance+=1




        create_road(rx,ry1)
        create_road(rx,ry2)

        tly1 += car_speed
        try1 += car_speed
        if tly1>=screen_h:
            t1=random.randint(0,8)
            tly1=random.randint(175,screen_h)
            tly1=-tly1

        if try1>=screen_h:
            t2=random.randint(0,8)
            try1=random.randint(175,screen_h)
            try1=-try1


        create_trees(tlx,tly1,t1)
        create_trees(trx,try1,t2)


        player_move(ml,mr)
        create_player(player_x,player_y,p_t)


        ey+=enemy_speed
        if ey>=screen_h and car_speed>0:
            score+=10

            ex = random.randint(330, 855)
            ey = random.randint(180, screen_h)
            et = random.randint(0, 17)
            ey = -ey
            if score == level_check:
                level += 1
                show_level(level)
                enemy_speed += 2
                level_check = 250 * copy_lc
                copy_lc += 1
            else:
                mixer.Sound.play(score_sound)

        create_enemy(ex,ey,et)

        if py == screen_h//2:
            petrol_check = 2 * distance_lc
            distance_lc += 1
            petrol-=1

        if petrol==13:
            px = random.randint(330, 855)
            py = random.randint(180, screen_h)
            py = -py

        if petrol<=7:
            py+=1
            create_fuel_power(px,py)


        collison(ex,ey,player_x,px,py,score)


        show_score(score,level,car_speed)

        if distance == petrol_check:
            petrol_check = 2 * distance_lc
            distance_lc += 1
            petrol-=1

        show_petrol(petrol)
        screen.blit(pause1_img,(1180,20))

        pygame.display.update()
        clock.tick(FPS)

def show_settings_cars(s_car_t,difficulty_type,sensitivity_type):
    global p_t
    global g_sensitivity
    global enemy_speed

    if difficulty_type==2:
        enemy_speed=3
    elif difficulty_type==0:
        enemy_speed=1
    elif difficulty_type==1:
        enemy_speed=2

    if sensitivity_type==2:
        g_sensitivity=8
    elif sensitivity_type==0:
        g_sensitivity=3
    elif sensitivity_type==1:
        g_sensitivity=5

    # CHANGING CARS IN SETTINGS WINDOW
    p_t=s_car_t

    car_type=s_car_t
    car_change = pygame.image.load(f"sprites/setting/settings_cars/{car_type}.png").convert_alpha()
    screen.blit(car_change,(555,230))
    difficulty_change=pygame.image.load(f"sprites/setting/{difficulty_type}.png").convert_alpha()
    screen.blit(difficulty_change,(80,320))
    sensitivity_change=pygame.image.load(f"sprites/setting/{sensitivity_type}.png").convert_alpha()
    screen.blit(sensitivity_change,(1020,320))

def settings():
    settings_v = True
    global enemy_speed
    enemy_speed=1
    global g_sensitivity
    g_sensitivity=5
    s_car_t=0
    difficulty_type=0
    sensitivity_type=1

    while settings_v:
        screen.blit(settings_bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_v = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mixer.Sound.play(change_sound)
                    time.sleep(0.25)
                    s_car_t -= 1
                    if s_car_t < 0:
                        s_car_t = 0
                if event.key == pygame.K_RIGHT:
                    mixer.Sound.play(change_sound)
                    time.sleep(0.25)
                    s_car_t += 1
                    if s_car_t > 17:
                        s_car_t = 17


        screen.blit(l1,(395,330))
        screen.blit(r1,(774,330))

        screen.blit(difficulty_img,(80,320))
        screen.blit(sensitivity_img,(1020,320))
        screen.blit(save_img_1,(590,550))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 505 > mouse[0] > 395 and 500 > mouse[1] > 330:
            screen.blit(l2, (395,330))
            if click == (1, 0, 0):
                mixer.Sound.play(change_sound)
                time.sleep(0.25)
                s_car_t-=1
                if s_car_t<0:
                    s_car_t=0

        if 885 > mouse[0] > 775 and 500 > mouse[1] > 330:
            screen.blit(r2, (774,330))
            if click == (1, 0, 0):
                mixer.Sound.play(change_sound)
                time.sleep(0.25)
                s_car_t += 1
                if s_car_t > 17:
                    s_car_t = 17

        if 690 > mouse[0] > 590 and 580 > mouse[1] > 550:
            screen.blit(save_img_2, (590,550))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                settings_v=False
                intro_loop()

        if 120 > mouse[0] > 78 and 496 > mouse[1] > 442:
            if click == (1, 0, 0):
                mixer.Sound.play(change_sound)
                time.sleep(0.25)
                difficulty_type-=1
                if difficulty_type<0:
                    difficulty_type=0

        if 260 > mouse[0] > 220 and 496 > mouse[1] > 442:
            if click == (1, 0, 0):
                mixer.Sound.play(change_sound)
                time.sleep(0.25)
                difficulty_type += 1
                if difficulty_type > 2:
                    difficulty_type = 2

        if 1060 > mouse[0] > 1018 and 496 > mouse[1] > 442:
            if click == (1, 0, 0):
                mixer.Sound.play(change_sound)
                time.sleep(0.25)
                sensitivity_type-=1
                if sensitivity_type<0:
                    sensitivity_type=0

        if 1200 > mouse[0] > 1160 and 496 > mouse[1] > 442:
            if click == (1, 0, 0):
                mixer.Sound.play(change_sound)
                time.sleep(0.25)
                sensitivity_type += 1
                if sensitivity_type > 2:
                    sensitivity_type = 2

        show_settings_cars(s_car_t,difficulty_type,sensitivity_type)

        pygame.display.update()
        clock.tick(30)

def about():
    about_v = True
    while about_v:
        screen.blit(aboutimg, (0, 0))

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                about_v=False
                pygame.quit()
                quit()
        screen.blit(b1, (490, 625))
        mouse = pygame.mouse.get_pos()

        click = pygame.mouse.get_pressed()
        if 790 > mouse[0] > 490 and 710 > mouse[1] > 625:
            screen.blit(b2, (490, 625))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                about_v=False
                intro_loop()
        pygame.display.update()
        clock.tick(30)


def intro_loop():
    intro_v = True
    while intro_v:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                intro_v=False
                pygame.quit()
                quit()
        screen.blit(introImg, (0, 0))
        screen.blit(s1, (900, 100))
        screen.blit(sett1, (900, 230))
        screen.blit(a1, (900, 360))
        screen.blit(e1, (900, 490))

        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        # START
        if 1250 > mouse[0] > 900 and 200 > mouse[1] > 100:
            screen.blit(s2,(900,100))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                intro_v=False
                game_loop()
        # SETTINGS
        if 1250 > mouse[0] > 900 and 330 > mouse[1] > 230:
            screen.blit(sett2,(900,230))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                intro_v=False
                settings()
        # ABOUT
        if 1250 > mouse[0] > 900 and 460 > mouse[1] > 360:
            screen.blit(a2, (900, 360))
            if click == (1, 0, 0):
                mixer.Sound.play(click_s)
                time.sleep(0.25)
                intro_v=False
                about()
        # EXIT
        if 1250 > mouse[0] > 900 and 590 > mouse[1] > 490:
            screen.blit(e2, (900, 490))
            if click==(1,0,0):
                mixer.Sound.play(click_s)
                time.sleep(1)
                intro_v = False
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(30)

def loading():
    loading_v=True
    i=1
    mixer.Sound.play(loading_s)
    while loading_v:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                loading_v=False
                pygame.quit()
                quit()
        screen.blit(loading_img,(0,0))
        pygame.display.update()
        i+=1
        if(i//30>=4):
            loading_v=False
            intro_loop()
        clock.tick(30)



loading()
pygame.quit()
quit()