import pygame

def display_stats(screen, player):

    health_value = player.get('health', None)
    armor_value = player.get('armor', None)
    appetite_value = player.get('appetite', None)
    magical_number_cast_value = player.get('magical-number-cast', None)  

    # Tọa độ cho từng chỉ số
    start_x, start_y = 1325, 350  
    spacing = 125

    # Hiển thị health
    if health_value is not None:
        if health_value == 1:
            health_image = pygame.image.load('assets/gui/hp/1hp.png')
        elif health_value == 2:
            health_image = pygame.image.load('assets/gui/hp/2hp.png')
        elif health_value == 3:
            health_image = pygame.image.load('assets/gui/hp/3hp.png')
        elif health_value == 4:
            health_image = pygame.image.load('assets/gui/hp/4hp.png')
        elif health_value <= 0:
            health_image = pygame.image.load('assets/gui/hp/0hp.png')

        screen.blit(health_image, (start_x, start_y))

    # Hiển thị armor
    if armor_value is not None:
        if armor_value == 1:
            armor_image = pygame.image.load('assets/gui/armor/1armor.png')
        elif armor_value == 2:
            armor_image = pygame.image.load('assets/gui/armor/2armor.png')
        elif armor_value == 3:
            armor_image = pygame.image.load('assets/gui/armor/3armor.png')
        elif armor_value == 4:
            armor_image = pygame.image.load('assets/gui/armor/4armor.png')
        elif armor_value == 0:
            armor_image = pygame.image.load('assets/gui/armor/0armor.png')

        screen.blit(armor_image, (start_x, start_y + spacing))

    # Hiển thị appetite
    if appetite_value is not None:
        if appetite_value == 1:
            appetite_image = pygame.image.load('assets/gui/food/1food.png')
        elif appetite_value == 2:
            appetite_image = pygame.image.load('assets/gui/food/2food.png')
        elif appetite_value == 3:
            appetite_image = pygame.image.load('assets/gui/food/3food.png')
        elif appetite_value == 4:
            appetite_image = pygame.image.load('assets/gui/food/4food.png')
        elif appetite_value == 0:
            appetite_image = pygame.image.load('assets/gui/food/0food.png')

        screen.blit(appetite_image, (start_x + spacing, start_y))

    if magical_number_cast_value is not None:
        if magical_number_cast_value == 1:
            magical_number_cast_image = pygame.image.load("assets/gui/mana/1mana.png")
        elif magical_number_cast_value == 2:
            magical_number_cast_image = pygame.image.load("assets/gui/mana/2mana.png")
        elif magical_number_cast_value == 3:
            magical_number_cast_image = pygame.image.load("assets/gui/mana/3mana.png")
        elif magical_number_cast_value == 4:
            magical_number_cast_image = pygame.image.load("assets/gui/mana/4mana.png")
        elif magical_number_cast_value == 0:
            magical_number_cast_image = pygame.image.load("assets/gui/mana/0mana.png")

        screen.blit(magical_number_cast_image, (start_x + spacing, start_y + spacing))