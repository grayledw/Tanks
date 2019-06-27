import pygame as pg
import pygame,random,math,time,sys

hillPointList = [(1280, 500), (1280, 720), (0, 720), (0, 500)]
hillPeakPointList = []  # new list of peaks
width = 1280
height = 720
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Tank Battle")
screen.fill((0, 0, 0))
greenPowerActivated = False
redPowerActivated = False
redHasPower = True
greenHasPower = True
greenTurn = True
redTurn = False






class Board:
    def __init__(self):
        pass

    def generateHills(self, terrain_diversity):
        global hillPointList, hillPeakPointList
        x = 0
        i = 0
        point = 0
        while i < 1280:
            hillPointList.append((x, random.randrange(450, 550)))
            x = x + 80
            i = i + terrain_diversity
        done_shift = False

        while point < len(hillPointList):
            if not done_shift:
                point = point + 4
                done_shift = True
            hillPeakPointList.append(hillPointList[point])
            point = point + 1
        #print(hillPeakPointList)

    def draw_hills(self):
        pg.draw.polygon(screen, (135, 206, 250), hillPointList)


class Tank:
    def __init__(self):
        self.green_tank = None
        self.red_tank = None
        self.redTankDestroyed = False
        self.greenTankDestroyed = False
        self.x_direction = 2
        self.y_direction = 2
        self.green_x = 100
        self.green_y = 150
        self.red_x = 1130
        self.red_y = 150
        self.green_collision = False
        self.red_collision = False

        self.original_green = pygame.image.load("Green_Tank_45x20.png")
        self.original_red = pygame.image.load("Red_Tank_45x20.png")

        self.green_tank = self.original_green
        screen.blit(self.green_tank, (self.green_x, self.green_y))

        self.red_tank = self.original_red
        screen.blit(self.red_tank, (self.red_x, self.red_y))

        self.green_rect = [self.green_x, self.green_y, 45, 20]
        self.red_rect = [self.red_x, self.red_y, 45, 20]
    def findAngleGreen(self,pos):
        sX = self.green_x
        sY = self.green_y
        try:
            angle = math.atan((sY - pos[1]) / (sX - pos[0]))
        except:
            angle = math.pi / 2

        if pos[1] < sY and pos[0] > sX:
            angle = abs(angle)
        elif pos[1] < sY and pos[0] < sX:
            angle = math.pi - angle
        elif pos[1] > sY and pos[0] < sX:
            angle = math.pi + abs(angle)
        elif pos[1] > sY and pos[0] > sX:
            angle = (math.pi * 2) - angle

        return angle
    def findAngleRed(self,pos):
        sX = self.red_x
        sY = self.red_y

        try:
            angle = math.atan((sY - pos[1]) / (sX - pos[0]))
        except:
            angle = math.pi / 2

        if pos[1] < sY and pos[0] > sX:
            angle = abs(angle)
        elif pos[1] < sY and pos[0] < sX:
            angle = math.pi - angle
        elif pos[1] > sY and pos[0] < sX:
            angle = math.pi + abs(angle)
        elif pos[1] > sY and pos[0] > sX:
            angle = (math.pi * 2) - angle

        return angle



    def spawnGreenTank(self):
        # green
        if not self.green_collision:
            # green tank spawn x = 100
            slope = ((hillPeakPointList[2])[1] - (hillPeakPointList[1])[1]) / ((hillPeakPointList[2])[0] -
                                                                               (hillPeakPointList[1])[0])
            y_value = slope * (100 - (hillPeakPointList[1])[0]) + (hillPeakPointList[1])[1]
            if self.green_y + 20 > y_value:
                #print("GREEN - y_value = %5d; self_y = %5d" % (y_value, self.green_y))
                self.green_collision = True
                # Rotate for an angle
                angle = math.atan(((hillPeakPointList[2])[1] - (hillPeakPointList[1])[1]) / ((hillPeakPointList[2])[0] -
                                                                                             (hillPeakPointList[1])[0]))
                angle *= 180 / math.pi
                #print("Spawn Angle: %d" % angle)
                pivot = pygame.math.Vector2(self.green_x, y_value)
                offset = pygame.math.Vector2(45/2, -10)
                self.green_tank, self.green_rect = self.rotate(self.original_green, angle, pivot, offset)
            else:
                self.dropGreenTank()

    def spawnRedTank(self):
        if not self.red_collision:
            # red tank spawn x = 1130
            slope = ((hillPeakPointList[15])[1] - (hillPeakPointList[14])[1]) / ((hillPeakPointList[15])[0] -
                                                                                 (hillPeakPointList[14])[0])
            y_value = slope * (1130 - (hillPeakPointList[15])[0]) + (hillPeakPointList[15])[1]

            if self.red_y + 20 > y_value:
                #print("RED - y_value = %5d; self_y = %5d" % (y_value, self.red_y))
                self.red_collision = True
                # Rotate for an angle
                angle = math.atan(((hillPeakPointList[15])[1] - (hillPeakPointList[14])[1]) /
                                  ((hillPeakPointList[15])[0] - (hillPeakPointList[14])[0]))
                angle *= 180 / math.pi
                pivot = pygame.math.Vector2(self.red_x, y_value)
                offset = pygame.math.Vector2(45/2, -10)
                self.red_tank, self.red_rect = self.rotate(self.red_tank, angle, pivot, offset)
            else:
                self.dropRedTank()

    def dropGreenTank(self):
        self.green_y += self.y_direction

    def dropRedTank(self):
        self.red_y += self.y_direction

    def drawGreenTank(self):
        if self.green_collision:
            screen.blit(self.green_tank, self.green_rect)
        else:
            screen.blit(self.green_tank, (self.green_x, self.green_y))

    def drawRedTank(self):
        if self.red_collision:
            screen.blit(self.red_tank, self.red_rect)
        else:
            screen.blit(self.red_tank, (self.red_x, self.red_y))

    def rotate(self, surface, angle, pivot, offset):
        """Rotate the surface around the pivot point.

        Args:
            surface (pygame.Surface): The surface that is to be rotated.
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        rotated_image = pg.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect  # Return the rotated image and shifted rect.

    def moveGreenTankLeft(self):
        index = 1
        for i in range(len(hillPeakPointList)):
            if hillPeakPointList[i][0] > self.green_x:
                index = i
                break
        left_point = hillPeakPointList[index - 1]
        right_point = hillPeakPointList[index]
        slope = (right_point[1] - left_point[1]) / (right_point[0] - left_point[0])

        angle = math.atan(slope)
        angle *= 180 / math.pi
        new_green_x = self.green_x - self.x_direction
        new_green_y = slope * (new_green_x - left_point[0]) + left_point[1]

        self.green_x = new_green_x
        self.green_y = new_green_y
        pivot = pygame.math.Vector2(self.green_x, self.green_y)
        offset = pygame.math.Vector2(45 / 2, -10)

        if self.green_x < 0:
            self.green_x = 0

        self.green_tank, self.green_rect = self.rotate(self.original_green, angle, pivot, offset)
        tankGreenPos = (self.green_x,self.green_y)
    def moveGreenTankRight(self):
        index = 1
        for i in range(len(hillPeakPointList)):
            if hillPeakPointList[i][0] > self.green_x:
                index = i
                break
        left_point = hillPeakPointList[index - 1]
        right_point = hillPeakPointList[index]
        slope = (right_point[1] - left_point[1]) / (right_point[0] - left_point[0])

        angle = math.atan(slope)
        angle *= 180 / math.pi
        new_green_x = self.green_x + self.x_direction
        new_green_y = slope*(new_green_x-left_point[0])+left_point[1]

        self.green_x = new_green_x
        self.green_y = new_green_y
        pivot = pygame.math.Vector2(self.green_x, self.green_y)
        offset = pygame.math.Vector2(45 / 2, -10)

        if self.green_x + 45 > 480:
            self.green_x = 445

        self.green_tank, self.green_rect = self.rotate(self.original_green, angle, pivot, offset)
        tankGreenPos = (self.green_x,self.green_y)
    def moveRedTankLeft(self):
        index = 1
        for i in range(len(hillPeakPointList)):
            if hillPeakPointList[i][0] > self.red_x:
                index = i
                break
        left_point = hillPeakPointList[index - 1]
        right_point = hillPeakPointList[index]
        slope = (right_point[1] - left_point[1]) / (right_point[0] - left_point[0])

        angle = math.atan(slope)
        angle *= 180 / math.pi
        new_red_x = self.red_x - self.x_direction
        new_red_y = slope * (new_red_x - left_point[0]) + left_point[1]

        self.red_x = new_red_x
        self.red_y = new_red_y
        pivot = pygame.math.Vector2(self.red_x, self.red_y)
        offset = pygame.math.Vector2(45 / 2, -10)

        if self.red_x < 720:
            self.red_x = 720
        tankRedPos = (self.red_x,self.red_y)
        self.red_tank, self.red_rect = self.rotate(self.original_red, angle, pivot, offset)

    def moveRedTankRight(self):
        index = 1
        for i in range(len(hillPeakPointList)):
            if hillPeakPointList[i][0] > self.red_x:
                index = i
                break
        left_point = hillPeakPointList[index - 1]
        right_point = hillPeakPointList[index]
        slope = (right_point[1] - left_point[1]) / (right_point[0] - left_point[0])

        angle = math.atan(slope)
        angle *= 180 / math.pi
        new_red_x = self.red_x + self.x_direction
        new_red_y = slope * (new_red_x - left_point[0]) + left_point[1]

        self.red_x = new_red_x
        self.red_y = new_red_y
        pivot = pygame.math.Vector2(self.red_x, self.red_y)
        offset = pygame.math.Vector2(45 / 2, -10)

        if self.red_x + 45 > 1280:
            self.red_x = 1240

        self.red_tank, self.red_rect = self.rotate(self.original_red, angle, pivot, offset)
        tankRedPos = (self.red_x,self.red_y)

class Bullet():
    def __init__(self,tankX,tankY,window, pow,angle,redTurn,color):
        self.tankX = tankX
        self.tankY = tankY
        self.window = window
        self.time = 0
        self.color = color
        self.power = pow
        self.angle = angle
        self.ballX = tankX
        self.ballY = tankY
        self.keepRunning = True
        self.notHit = True
        self.red_turn = redTurn


    def draw(self,window):
        self.bullet = pg.draw.circle(window,self.color, (self.ballX,self.ballY), 10)
        pg.display.flip()




    def bulletPath(self, startX , startY, power, ang, time):
        self.power = power
        self.time = time
        angle = ang


        velocityX = math.cos(angle) * power
        velocityY = math.sin(angle) * power
        #if self.red_turn:
        #    velocityY = velot



        distanceX = velocityX * self.time
        distanceY = (velocityY * self.time) + ((-3.9 * (self.time ** 2 )) / 2 )

        newX = round(distanceX + startX)
        newY = round(startY - distanceY)

        return (newX, newY)

    def move(self):

        if self.ballY < 720 - 10 and self.notHit:
            self.time += 0.15
            pos = self.bulletPath(self.tankX,self.tankY,self.power,self.angle,self.time)
            if self.ballX < 0:

                #self.ballX = 1270
                self.ballY = pos[1]

            if self.ballX >= 1280 - 10:

                self.ballX = 120 - 10
                self.ballY = pos[1]
            else:

                self.ballX = pos[0]
                self.ballY = pos[1]
            #if self.ballY < 0:
            #    self.ballY = 0
                ##print("bally: ",self.ballY)
            if self.ballY > 550:
                ##print("in")
                self.notHit = False


        else:
            self.keepRunning = False


    def update(self):
        if self.ballY < 720 and self.keepRunning:
            self.move()
            self.draw(self.window)
            pg.display.flip()
            time.sleep(0.005)
            ##print(self.ballX,self.ballY,self.tankX,self.tankY)




class Main:
    pg.init()
    powerIncrease = 20

    boardTest = Board()
    boardTest.generateHills(5)
    tankGame = Tank()
    bulletRed = None
    bulletGreen = None

    green_turn = True
    red_turn = False
    continue_moving_left = False
    continue_moving_right = False
    running = True
    bulletDraw = True
    bulletGreenPos = (0,0)




    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('GAME OVER', True, (255,0,0), (0,0,0))
    textRect = text.get_rect()
    textRect.center = (1280 // 2, 300)
    redActive = False
    greenActive = True


    while running:
        pos = pg.mouse.get_pos()
        tankRedPos = (tankGame.red_x,tankGame.red_y)
        tankGreenPos = (tankGame.green_x,tankGame.green_y)
        try:
            bulletGreenPos = (bulletGreen.ballX,bulletGreen.ballY)
        except:
            pass
        #print(tankRedPos)
        #print(tankGreenPos)
        #print(bulletGreenPos)
        for event in pg.event.get():
            # #print(event)
            if event.type == pg.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    continue_moving_left = True

                if event.key == pygame.K_RIGHT:
                    continue_moving_right = True

                if event.key == pygame.K_p:
                    if green_turn and greenHasPower:
                        print("Green Tank: Activated High-Velocity shot.")

                        powertext = font.render('Green Tank: Activated High-Velocity shot.', True, (150,255,0), (0,0,0))
                        powertextRect = powertext.get_rect()
                        powertextRect.center = (1280 // 2, 300)
                        screen.blit(powertext,powertextRect)
                        #time.sleep(2)
                        pg.display.update()

                        greenPowerActivated = True
                    elif red_turn and redHasPower:
                        print("Red Tank: Activated High-Velocity shot.")
                        redPowerActivated = True
                else:
                    #print("used")
                    pass
                if event.key == pygame.K_e:
                    green_turn = not green_turn
                    red_turn = not red_turn
            if event.type == pg.MOUSEBUTTONDOWN :
                greenAngle = tankGame.findAngleGreen(pos)
                redAngle = tankGame.findAngleRed(pos)


                ##print(angle)
                if green_turn:
                    if greenPowerActivated and greenHasPower:
                        bulletGreen = Bullet(tankGame.green_x,tankGame.green_y,screen,60 + powerIncrease,greenAngle,red_turn,(0,255,0))
                        greenHasPower = False

                    else:
                        bulletGreen = Bullet(tankGame.green_x,tankGame.green_y,screen,60,greenAngle,red_turn,(0,255,0))
                        redActive = True
                        greenActive = True


                else:
                    if redPowerActivated and redHasPower:
                        bulletRed = Bullet(tankGame.red_x,tankGame.red_y,screen,60 + powerIncrease,redAngle,red_turn,(255,0,0))
                        redHasPower = False
                    else:

                        bulletRed = Bullet(tankGame.red_x,tankGame.red_y,screen,60,redAngle,red_turn,(255,0,0))
                        greenActive = True
                        redActive = False
                    #math.radians(180 - math.degrees(angle))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    continue_moving_left = False
                if event.key == pygame.K_RIGHT:
                    continue_moving_right = False

        if continue_moving_left:
            if green_turn:
                tankGame.moveGreenTankLeft()
            if red_turn:
                tankGame.moveRedTankLeft()
        if continue_moving_right:
            if green_turn:
                tankGame.moveGreenTankRight()
            if red_turn:
                tankGame.moveRedTankRight()

        screen.fill((0, 0, 0))


        if not tankGame.green_collision:
            tankGame.spawnGreenTank()
        if not tankGame.red_collision:
            tankGame.spawnRedTank()

        tankGame.drawGreenTank()
        tankGame.drawRedTank()
        boardTest.draw_hills()
        #tankGame.destroyRedTank()
        if bulletRed:
            bulletRed.update()

            if bulletRed.ballX > 1280 or bulletRed.ballX < 0:
                #print("out of screen x")
                bulletRed.ballY = 750
            index = 1
            for i in range(len(hillPeakPointList)):
                if hillPeakPointList[i][0] > bulletRed.ballX:
                    index = i
                    break
            left_point = hillPeakPointList[index - 1]
            right_point = hillPeakPointList[index]
            slope = (right_point[1] - left_point[1]) / (right_point[0] - left_point[0])
            yOnSlope = slope * (bulletRed.ballX - left_point[0]) + left_point[1]
            #print("yonslope:",yOnSlope)
            if bulletRed.ballY > yOnSlope:
                #print("below")
                bulletRed.ballY = 750

            if red_turn:
                green_tank_rect = tankGame.green_rect
                red_bullet_rect = bulletRed.bullet
                if green_tank_rect.colliderect(red_bullet_rect):
                    text = font.render('GAME OVER! Red Tank Wins!', True, (255,0,0), (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = (1280 // 2, 300)
                    screen.blit(text,textRect)
                    pg.display.update()

                    #print('red Bullet hit green Tank!!!')
                    time.sleep(3)
                    sys.exit()
#"===================================================================================================="
        if bulletGreen:
            bulletGreen.update()
            if bulletGreen.ballX > 1280 or bulletGreen.ballX < 0:
                #print("out of screen x")
                bulletGreen.ballY = 750
            index = 1
            for i in range(len(hillPeakPointList)):
                if hillPeakPointList[i][0] > bulletGreen.ballX:
                    index = i
                    break
            left_point = hillPeakPointList[index - 1]
            right_point = hillPeakPointList[index]
            slope = (right_point[1] - left_point[1]) / (right_point[0] - left_point[0])
            yOnSlope = slope * (bulletGreen.ballX - left_point[0]) + left_point[1]
            #print("yonslope:",yOnSlope)
            if bulletGreen.ballY > yOnSlope:
                #print("below")
                bulletGreen.ballY = 750

            ##print("BULLET GREEN: ",bulletGreenCurrentPos)
            # detect collisions
            if green_turn:
                red_tank_rect = tankGame.red_rect
                green_bullet_rect = bulletGreen.bullet
                if red_tank_rect.colliderect(green_bullet_rect):
                    text = font.render('GAME OVER! Green Tank Wins!', True, (255,0,0), (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = (1280 // 2, 300)
                    #print('Green Bullet hit Red Tank!!!')
                    screen.blit(text,textRect)
                    pg.display.update()
                    time.sleep(3)
                    sys.exit()
                    #pygame.quit()



        pg.display.update()
