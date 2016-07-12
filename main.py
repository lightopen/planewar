#coding=gbk
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Plane War")

background = pygame.image.load(r"images/background.png").convert()

# ������Ϸ����
pygame.mixer.music.load(r"sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound(r"sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound(r"sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound(r"sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound(r"sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound(r"sound/get_bullet.wav")
get_bomb_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound(r"sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound(r"sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound(r"sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound(r"sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound(r"sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound(r"sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.SmallEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)
		
def add_mid_enemies(group1, group2, num):
	for i in range(num):
		e2 = enemy.MidEnemy(bg_size)
		group1.add(e2)
		group2.add(e2)
		
def add_big_enemies(group1, group2, num):
	for i in range(num):
		e3 = enemy.BigEnemy(bg_size)
		group1.add(e3)
		group2.add(e3)

def inc_speed(target, num):
	for each in target:
		each.speed += mun

class Level(object):
	
	def __init__(self):
		self.level_base = 1
		self.score_base = 50000
		
	def add_level(self):
		self.level_base += 1
		self.score_base *= 3
		
def main():
	pygame.mixer.music.play(-1)
	
	clock = pygame.time.Clock()
	
	running = True
	
	BLACK = (0, 0, 0)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)
	WHITE = (255, 255, 255)
	
	#�����ҷ��ɻ�
	me = myplane.MyPlane(bg_size)
	delay = 100
	switch_image = True

	enemies = pygame.sprite.Group()
	
	#����С�ͷɻ�
	small_enemies = pygame.sprite.Group()
	add_small_enemies(small_enemies, enemies, 15)
	
	#�������ͷɻ�
	mid_enemies = pygame.sprite.Group()
	add_mid_enemies(mid_enemies, enemies, 4)
	
	#���ɴ��ͷɻ�
	big_enemies = pygame.sprite.Group()
	add_big_enemies(big_enemies, enemies, 2)
	
	#������ͨ�ӵ�
	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4
	for i in range(BULLET1_NUM):
		bullet1.append(bullet.Bullet1(me.rect.midtop))
	
	# �����Ѷ�ϵ��, ͳ�Ƶ÷�
	level = 1
	level_instance = Level()
	score = 0
	score_font = pygame.font.Font("font/font.ttf", 36)
	
	# ÿ30�뷢��һ��������
	bullet_supply  = supply.Bullet_Supply(bg_size)
	bomb_supply  = supply.Bomb_Supply(bg_size)
	SUPPLY_TIME = USEREVENT
	pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
	
	#����ҷ��޵ж�ʱ��
	INVINVIBLE_TIME = USEREVENT + 2
	
	# �����ӵ���ʱ��
	DOUBLE_BULLET_TIME = USEREVENT + 1
	is_double_supply  = False
	#���ɳ����ӵ�
	bullet2 = []
	bullet2_index = 0
	BULLET2_NUM = 8
	for i in range(BULLET2_NUM // 2):
		bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
		bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
	
	#������������
	life_image = pygame.image.load("images/life.png").convert_alpha()
	life_rect = life_image.get_rect()
	life_num = 3
	
	# ����ȫ��ը��
	bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_font = pygame.font.Font('font/font.ttf', 48)
	bomb_num = 3
	
	#��������ֵ
	e1_destroy_index = 0
	e2_destroy_index = 0
	e3_destroy_index = 0
	me_destory_index = 0
	
	# ������ͣ��ť
	paused = False
	pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
	pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
	resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
	resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
	pause_rect = pause_nor_image.get_rect()
	pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
	pause_image = pause_nor_image
	
	# �����ظ����ļ�
	recorded = False
	
	# ������Ϸ��������
	gameover_font = pygame.font.Font("font/font.TTF", 48)
	again_image = pygame.image.load("images/again.png").convert_alpha()
	again_rect = again_image.get_rect()
	gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
	gameover_rect = gameover_image.get_rect()
	
	
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and pause_rect.collidepoint(event.pos):
					paused = not paused
					if paused:
						pygame.time.set_timer(SUPPLY_TIME, 0)
						pygame.mixer.music.pause()
						pygame.mixer.pause()
					else:
						pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()
			elif event.type == MOUSEMOTION:
				if pause_rect.collidepoint(event.pos):
					if paused:
						pause_image = resume_pressed_image
					else:
						pause_image = pause_pressed_image
				else:
					if paused:
						pause_image = resume_nor_image
					else:
						pause_image = pause_nor_image
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
				if choice([True, False]):
					bomb_supply.reset()
				else:
					bullet_supply.reset()
			elif event.type == DOUBLE_BULLET_TIME:
				is_double_supply = False
				pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
			elif event.type == INVINVIBLE_TIME:
				me.invincible = False
				pygame.time.set_timer(INVINVIBLE_TIME, 0)
				
		# ������Ļ����
		screen.blit(background, (0, 0))
		
		# �����Ѷ�ϵ��
		if level == level_instance.level_base and score > level_instance.score_base:
			upgrade_sound.play()
			level_instance.add_level()
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 2)
			add_big_enemies(big_enemies, enemies, 1)
			for e1 in small_enemies:
				e1.speed += 1
			for e2 in mid_enemies:
				if (level % 2) == 0:
					e2.speed += 1
			for e3 in big_enemies:
				if (level % 3) == 0:
					e3.speed += 1
			level += 1

		
		if life_num and not paused:
			#����û����̲���
			key_pressed = pygame.key.get_pressed()
			
			if key_pressed[K_w] or key_pressed[K_UP]:
				me.moveUp()
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				me.moveDown()
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				me.moveLeft()
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				me.moveRight()
			
			# ����ȫ��ը������
			if bomb_supply.active:
				bomb_supply.move()
				screen.blit(bomb_supply.image, bomb_supply.rect)
				if pygame.sprite.collide_mask(bomb_supply, me):
					get_bomb_sound.play()
					if bomb_num < 3:
						bomb_num += 1
					bomb_supply.active  = False
			# ���Ƴ����ӵ�����
			if bullet_supply.active:
				bullet_supply.move()
				screen.blit(bullet_supply.image, bullet_supply.rect)
				if pygame.sprite.collide_mask(bullet_supply, me):
					get_bullet_sound.play()
					pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
					bullet_supply.active  = False
					is_double_supply = True
			
			# �����ӵ�
			if not(delay % 10 ):
				if is_double_supply:
					bullets = bullet2
					bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
					bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
					bullet2_index = (bullet2_index + 2) % BULLET2_NUM
				else:
					bullets = bullet1
					bullets[bullet1_index].reset(me.rect.midtop)
					bullet1_index = (bullet1_index + 1) % BULLET1_NUM
				
			# ����ӵ��Ƿ���ел�
			for b in bullets:
				if b.active:
					b.move()
					screen.blit(b.image, b.rect)
					enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
					if enemy_hit:
						b.active = False
						for e in enemy_hit:
							if e in small_enemies:
								e.active = False
							else:
								e.energy -= 1
								e.hit = True
								if e.energy == 0:
									e.active = False
			
			
			
			#���ƴ��ͻ�
			for each in big_enemies:
				if each.active:
					each.move()
					#���ƻ�����Ч
					if each.hit:
						screen.blit(each.image_hit,each.rect)
						each.hit = False
					else:
						if switch_image:
							screen.blit(each.image1, each.rect)
						else:
							screen.blit(each.image2, each.rect)
					# ����Ѫ��
					pygame.draw.line(screen, BLACK,\
							(each.rect.left, each.rect.top - 5),\
							(each.rect.right, each.rect.top - 5),\
							2)
					# ����������20%��ʾ��ɫ�� ������ʾ��ɫ
					energy_remain = each.energy / enemy.BigEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color,\
							(each.rect.left, each.rect.top - 5),\
							(each.rect.left + each.rect.width * energy_remain, \
							each.rect.top -5),\
							2)
					
					#�������֣�������Ч
					if each.rect.bottom == -50:
						enemy3_fly_sound.play(-1)
				else:
					#����
					if not(delay % 3):
						if e3_destroy_index == 0:
							enemy3_down_sound.play()
						screen.blit(each.destroy_images[e3_destroy_index], each.rect)
						e3_destroy_index = (e3_destroy_index + 1) % 6
						if e3_destroy_index == 0:
							score += 6000
							enemy3_fly_sound.stop()
							each.reset()
						
			#�������ͷɻ�
			for each in mid_enemies:
				if each.active:
					each.move()
					#���ƻ�����Ч
					if each.hit:
						screen.blit(each.image_hit,each.rect)
						each.hit = False
					else:
						screen.blit(each.image, each.rect)
					# ����Ѫ��
					pygame.draw.line(screen, BLACK,\
							(each.rect.left, each.rect.top - 5),\
							(each.rect.right, each.rect.top - 5),\
							2)
					# ����������20%��ʾ��ɫ�� ������ʾ��ɫ
					energy_remain = each.energy / enemy.MidEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color,\
							(each.rect.left, each.rect.top - 5),\
							(each.rect.left + each.rect.width * energy_remain, \
							each.rect.top -5),\
							2)
				else:
					#����
					if not(delay % 3):
						if e2_destroy_index == 0:
							enemy2_down_sound.play()
						screen.blit(each.destroy_images[e2_destroy_index], each.rect)
						e2_destroy_index = (e2_destroy_index + 1) % 4
						if e2_destroy_index == 0:
							score += 2000
							each.reset()
							
			# ����С�ͷɻ�
			for each in small_enemies:
				if each.active:
					each.move()
					screen.blit(each.image, each.rect)
				else:
					#����
					if not(delay % 3):
						if e1_destroy_index == 0:
							enemy1_down_sound.play()
						screen.blit(each.destroy_images[e1_destroy_index], each.rect)
						e1_destroy_index = (e1_destroy_index + 1) % 4
						if e1_destroy_index == 0:
							score += 1000
							each.reset()
			
			#���ײ���¼�
			enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
			if enemies_down and not me.invincible:
				me.active = False
				for each in enemies_down:
					each.active = False
					
			
			#�����ҷ��ɻ� �������л�
			if me.active:
				if switch_image:
					screen.blit(me.image1, me.rect)
				else:
					screen.blit(me.image2, me.rect)
			else:
				me_down_sound.play()
				if not(delay % 3):
					screen.blit(me.destroy_images[me_destory_index], me.rect)
					me_destory_index = (me_destory_index + 1) % 4
					if me_destory_index == 0:
						life_num -= 1
						me.reset()
						pygame.time.set_timer(INVINVIBLE_TIME, 3 * 1000)
			
			# ����ը��
			bomb_text = bomb_font.render("�� %d" % bomb_num, True, WHITE)
			text_rect = bomb_text.get_rect()
			screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
			screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))
			
			# ����ʣ����������
			if life_num:
				for i in range(life_num):
					screen.blit(life_image, \
							(width-10-(i+1)*life_rect.width, \
							height-10- life_rect.height))
		#������Ϸ��������
		elif life_num == 0:
			pygame.mixer.music.stop()
			pygame.mixer.stop()
			pygame.time.set_timer(SUPPLY_TIME, 0)
			
			if not recorded:
				f = open("record.txt", 'r+')
				
				record_score = int(f.read())
				if score > record_score:
					record_score = score
					f.truncate()
					f.write(str(score))
				f.close()
				recorded = True
		
			# ���ƽ�������
			record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
			screen.blit(record_score_text, (50, 50))
			gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
			gameover_text1_rect = gameover_text1.get_rect()
			gameover_text1_rect.left, gameover_text1_rect.top = \
						(width - gameover_text1_rect.width) // 2, height // 3
			screen.blit(gameover_text1, gameover_text1_rect)
			
			gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
			gameover_text2_rect = gameover_text2.get_rect()
			gameover_text2_rect.left, gameover_text2_rect.top = \
									(width - gameover_text2_rect.width) // 2, \
									gameover_text1_rect.bottom + 10
			screen.blit(gameover_text2, gameover_text2_rect)

			again_rect.left, again_rect.top = \
								(width - again_rect.width) // 2, \
								gameover_text2_rect.bottom + 50
			screen.blit(again_image, again_rect)

			gameover_rect.left, gameover_rect.top = \
								(width - again_rect.width) // 2, \
								again_rect.bottom + 10
			screen.blit(gameover_image, gameover_rect)

			# ����û���������
			# ����û�����������
			if pygame.mouse.get_pressed()[0]:
				# ��ȡ�������
				pos = pygame.mouse.get_pos()
				# ����û���������¿�ʼ��
				if again_rect.left < pos[0] < again_rect.right and \
					again_rect.top < pos[1] < again_rect.bottom:
					# ����main���������¿�ʼ��Ϸ
					main()
				# ����û������������Ϸ��            
				elif gameover_rect.left < pos[0] < gameover_rect.right and \
					gameover_rect.top < pos[1] < gameover_rect.bottom:
					# �˳���Ϸ
					pygame.quit()
					sys.exit()    
					
		# ������ͣ��ť
		screen.blit(pause_image, pause_rect)
		
		# ���Ƶ÷�
		score_text = score_font.render("Score: %d" % score, True, WHITE)
		screen.blit(score_text, (10, 5))
		
		#�л�ͼƬ
		if not (delay % 5):
			switch_image =  not switch_image
		delay -= 1
		if not delay:
			delay = 100
		pygame.display.flip()
		clock.tick(60)
	
	
if __name__ == "__main__":
	try:
		main()
	except:
		pass

		
	
