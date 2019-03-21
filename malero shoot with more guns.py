import pygame
import random

class Malero:
    def __init__(self):
        global multiplier
        self.x = int(42 * multiplier)
        self.y = int(193 * multiplier)
        self.changeX = 0
        self.changeY = 0
        self.width = int(12 * multiplier)
        self.height = int(16 * multiplier)
        self.surface = pygame.transform.scale(pygame.image.load("malero.png"), (self.width, self.height))
class Malery:
    def __init__(self):
        self.width = int(12 * multiplier)
        self.height = int(16 * multiplier)
        self.surface = pygame.transform.scale(pygame.image.load("malery.png"), (self.width, self.height))
        self.x = screenX
        self.y = random.randint(0, screenY - self.height)
        self.changeX = random.randint(-15, -1)
        self.changeY = random.randint(-15, 15)
class Bullet:
    def __init__(self):
        self.width = int(1 * multiplier)
        self.height = int(1 * multiplier)
        self.x = 0
        self.y = 0
        self.changeX = 0
        self.changeY = 0
class Ball:
    def __init__(self):
        global memeList
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = random.randint(0, 1)
        self.text = ""
        self.size = 0
        self.colour = ""
        self.surface = ()
        self.width = 0
        self.height = 0
class Gun:
    def __init__(self):
        self.type = "pistol"
        self.ammo = 6
        self.clip = 6

def changeGun():
    global gun
    gunList = ["pistol", "triGun", "omniDirectional"]
    gunI = 0
    for i in gunList:
        if gun.type == i:
            nextGun = gunI + 1
            break
        elif gun.type == "infiniGun":
            nextGun = 0
            break
        gunI += 1
    if nextGun >= len(gunList):
        nextGun = 0
    gun.type = gunList[nextGun]
    print(gun.type)

    if gun.type == "pistol":
        gun.ammo = 6
        gun.clip = 6
    elif gun.type == "triGun":
        gun.ammo = 0
        gun.clip = 300
    elif gun.type == "omniDirectional":
        gun.ammo = 0
        gun.clip = 8
    elif gun.type == "infiniGun":
        gun.ammo = -21
        gun.clip = -21
        ammoDebt = -21
    return gun
    
def makeBullet(x, y, changeY, changeX = 10):
    bullet = Bullet()
    bullet.x = x
    bullet.y = y
    bullet.changeX = changeX
    bullet.changeY = changeY
    return bullet        
def makeBall():
    ball = Ball()
    ball.text = memeList[random.randint(0,len(memeList)-1)]
    ball.colour = colourList[random.randint(0,len(colourList)-1)]
    ball.size = random.randint(6, 50)
    ball.surface = pygame.font.SysFont("comicsansms", ball.size).render(ball.text, True, ball.colour)
    ball.width = ball.surface.get_width()
    ball.height = ball.surface.get_height()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.x = screenX
    ball.y = random.randint(0, screenY - ball.height)
    ball.change_x = random.randrange(-10, -1)

    return ball        
def make_malero(randomSpawn = False):
    mar = Malero()
    if randomSpawn:
        mar.x = random.randint(0, screenX - mar.width)
        mar.y = random.randint(0, screenY - mar.height)
    return mar
def make_malery():
    mal = Malery()
    return mal
def collide(oneList, twoList, deleteTwoList = False, deleteOneList = True):
    collide =  False
    oneI = 0
    for one in oneList:
        twoI = 0
        for two in twoList:
            touchY = False
            touchX = False 
            for i in range(0, two.height):
                if two.y + i > one.y and two.y + i < one.y + one.height:
                    touchY = True
                    break
            for i in range(0, two.width):
                if two.x + i > one.x and two.x + i < one.x + one.width:
                    touchX = True
                    break
            twoI += 1
            if deleteOneList and touchX and touchY:
                oneList.remove(one)
                collide = True
                if deleteTwoList:
                    twoList.remove(two)
                break
        oneI += 1
        
    if collide:
        return True
    else:
        return False
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (254, 79, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRASS = (0, 168, 0)
BUSH = (128, 208, 16)
CYAN = (0, 255, 247)
BLUE = (1, 18, 254)
SKY = (92, 148, 252)
INDIGO = (255, 0, 255)
VIOLET = (116, 20, 120)
 
##screenX = GetSystemMetrics(0)
##screenY = GetSystemMetrics(1)
#256 x 240 (1)
#1440 x 1080 (4.5)
multiplier = 2
screenX = int(256 * multiplier)
screenY = int(240 * multiplier)
 
pygame.init()

# Set the height and width of the screen
size = [screenX, screenY]
##screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("malero")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

colourList = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, INDIGO, VIOLET]
with open("lines.txt") as f:
    memeList = f.read().split("\n")

