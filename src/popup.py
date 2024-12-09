import pygame
import time

# Hàm hiển thị pop-up thông báo
def show_popup(screen, message, duration=2, fade_duration=1):
    
    popup_width = 421
    popup_height = 50
    popup_color = (5, 42, 63) 
    text_color = (255, 255, 255) 
    border_color = (200, 128, 128) 
    border_thickness = 2

    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill(popup_color)

    font = pygame.font.Font('assets/font/font-times-new-roman/times-new-roman-14.ttf', 20)
    text = font.render(message, True, text_color)
    
    popup_x = 32
    popup_y = 32

    text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
    
    start_time = time.time()
    end_time = start_time + duration
    alpha = 255 

    # Giai đoạn 1: Giữ nguyên trạng thái trong duration giây.
    while time.time() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Nếu người dùng click chuột, thoát ngay khỏi vòng lặp, tức kết thúc animation.
                return
        
        popup_surface.set_alpha(alpha)
        
        # Vẽ viền xung quanh pop-up.
        border_rect = pygame.Rect(popup_x - border_thickness, popup_y - border_thickness, popup_width + 2 * border_thickness, popup_height + 2 * border_thickness)
        pygame.draw.rect(screen, border_color, border_rect)
        
        # Vẽ pop-up và văn bản.
        screen.blit(popup_surface, (popup_x, popup_y))
        screen.blit(text, text_rect)
        
        pygame.display.update()

    # Giai đoạn 2: Mờ dần trong fade_duration giây.
    fade_start_time = time.time()
    while time.time() - fade_start_time < fade_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Nếu người dùng click chuột, thoát ngay khỏi vòng lặp, tức kết thúc animation.
                return

        elapsed_time = time.time() - fade_start_time
        alpha = 255 * (1 - elapsed_time / fade_duration)
        if alpha < 0:
            alpha = 0
        
        popup_surface.set_alpha(alpha)

        border_surface = pygame.Surface((popup_width + 2 * border_thickness, popup_height + 2 * border_thickness), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0)) 
        pygame.draw.rect(border_surface, border_color, border_surface.get_rect(), border_thickness) 
        border_surface.set_alpha(alpha) 

        screen.blit(border_surface, (popup_x - border_thickness, popup_y - border_thickness))
        
        screen.blit(popup_surface, (popup_x, popup_y))
        screen.blit(text, text_rect)

        pygame.display.update()  
        pygame.time.delay(16)  
