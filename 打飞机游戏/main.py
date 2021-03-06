import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('King\'s flight war')

background = pygame.image.load('images/background.png').convert()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

#载入背景音乐：
pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc
        

def main():
    pygame.mixer.music.play(-1)

    #生成我放飞机
    me = myplane.MyPlane(bg_size)
    #生成敌方飞机
    enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 10)

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,8)

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 4
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 8
    for i in range(bullet2_num//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30,me.rect.centery)))

    #飞机毁灭图片
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #统计得分
    score = 0
    score_font = pygame.font.Font('font/font.ttf', 36)

    #标识是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10,10
    paused_image = pause_nor_image

    #设置难度级别
    level = 1

    #全屏炸弹
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('font/font.ttf',48)
    bomb_num = 5

    #每30S发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,25*1000)

    #超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    #无敌定时器
    INVINCIBLE_TIME =USEREVENT + 2 

    #标志是使用超级子弹
    is_double_bullet = False

    clock = pygame.time.Clock()
    #用于切换图片
    switch_image = True
    #延时变量
    delay = 100
    #判断是否记录
    recorded = False

    #生命数量
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    #游戏结束画面
    gameover_font = pygame.font.Font('font/font.ttf',48)
    again_image = pygame.image.load('images/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load('images/gameover.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()

    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME,30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

                        
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME,0)

        #根据用户的分来提升难度
        if level == 1 and score > 10000:
            level = 2
            upgrade_sound.play()
            #增加飞机
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            #提升小型飞机速度
            inc_speed(small_enemies,1)
            
        elif level == 2 and score > 40000:
            level = 3
            upgrade_sound.play()
            #增加飞机
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            #提升小型飞机速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            
        elif level == 3 and score > 100000:
            level = 4
            upgrade_sound.play()
            #增加飞机
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            #提升小型飞机速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        elif level == 4 and score > 500000:
            level = 5
            upgrade_sound.play()
            #增加飞机
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            #提升小型飞机速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
                        
        screen.blit(background,(0,0))
        if not paused and life_num:
            #检测用户键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            #绘制全屏炸弹并检测是否获得

            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num<9:
                        bomb_num += 1
                    bomb_supply.active = False

            #绘制超级子弹补给并检测是否获得

            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,18*1000)
                    bullet_supply.active = False
                    


            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx + 30,me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num

            #检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.life -= 1
                                if e.life == 0:
                                    e.active = False
                            else:
                                e.active = False
                         
            
            #检测我放飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me,enemies,False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            
            
            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                 #毁灭飞机
                me_down_sound.play()
                if not (delay % 3):
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME,3 * 1000)
            #绘制生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,\
                                (width-10-(i+1)*life_rect.width,\
                                 height - 10 - life_rect.height))
                        
            score_text = score_font.render('Score : %s'%str(score),True,WHITE)
            screen.blit(score_text,(10,5))
                        
                
            #切换图片
            if not (delay % 5):
                switch_image = not switch_image
                
            #绘制敌方飞机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit == True:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:     
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    #绘制血槽
                    pygame.draw.line(screen, BLACK,\
                                     (each.rect.left, each.rect.top - 5),\
                                     (each.rect.right,each.rect.top - 5), 2)
                    #当生命大于20%显示绿色，否则红色
                    life_remain = each.life / enemy.BigEnemy.life
                    if life_remain > 0.2:
                        life_color = GREEN
                    else:
                        life_color = RED
                    pygame.draw.line(screen,life_color,\
                                     (each.rect.left, each.rect.top - 5),\
                                     (each.rect.left + each.rect.width*life_remain, each.rect.top - 5),2)
                        
                    #大飞机来临前播放音效
                    if each.rect.bottom > -50:
                        enemy3_fly_sound.play()
                else:
                    #毁灭飞机
                    if not (delay % 3):
                        if e3_destroy_index == 1:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()
                        
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit == True:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else: 
                        screen.blit(each.image,each.rect)
                    #绘制血槽
                    pygame.draw.line(screen, BLACK,\
                                     (each.rect.left, each.rect.top - 5),\
                                     (each.rect.right,each.rect.top - 5), 2)
                    #当生命大于20%显示绿色，否则红色
                    life_remain = each.life / enemy.MidEnemy.life
                    if life_remain > 0.2:
                        life_color = GREEN
                    else:
                        life_color = RED
                    pygame.draw.line(screen,life_color,\
                                     (each.rect.left, each.rect.top - 5),\
                                     (each.rect.left + each.rect.width*life_remain, each.rect.top - 5),2)
                else:
                    #毁灭飞机
                    
                    if not (delay % 3):
                        if e2_destroy_index == 1:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 1000
                            each.reset()

            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    #毁灭飞机
                    
                    if not (delay % 3):
                        if e1_destroy_index == 1:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 500
                            each.reset()

                            
            #绘制炸弹数量
            bomb_text = bomb_font.render('* %d'%bomb_num,True,WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image,(10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text,(20+ bomb_rect.width,height - 5 - text_rect.height))

        #绘制游戏结束画面
        elif life_num == 0:
            
            #音乐停止
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            #补给停止
            pygame.time.set_timer(SUPPLY_TIME,0)
            if not recorded:
                recorded = not recorded 

                #读取历史最高分
                with open('record.txt','r') as f:
                    record_score = int(f.read())

                #如果玩家得分高于存档，则覆盖存档

                if score > record_score:
                    with open('record.txt','w') as f:
                        f.write(str(score))
            #绘制结束画面
            record_score_text = score_font.render('Best : %d'%record_score,True,(255,255,255))
            screen.blit(record_score_text,(50,50))

            gameover_text1 = gameover_font.render('You Score', True, (255,255,255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                      (width - gameover_text1_rect.width)//2,\
                                      height // 2
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score),True, (255,255,255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                      (width - gameover_text2_rect.width)//2,\
                                      height // 2 + 50
            
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width)//2,\
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image,again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width)//2,\
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            #检测用户鼠标操作
            if pygame.mouse.get_pressed()[0]:
                pos = pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and\
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()
                    
                    
        #绘制暂停按钮
        screen.blit(paused_image,paused_rect)

        
        
        

        delay -= 1
        if not delay:
            delay = 100
        switch_image = not switch_image
        

        pygame.display.flip()
        
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
                
        
                                       