marList = []
ballList = []
monList = []
bulList = []
monList.append(make_malery())
marList.append(make_malero())
play = True
shooting = False
triggerUp = True
reloading = False
changedGun = False
changingGun = False
global gun
gun = Gun()
scoreDebt = 0
global ammoDebt
ammoDebt = 0
score = 0
lives = 3
ticks = 0
tacks = 0
right = False
left = False
down = False
up = False
kageBunshinNoJutsu = False

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # Space bar! Spawn a new ball.
            if event.key == pygame.K_UP:
                up = True
            elif event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_LEFT:
                left = True
            elif event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_BACKSPACE:
                marList = []
                monList = []
                ballList = []
                score = 0
                lives = 3
                marList.append(make_malero())
            if event.key == pygame.K_SPACE:
                kageBunshinNoJutsu = True
            if event.key == pygame.K_z:
                shooting = True
            if event.key == pygame.K_x:
                reloading = True
            if event.key == pygame.K_c:
                if not changedGun:
                    changingGun = True
            if event.key == pygame.K_i:
                gun.type = "infiniGun"
            if event.key == pygame.K_p:
                play = not play
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            elif event.key == pygame.K_DOWN:
                down = False
            if event.key == pygame.K_LEFT:
                left = False
            elif event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_SPACE:
                kageBunshinNoJutsu = False
            if event.key == pygame.K_z:
                shooting = False
                triggerUp = True
            if event.key == pygame.K_c:
                changingGun = False
                changedGun = False
                
