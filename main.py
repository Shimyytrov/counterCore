import pygame
import sys
import random

#========== configuration ==========#
pygame.init()
fps = 50    # fps
fpsClock = pygame.time.Clock() # clock
screenInfo = pygame.display.Info() # get screen info
width, height = screenInfo.current_w, screenInfo.current_h    # get screen (width, height)
screen = pygame.display.set_mode((width, height))   # full screen
# load fonts
font = pygame.font.Font('./assets/fonts/courier.ttf', 48)
fontBig = pygame.font.Font('./assets/fonts/mindustry.ttf', 72)
fontMindustry = pygame.font.Font('./assets/fonts/mindustry.ttf', 36)
event = pygame.event.get()
 
# load sprites
core = pygame.image.load('./assets/sprites/core.png').convert_alpha()
core = pygame.transform.scale(core, (256, 256))
coreRect = core.get_rect(center = (width/2, height/2))
coreStage1 = pygame.image.load('./assets/sprites/coreDeepRed.png').convert_alpha()
coreStage1 = pygame.transform.scale(coreStage1, (256, 256))
coreStage1Rect = coreStage1.get_rect(center = (width/2, height/2))
coreStage2 = pygame.image.load('./assets/sprites/coreRed.png').convert_alpha()
coreStage2 = pygame.transform.scale(coreStage2, (256, 256))
coreStage2Rect = coreStage2.get_rect(center = (width/2, height/2))
coreStage3 = pygame.image.load('./assets/sprites/coreBrightRed.png').convert_alpha()
coreStage3 = pygame.transform.scale(coreStage3, (256, 256))
coreStage3Rect = coreStage3.get_rect(center = (width/2, height/2))
coreStage4 = pygame.image.load('./assets/sprites/coreXtremeRed.png').convert_alpha()
coreStage4 = pygame.transform.scale(coreStage4, (256, 256))
coreStage4Rect = coreStage4.get_rect(center = (width/2, height/2))
waterBucket = pygame.image.load('./assets/sprites/waterBucket.png').convert_alpha()
waterBucket = pygame.transform.scale(waterBucket, (192, 192))
waterBucketRect = waterBucket.get_rect(center = (width-width/16, height/8))
cryofluid = pygame.image.load('./assets/sprites/cryofluid.png').convert_alpha()
cryofluid = pygame.transform.scale(cryofluid, (192, 192))
cryofluidRect = cryofluid.get_rect(center = (width-width/16, (height/8)*3))

#load sounds
largeExplosion = pygame.mixer.Sound('./assets/sounds/meltdown.wav')
endBoom = pygame.mixer.Sound('./assets/sounds/orchestraBoom.wav')
def play_track(file, loop, fade_ms):    # play track function
    pygame.mixer.music.load(f'./assets/music/{file}.ogg')
    pygame.mixer.music.play(loop, fade_ms)

# variables
mouse_pos = (0, 0)
tick = 0
temperature = 0.00
speed = 0
powerLevel = 1
started = False
score = 0
ending = None

# Cooldowns 
bucketCooldown = False
bucketCooldownEnd = -1
cryofluidCooldown = False
cryofluidCooldownEnd = -1

#========== Event Sector ==========#
nextEventPlanned = False
nextEvent = -1
eventMsg = "Error Event"

def pwrLvlUp():
    global powerLevel
    global eventMsg
    eventMsg = "Your power level has been increased!"
    powerLevel += random.randint(1,5)

def pwrLvlDown():
    global powerLevel
    global eventMsg
    eventMsg = "Your power level has been decreased!"
    powerLevel -= random.randint(1,5)

events = [
    pwrLvlUp,   # Power Level Go Up
    pwrLvlDown  # Power Level Go Down
]

