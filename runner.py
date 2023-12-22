import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
  def __init__(self) -> None:
    super().__init__()

    player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
    player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
    self.player_walk = [player_walk_1, player_walk_2]
    self.player_index = 0
    self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

    self.image = self.player_walk[self.player_index]
    self.rect = self.image.get_rect(midbottom = (80, 300))
    self.gravity = 0

    self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")

  # allows jumping only when the space bar is pressed and when the player is on the ground
  def player_input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
      self.gravity = -20
      self.jump_sound.play()

  # apply gravity to falls and prevent player from falling through
  def apply_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    if self.rect.bottom >= 300:
      self.rect.bottom = 300

  # animate the player
  def animation_state(self):
    if self.rect.bottom < 300:
      self.image = self.player_jump
    else:
      self.player_index += 0.1
      if (self.player_index >= len(self.player_walk)):
        self.player_index = 0
      self.image = self.player_walk[int(self.player_index)]

  # update the player every frame
  def update(self):
    self.player_input()
    self.apply_gravity()
    self.animation_state()

class Obstacle(pygame.sprite.Sprite):
  def __init__(self, type) -> None:
    super().__init__()

    if type == "fly":
      fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
      fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
      self.frames = [fly_frame_1, fly_frame_2]
      y_pos = 210
    else:
      snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
      snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
      self.frames = [snail_frame_1, snail_frame_2]
      y_pos = 300

    self.animation_index = 0
    self.image = self.frames[self.animation_index]
    self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

  # animate the obstacles
  def animation_state(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames):
      self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]

  # update the obstacles by moving them to the left and remove them when off the screen
  def update(self):
    self.animation_state()
    self.rect.x -= 6
    self.destroy()

  # function to destroy the obstacle
  def destroy(self):
    if self.rect.x <= -100:
      self.kill()

# displays the score on the screen
def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_surface = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
  score_rectangle = score_surface.get_rect(center = (400, 50))
  screen.blit(score_surface, score_rectangle)
  return current_time

# check the collision between the player and any sprites
def collision_sprite():
  if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
    obstacle_group.empty()
    return False
  else:
    return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

# plays the background music in loops
bgm = pygame.mixer.Sound("audio/music.wav")
bgm.set_volume(0.7)
bgm.play(loops = -1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# displaying the intro screen
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rectangle = player_stand.get_rect(center = (400, 200))

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rectangle = game_name.get_rect(center = (400, 80))

game_message = test_font.render("Press space to run", False, (111, 196, 169))
game_message_rectangle = game_message.get_rect(center = (400, 320))

# set up the obstacle timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if game_active:
      if event.type == obstacle_timer:
        obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        start_time = int(pygame.time.get_ticks() / 1000)

  if game_active:
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    score = display_score()

    player.draw(screen)
    player.update()

    obstacle_group.draw(screen)
    obstacle_group.update()

    game_active = collision_sprite()

  else:

    # displays the game over screen
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rectangle)

    score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
    score_message_rectangle = score_message.get_rect(center = (400, 330))
    screen.blit(game_name, game_name_rectangle)

    # displays either the score or the instructions
    if score == 0:
      screen.blit(game_message, game_message_rectangle)
    else:
      screen.blit(score_message, score_message_rectangle)

  # update the game and the clock
  pygame.display.update()
  clock.tick(60)