#main logic
    if play:
        if clock.get_fps() < 8:
            danger = RED
        else:
            danger = YELLOW

        if ticks >= 60 * 5:
            monList.append(make_malery())
            ticks = 0
        if tacks >= 60 * 1:
            ballList.append(makeBall())
            tacks = 0
            
        if kageBunshinNoJutsu and lives > 0:
            marList.append(make_malero(True))
            lives += -1
        else:
            if len(marList) > 1:
                for mar in marList:
                    for mara in marList:
                        if mar != mara and mar.x == mara.x and mar.y == mara.y:
                            lives += 1
                            marList.remove(mar)
                            break

        if changingGun and not changedGun:
            ammoDebt = 0
            gun = changeGun()
            changedGun = True
            
        if reloading and not shooting:
            if gun.type == "omniDirectional" and gun.ammo < gun.clip:
                if ammoDebt == 0:
                    ammoDebt = 4
                if ammoDebt > 0:
                    gun.ammo += 4
                    ammoDebt += -4
                if gun.ammo == 8:
                    reloading = False
                reloading = False
            elif gun.type == "triGun" and gun.ammo < gun.clip:
                if ammoDebt == 0:
                    ammoDebt = gun.clip - gun.ammo
                elif ammoDebt > 0:
                    gun.ammo += 3
                    ammoDebt += -3
                if gun.ammo == 300:
                    reloading = False
            elif gun.type == "infiniGun":
                ammoDebt = -21
                reloading = False
            else:
                gun.ammo = gun.clip
                reloading = False

        for mar in marList:
            if up:
                mar.changeY = -5 * multiplier
            elif down:
                mar.changeY = 5 * multiplier
            else:
                mar.changeY = 0

            if right:
                mar.changeX = 5 * multiplier
            elif left:
                mar.changeX = -5 * multiplier
            else:
                mar.changeX = 0

            mar.y += mar.changeY
            mar.x += mar.changeX

            if mar.x < 0:
                mar.x = 0
            if mar.x > screenX - mar.width:
                mar.x = screenX - mar.width
            if mar.y < 0:
                mar.y = 0
            if mar.y > screenY - mar.height:
                mar.y = screenY - mar.height

        if shooting and not reloading and gun.ammo > 0:
            if gun.type == "pistol":
                if triggerUp:
                    for mar in marList:
                        bulList.append(makeBullet(mar.x, mar.y, 0))
                        gun.ammo += -1
                    triggerUp = False
            elif gun.type == "triGun":
                for mar in marList:
                    bulList.append(makeBullet(mar.x, mar.y, -2))
                    bulList.append(makeBullet(mar.x, mar.y, 0))
                    bulList.append(makeBullet(mar.x, mar.y, 2))
                    gun.ammo += -3
            elif gun.type == "omniDirectional":
                for mar in marList:
                    if triggerUp:
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, -10, 0))
                            gun.ammo += -1
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, -10, -10))
                            gun.ammo += -1
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, 0, -10))
                            gun.ammo += -1
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, 10, -10))
                            gun.ammo += -1
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, 10, 0))
                            gun.ammo += -1
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, 10, 10))
                            gun.ammo += -1
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, 0, 10))
                            gun.ammo += -1
                        if gun.ammo > 0:
                            bulList.append(makeBullet(mar.x, mar.y, -10, 10))
                            gun.ammo += -1
                        triggerUp = False
        elif gun.type == "infiniGun":
            if shooting:
                for mar in marList:
                    bulList.append(makeBullet(mar.x, mar.y, 0, 1))
            gun.ammo = - 21
        elif gun.ammo < 0:
            gun.ammo = 0

        for bul in bulList:
            bul.x += bul.changeX
            bul.y += bul.changeY
            if bul.x > screenX:
                bulList.remove(bul)
            elif bul.y > screenY:
                bulList.remove(bul)
            elif bul.y < 0:
                bulList.remove(bul)

        for mon in monList:
            mon.y += mon.changeY
            mon.x += mon.changeX
            if mon.x < 0 - mon.width:
                monList.remove(mon)
            if mon.y < 0:
                mon.changeY = - mon.changeY
            if mon.y > screenY - mon.height:
                mon.changeY = - mon.changeY

        for ball in ballList:
            # Move the ball's center
            ball.change_y = -ball.change_y
            ball.x += ball.change_x
            ball.y += ball.change_y
            if ball.x < 0 - ball.width:
                ballList.remove(ball)

        if collide(ballList, bulList):
            scoreDebt = 100

        collide(marList, ballList)

        collide(monList, bulList, True, True)
        
        if collide(monList, marList):
            scoreDebt = 1
            lives += 1

        if scoreDebt > 0:
            scoreDebt += -1
            score += 1

        if gun.ammo <= 0:
            ammoText = "ammo: 0 Press 'x' to reload"
        else:
            ammoText = "ammo: " + str(gun.ammo)
        if ammoDebt > 0:
            ammoText = "ammo: " + str(gun.ammo) + " + " + str(ammoDebt)
        elif ammoDebt == -21:
            ammoText = "ammo: ∞"
        if scoreDebt > 0:
            scoreText = "score: " + str(score) + " + " + str(scoreDebt)
        else:
            scoreText = "score: " + str(score)

    if lives <= 0 and len(marList) < 1:
        livesText = "YOU LOSE"
        lossCol = RED
        lossSize = 50
    elif not play:
        livesText = "PAUSE"
        lossSize = 50
    else:
        livesText = "lives: " + str(lives)
        lossCol = YELLOW
        lossSize = 12

    fpsText = "fps: " + str(clock.get_fps())
    gunTypeText = "gun type: " + str(gun.type)

    # --- Drawing
    # Set the screen background
    screen.fill(SKY)

    # Draw the balls
    for mar in marList:
        screen.blit(mar.surface, (mar.x, mar.y))
    for mon in monList:
        screen.blit(mon.surface, (mon.x, mon.y))
    for ball in ballList:
        screen.blit(ball.surface, [ball.x, ball.y])
    for bul in bulList:
        pygame.draw.rect(screen, WHITE, [bul.x, bul.y, bul.width, bul.height])
    if not play:
        s = pygame.Surface((screenX, screenY))
        s.fill((0, 0, 0))
        s.set_alpha(128)
        screen.blit(s, (0,0))

#counters
    
    fpsSurface = pygame.font.SysFont("couriernew", 12, True).render(fpsText, True, danger, BLACK)
    scoreSurface = pygame.font.SysFont("couriernew", 12, True).render(scoreText, True, YELLOW, BLACK)
    livesSurface = pygame.font.SysFont("couriernew", lossSize, True).render(livesText, True, lossCol, BLACK)
    ammoSurface = pygame.font.SysFont("couriernew", 12, True).render(ammoText, True, YELLOW, BLACK)
    gunTypeSurface = pygame.font.SysFont("couriernew", 12, True).render(gunTypeText, True, YELLOW, BLACK)
    screen.blit(scoreSurface, [0, 13])
    screen.blit(fpsSurface, [0, 0])
    screen.blit(ammoSurface, [0, 39])
    screen.blit(gunTypeSurface, [0, 52])
    screen.blit(livesSurface, [0, 26])

    # --- Wrap-up
    # Limit to 60 frames per second
    ticks += 1
    tacks += 1
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close everything down
pygame.quit()

