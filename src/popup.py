import pygame
import time

# Hàm hiển thị pop-up thông báo
def show_popup(screen, message, duration=2, fade_duration=1):
    
    popup_width = 421
    popup_height = 50
    popup_color = (5, 42, 63)  # Màu nền của pop-up
    text_color = (255, 255, 255)  # Màu chữ
    border_color = (200, 128, 128)  # Màu viền
    border_thickness = 2  # Độ dày của viền

    # Tạo một surface cho pop-up với hỗ trợ alpha
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill(popup_color)

    # Vẽ văn bản
    font = pygame.font.Font('assets/font/font-times-new-roman/times-new-roman-14.ttf', 20)
    text = font.render(message, True, text_color)
    
    # Tính toán vị trí của pop-up
    popup_x = 32
    popup_y = 32

    # Căn giữa văn bản bên trong pop-up
    text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
    
    # Hiển thị pop-up trong khoảng thời gian cố định (2 giây)
    start_time = time.time()
    end_time = start_time + duration
    alpha = 255  # Hiển thị rõ ràng (alpha 255 là hoàn toàn không trong suốt)

    # Giai đoạn 1: Hiển thị rõ ràng trong duration giây
    while time.time() < end_time:
        popup_surface.set_alpha(alpha)
        
        # Vẽ viền xung quanh pop-up với độ dày đã xác định
        border_rect = pygame.Rect(popup_x - border_thickness, popup_y - border_thickness, popup_width + 2 * border_thickness, popup_height + 2 * border_thickness)
        pygame.draw.rect(screen, border_color, border_rect)
        
        # Vẽ pop-up và văn bản
        screen.blit(popup_surface, (popup_x, popup_y))
        screen.blit(text, text_rect)
        
        pygame.display.update()  # Chỉ cập nhật phần màn hình cần thiết
        pygame.time.delay(16)  # Giữ tốc độ khung hình ổn định (khoảng 60 FPS)

    # Giai đoạn 2: Mờ dần trong fade_duration giây
    fade_start_time = time.time()
    while time.time() - fade_start_time < fade_duration:
        # Cập nhật alpha để giảm dần từ 255 về 0 trong khoảng fade_duration
        elapsed_time = time.time() - fade_start_time
        alpha = 255 * (1 - elapsed_time / fade_duration)
        if alpha < 0:
            alpha = 0
        
        # Áp dụng alpha lên cả pop-up và viền mà không đổi màu
        popup_surface.set_alpha(alpha)

        # Tạo một surface viền với hỗ trợ alpha
        border_surface = pygame.Surface((popup_width + 2 * border_thickness, popup_height + 2 * border_thickness), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))  # Làm trong suốt nền
        pygame.draw.rect(border_surface, border_color, border_surface.get_rect(), border_thickness)  # Vẽ viền với độ dày đã xác định
        border_surface.set_alpha(alpha)  # Đồng bộ alpha với pop-up
        
        # Vẽ viền xung quanh pop-up
        screen.blit(border_surface, (popup_x - border_thickness, popup_y - border_thickness))
        
        # Vẽ pop-up và văn bản
        screen.blit(popup_surface, (popup_x, popup_y))
        screen.blit(text, text_rect)

        pygame.display.update()  # Chỉ cập nhật phần màn hình cần thiết
        pygame.time.delay(16)  # Giữ tốc độ khung hình ổn định (khoảng 60 FPS)
