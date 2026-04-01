import pygame

def DefaulRoom(screen, center):
    roomHeight = 600
    roomWidth = 800
    exitWidth = 80

    x = center.x - roomWidth // 2
    y = center.y - roomHeight // 2

    exitX = center.x - exitWidth // 2

    # 3 regular walls
    pygame.draw.line(screen, "white", (x, y), (x, y + roomHeight), 1) 
    pygame.draw.line(screen, "white", (x + roomWidth, y), (x + roomWidth, y + roomHeight), 1) 
    pygame.draw.line(screen, "white", (x, y + roomHeight), (x + roomWidth, y + roomHeight), 1) 

    # wall with exit
    pygame.draw.line(screen, "white", (x, y), (exitX, y), 1)
    pygame.draw.line(screen, "white", (exitX + exitWidth, y), (x + roomWidth, y), 1)

    #EXIT
    pygame.draw.line(screen, "red", (exitX, y), (exitX + exitWidth, y), 1)