while True:
    screen.fill((16, 16, 16))
    coreStage1.set_alpha(temperature/4)
    coreStage2.set_alpha((temperature-1024)/4)
    coreStage3.set_alpha((temperature-2048)/4)
    coreStage4.set_alpha((temperature-3072)/4)
    
    
    screen.blit(core, coreRect)
    screen.blit(coreStage1, coreStage1Rect)
    screen.blit(coreStage2, coreStage2Rect)
    screen.blit(coreStage3, coreStage3Rect)
    screen.blit(coreStage4, coreStage4Rect)
    
    if not started:
        msgStart = font.render('Press Space to Start', True, (255,255,255)) # Press to Start
        msgStartRect = msgStart.get_rect(center = (width/2, height/1.3))
        screen.blit(msgStart, msgStartRect)
        title = fontBig.render('Counter Core', True, (255,255,255)) # Game Title
        titleRect = title.get_rect(center = (width/2, height/3.6))
        screen.blit(title, titleRect)

    if started:
        toolBarBoarder = pygame.draw.rect(screen, (211,211,211),(width-width/8,0, 4, height))
        screen.blit(waterBucket,waterBucketRect)
        screen.blit(cryofluid,cryofluidRect)

        if waterBucketRect.collidepoint(pygame.mouse.get_pos()):
            if waterBucketRect.collidepoint(mouse_pos) and not bucketCooldown:
                temperature -= 25
                mouse_pos = (0, 0)
                bucketCooldown = True
                bucketCooldownEnd = tick + 50*20

        if cryofluidRect.collidepoint(pygame.mouse.get_pos()):
            if cryofluidRect.collidepoint(mouse_pos) and not cryofluidCooldown:
                temperature -= 75
                mouse_pos = (0, 0)
                cryofluidCooldown = True
                cryofluidCooldownEnd = tick + 50*60
            

        tick += 1
        if tick % 1 == 0: # per tick event
            temperature += speed
        if tick % 50 == 0: # per second event
            score += (powerLevel*15 + temperature/100)
            speed = (
                powerLevel/100
            )

        if tick % 500 == 0: # per minute event
            powerLevel += tick/500

        if not nextEventPlanned:
            nextEvent = tick + random.randint(50*30, 50*120)
            nextEventPlanned = True

        if nextEvent <= tick <= (nextEvent+250): # Show Event Alert
            eventAlert = font.render(eventMsg, True, (255, 255, 255))
            eventAlertRect = eventAlert.get_rect(center = (width/2, height/1.3))
            screen.blit(eventAlert, eventAlertRect)

        if tick == nextEvent:
            print("Hello Kasuga!", tick)
            random.choice(events)()
            
        if tick >= nextEvent+250:
            nextEventPlanned = False

        if bucketCooldown:
            waterBucket.set_alpha(128)
        if tick == bucketCooldownEnd:
            waterBucket.set_alpha(256)
            bucketCooldown = False
        if cryofluidCooldown:
            cryofluid.set_alpha(128)
        if tick == cryofluidCooldownEnd:
            cryofluid.set_alpha(256)
            cryofluidCooldown = False

        text = font.render((str("%.2f" % temperature)+"°C"), True, (255, 255, 255))
        textRect = text.get_rect(center = (width/2, height/2.8))
        curScore = font.render(str("%.0f" % score), True, (255, 255, 255))
        curScoreRect = curScore.get_rect(center = (width/2, height/16))
        screen.blit(text, textRect)
        screen.blit(curScore, curScoreRect)

    if temperature >= 5120:
        ending = "meltdown"
        break


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT: # quit
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not started:
                play_track('theFacility', -1, 0)
            started = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            temperature = 100304103
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

    #----- loop repeat
    pygame.display.flip()   # update frame
    fpsClock.tick(fps)


# MELTDOWN EVENT
if ending == "meltdown":
    tick = 0
    pygame.mixer.music.stop()
    largeExplosion.play()
    while True:
        tick += 1

        if tick == 300:
            play_track('gameOver', 0, 0)
        if 0 <= tick <= 1:
            screen.fill((255,255,255))
        elif 1 < tick < 5:
            screen.fill((0,0,0))
        elif 5 <= tick < 8:
            screen.fill((255,0,0))
        elif 8 <= tick < 12:
            screen.fill((0,0,0))
        elif 12 <= tick < 15:
            screen.fill((255,255,0))
        elif 15 <= tick < 100:
            screen.fill((0,0,0))

        elif tick == 100:
            endBoom.play()
            
        elif 100 <= tick <= 200:
            screen.fill((0,0,0))
            gameOver = fontBig.render("GAME OVER", True, (255,0,0))
            gameOverRect = gameOver.get_rect(center = (width/2,height/2.8))
            screen.blit(gameOver,gameOverRect)
            finalScore = font.render("Your score: "+ str("%.0f" % score), True,(255,255,255))
            finalScoreRect = finalScore.get_rect(center = (width/2,height/1.8))
            screen.blit(finalScore,finalScoreRect)

        elif 300 <= tick:
            screen.fill((0,0,0))
            if 300 <= tick < 433:
                text = fontMindustry.render("Counter Core", True, (255,255,255))
                textRect = text.get_rect(center = (width/2,height/2))
            if 433 <= tick < 566:
                text = fontMindustry.render("A Short Game by Alexander and Chrono", True, (255,255,255))
                textRect = text.get_rect(center = (width/2,height/2))
            if 566 <= tick < 700:
                text = fontMindustry.render("Music 'The Facility' by Alexander", True, (255,255,255))
                textRect = text.get_rect(center = (width/2,height/2))
            if 700 <= tick < 833:
                text = fontMindustry.render("Music 'Game Over' by Alexander", True, (255,255,255))
                textRect = text.get_rect(center = (width/2,height/2))
            if tick >= 833:
                text = fontMindustry.render('Thanks for Playing!', True, (255,255,255))
                textRect = text.get_rect(center = (width/2,height/2))
            
            screen.blit(text, textRect)


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT: # quit
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                started = True

        #----- loop repeat
        pygame.display.flip()   # update frame
        fpsClock.tick(fps)