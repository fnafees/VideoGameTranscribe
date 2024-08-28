import pygame
pygame.init()
pygame.joystick.init()

joysticks = []


for event in pygame.event.get():
    if event.type == pygame.JOYDEVICEADDED:
        print(event)


            