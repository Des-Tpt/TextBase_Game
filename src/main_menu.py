import pygame
import pygame.freetype
import sys
from game import main
import webbrowser

pygame.init()
pygame.font.init()

screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Tải các ảnh nền
background_images = [
    pygame.image.load('assets/img/Background-1.png'),
    pygame.image.load('assets/img/Background-3.png'),
    pygame.image.load('assets/img/Background-4.png'),
]
background_images = [pygame.transform.scale(img, (screen_width, screen_height)) for img in background_images]

click_sound = pygame.mixer.Sound('assets/sound/old-radio-button-click-97549.mp3')

# Tải ảnh tiêu đề

background_music = pygame.mixer.music.load('assets/sound/Soldier, Poet, King - Cullen Vance.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

font_path = 'assets/font/dungeon-depths-font/DungeonDepths-owJWV.ttf'
font_size = 20
font = pygame.freetype.Font(font_path, font_size)

white = (255, 255, 255)
black = (0, 0, 0)
highlight_color = (255, 215, 0)

menu_option = ['Start game', 'Instruction', 'Developer', 'Quit']
menu_rects = []

# Thông số cho fading.
background_change_time = 5000  # 5000 ms = 5 giây
fade_duration = 1000  # 1000 ms = 1 giây
current_background_index = 0
next_background_index = 1
last_change_time = pygame.time.get_ticks()
alpha = 255 

# Cái này là animation đổi background.
def draw_menu(highlighted_index):
    global current_background_index, next_background_index, last_change_time, alpha

    current_time = pygame.time.get_ticks()
    time_since_change = current_time - last_change_time # Thời gian đã trôi qua từ lần đổi cuối.

    if time_since_change > background_change_time: # Nếu đã vượt quá thời gian quy định, bắt đầu đổi.
        alpha = max(255 - int((time_since_change - background_change_time) / fade_duration * 255), 0) # Trừ dần giá trị alpha theo một tỉ lệ của fade_duration, để xem được bao nhiêu phần trăm của alpha với tổng số 255. càng giảm, hình tiếp theo càng rõ.
        if alpha <= 0:
            current_background_index = next_background_index
            next_background_index = (current_background_index + 1) % len(background_images)
            last_change_time = current_time
            alpha = 255

    current_bg = background_images[current_background_index]
    next_bg = background_images[next_background_index]
    
    # Hiển thị background
    screen.blit(current_bg, (0, 0))
    next_bg.set_alpha(255 - alpha) # Độ trong suốt là 255 - alpha, alpha lúc đầu sẽ là 255, trừ phát ra 0, hình tiếp theo sẽ trong suốt. Nhưng alpha càng ngày càng trừ vậy số này sẽ càng ngày càng lớn và hình tiếp theo càng ngày càng rõ.
    screen.blit(next_bg, (0, 0))

    global menu_rects
    menu_rects = []

    for idx, option in enumerate(menu_option): # Hàm liệt kê trong python
        text_rect_x = screen_width // 4
        text_rect_y = screen_height // 2 - 80 + idx * 60 # idx dùng để cách lựa chọn. Lựa chọn thứ nhất tại chỗ, thứ 2 cách thứ nhất 60, thứ ba cách thứ nhất 120.

        text_rect = font.get_rect(option) # Lấy kích thước của các text trong option
        text_rect.topleft = (text_rect_x, text_rect_y) # Đặt tọa độ góc trên bên trái cùng của rect text là tọa độ đã quy định.

        menu_rects.append(text_rect)    # Ghi lại tọa độ cho rect text, được dùng để highlight các chữ khi dùng chuột chỉ vào.

        font.render_to(screen, (text_rect.x-1, text_rect.y), option, black) # Vẽ outline.
        font.render_to(screen, (text_rect.x+1, text_rect.y), option, black)
        font.render_to(screen, (text_rect.x, text_rect.y-1), option, black)
        font.render_to(screen, (text_rect.x, text_rect.y+1), option, black)

        if idx == highlighted_index: # Trạng thái hover có đang diễn ra không. Nếu có, tô vàng, nếu không, giữ chữ màu trắng.
            font.render_to(screen, text_rect.topleft, option, highlight_color)
        else:
            font.render_to(screen, text_rect.topleft, option, white)

    pygame.display.flip()

def fade_out():
    # Tạo một biến surface, và fill nó bằng màu đen.
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))
    
    initial_volume = pygame.mixer.music.get_volume() # Hàm get âm lượng.

    for alpha in range(0, 255, 5): # Tương tự như đổi hình, quy định biến alpha, và cho cái surface trong suốt lúc đầu.
        fade_surface.set_alpha(alpha)
        
        screen.fill((0, 0, 0))  
        screen.blit(background_images[current_background_index], (0, 0)) 
        screen.blit(fade_surface, (0, 0))

        new_volume = initial_volume * (1 - alpha / 255)
        pygame.mixer.music.set_volume(new_volume)

        pygame.display.update()
        pygame.time.delay(25)

def main_menu():
    highlighted_index = -1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos() 
                    for idx, rect in enumerate(menu_rects): # Xét từng vị trí trong danh sách menu_rects. Nếu mouse_pos trùng với vị trí đó, mặc định là ấn. Chạy hàm theo từng option.
                        if rect.collidepoint(mouse_pos):
                            click_sound.play()
                            if idx == 0:
                                fade_out() 
                                start_game()
                            elif idx == 1:
                                instruction()
                            elif idx == 2:
                                github_link()
                            elif idx == 3:
                                pygame.quit()
                                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                highlighted_index = -1
                for idx, rect in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos): # Xét từng vị trí trong danh sách menu_rects. Nếu mouse_pos trùng với vị trí đó. Highlight option.
                        highlighted_index = idx

        draw_menu(highlighted_index)

def start_game():
    print("Vào game...")
    pygame.time.delay(1500)
    main()

def instruction():
    print("Giới thiệu...")

def github_link():
    print("Github...")
    webbrowser.open("https://github.com/Des-Tpt")

if __name__ == "__main__":
    main_menu()
