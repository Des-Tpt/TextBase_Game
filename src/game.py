import pygame
import pygame.freetype
import random
from popup import show_popup

pygame.init()

screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))

BG_COLOR = (15, 42, 63)
TEXT_COLOR = (220, 220, 220)
OPTION_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (255, 215, 0)

font_path = 'assets/font/font-times-new-roman/times-new-roman-14.ttf'
font_size = 20
font = pygame.freetype.Font(font_path, font_size)

# Hình minh họa
image = pygame.image.load('assets/img/rockslide00b.png')
image = pygame.transform.scale(image, (image.get_width() / 1.5, image.get_height() / 1.5))

# Tọa độ hiển thị hình minh họa
image_rect = pygame.Rect(30, 125, image.get_width(), image.get_height())

def draw_hud():
    screen.fill(BG_COLOR)
    screen.blit(image, image_rect)

    line_color = (200, 128, 128) 
    line_width = 2 

    draw_line(screen, line_color, (screen_width // 3 - 80, 30), (screen_width // 3 - 80, screen_height - 30), line_width)
    draw_line(screen, line_color, (screen_width - 300, 30), (screen_width - 300, screen_height - 30), line_width)
    draw_line(screen, line_color, (screen_width - 30, 30), (screen_width - 30, screen_height - 30), line_width)
    draw_line(screen, line_color, (30, 30), (30, screen_height - 30), line_width)
    draw_line(screen, line_color, (30, 30), (screen_width - 30, 30), line_width)
    draw_line(screen, line_color, (30, screen_height - 30), (screen_width - 30, screen_height - 30), line_width)


def draw_line(screen, line_color, line_start, line_end, line_width):
    pygame.draw.line(screen, line_color, line_start, line_end, line_width)

def fade_in(surface, speed=5):
    fade = pygame.Surface((screen_width, screen_height))
    fade.fill((0, 0, 0)) 
    alpha = 255

    while alpha > 0:
        fade.set_alpha(alpha)

        surface.fill(BG_COLOR)
        draw_hud() 
        surface.blit(fade, (0, 0)) 
        
        pygame.display.update()

        alpha -= speed
        pygame.time.delay(30)


def fade_in_text(surface, text, color, rect, status, font, delay=1):
    total_length = len(text)
    current_length = 0
    start_time = pygame.time.get_ticks()

    while current_length < total_length:
        current_time = pygame.time.get_ticks()

        # Kiểm tra sự kiện chuột
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # Khi click chuột
                return  # Dừng hiệu ứng fade-in và thoát khỏi hàm

        if current_time - start_time > delay:
            current_length += 5
            start_time = current_time

        if status == False:
            break

        # Vẽ HUD và text với hiệu ứng fade-in
        surface.fill(BG_COLOR)
        draw_hud()  # Luôn vẽ HUD nếu có cập nhật
        drawText(surface, text[:current_length], color, rect, font)

        pygame.display.update()  # Cập nhật màn hình một lần mỗi vòng lặp


def drawText(surface, text, color, rect, font, bkg=None): # Code em chôm được từ forum pygame.
    rect = pygame.Rect(rect)
    y = rect.top - 50
    lineSpacing = 10 
    indent = 30
    fontHeight = font.get_sized_height()

    lines= text.split('#')

    for index, line in enumerate(lines):
        is_first_line = True  

        while line:
            i = 1
            indent_x = rect.left + (indent if is_first_line else 0) #Dùng để thụt lề ở đoạn văn đầu tiên.

            if y + fontHeight > rect.bottom:
                break

            while font.get_rect(line[:i]).width < rect.width and i < len(line): # Đây là hàm kiểm tra chiều rộng từ đầu văn phản đến thứ tự thứ i.
                i += 1  #Nếu vẫn bé hơn chiều rộng của khung và text vẫn còn, cộng +1 cho i.

            if i < len(line): # Nếu hết dòng rồi mà đoạn văn vẫn chưa hết.
                i = line.rfind(" ", 0, i) + 1 #Tìm vị trí của dấu cách gần i nhất để không thay ngựa giữa dòng.

            if bkg: # Đoạn này được dùng để tạo ra 1 bức ảnh từ đoạn text đã viết. 
                image = font.render(line[:i], fgcolor=color, bgcolor=bkg)[0]
            else:
                image = font.render(line[:i], fgcolor=color)[0]

            surface.blit(image, (indent_x, y)) # Render bức ảnh ra.
            y += fontHeight + lineSpacing # Xuống dòng.

            line = line[i:] # Cắt đoạn text từ i ra sau. [:i] là từ trước tới i, [i:] là từ i về sau.
            is_first_line = False

    return line


def draw_and_handle_options(surface, options, option_rect, highlighted_index=None):
    option_y = option_rect.top
    lineSpacing = 10
    option_height = font.get_sized_height()

    option_hitboxes = []

    for i, option in enumerate(options):
        has_requirements, _ = check_requirements(option, player)
        option_text = option["text"] if has_requirements else option.get("sateless", "Không thể thực hiện hành động này")

        option_color = HIGHLIGHT_COLOR if i == highlighted_index and has_requirements else (150, 150, 150) if not has_requirements else OPTION_COLOR

        current_y = option_y
        hitbox_height = 0 

        while option_text:
            j = 1
            # Lưu trữ giá trị get_rect để tránh gọi nhiều lần trong khi render
            rendered_width = font.get_rect(option_text[:j]).width
            while rendered_width < option_rect.width and j < len(option_text):
                j += 1
                rendered_width = font.get_rect(option_text[:j]).width

            if j < len(option_text):
                j = option_text.rfind(" ", 0, j) + 1

            font.render_to(surface, (option_rect.left, current_y), option_text[:j], option_color)
            current_y += option_height + lineSpacing

            option_text = option_text[j:]
            hitbox_height += option_height + lineSpacing 

        if has_requirements:
            option_hitboxes.append(pygame.Rect(option_rect.left, option_y, option_rect.width, hitbox_height))
        else:
            option_hitboxes.append(None)

        option_y += hitbox_height

    # Xử lý sự kiện chuột tách biệt để không phải tính toán hitbox khi render
    mouse_pos = pygame.mouse.get_pos()
    new_highlighted_index = -1

    for i, hitbox in enumerate(option_hitboxes):
        if hitbox is not None and hitbox.collidepoint(mouse_pos):
            new_highlighted_index = i

    return new_highlighted_index

def draw_text_and_options(surface, text, options, text_rect, option_rect, highlighted_index=None):
    drawText(surface, text, TEXT_COLOR, text_rect, font)

    text_height = get_text_height(text, font, text_rect)
    option_rect.top = text_rect.top + text_height

    draw_line(screen, (200, 128, 128), (465, option_rect.top - 35), (screen_width - 310, option_rect.top - 35), 2)

    return draw_and_handle_options(surface, options, option_rect, highlighted_index)

def get_text_height(text, font, rect):
    lines = text.split('#')  # Chia đoạn văn thành các đoạn nhỏ dựa vào dấu #
    font_height = font.get_sized_height()
    line_spacing = 10  # Khoảng cách giữa các dòng
    total_height = 0

    # Tính chiều cao của từng đoạn văn bản
    for line in lines:
        while line:
            i = 1
            rendered_width = font.get_rect(line[:i]).width # line[:i]: Từ đầu dòng tới vị trí i.
            while rendered_width < rect.width and i < len(line):
                i += 1
                rendered_width = font.get_rect(line[:i]).width

            if i < len(line):
                i = line.rfind(" ", 0, i) + 1

            # Tăng tổng chiều cao với mỗi dòng
            total_height += font_height + line_spacing
            line = line[i:]  # line[:i]: Từ vị trí i tới phần còn lại.

    return total_height


def change_scene(text, options, text_rect, option_rect):
    highlighted_index = -1
    running_scene = True
    fade_in_text(screen, text, TEXT_COLOR, text_rect, running_scene, font)

    while running_scene:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_scene = False
                break

        draw_hud()

        # Hiển thị văn bản và các tùy chọn
        highlighted_index = draw_text_and_options(
            screen, text, options, text_rect, option_rect, highlighted_index
        )

        if pygame.mouse.get_pressed()[0]:  # Kiểm tra xem người dùng có click chuột không
            if highlighted_index != -1:
                selected_option = options[highlighted_index]

                # Áp dụng hiệu ứng của lựa chọn (nếu có)
                apply_status(selected_option, player)

                # Kiểm tra nếu có danh sách scene tiếp theo
                next_scenes = selected_option.get("next_scenes")
                if next_scenes:
                    # Random scene từ danh sách
                    next_scene = random.choice(next_scenes)
                else:
                    # Nếu không có danh sách, lấy scene bình thường
                    next_scene = selected_option.get("next_scene", -1)

                return next_scene  # Trả về scene tiếp theo

        pygame.display.update()  # Cập nhật màn hình


text_rect = pygame.Rect(480, 100, 760, 600) # Khung hoạt động của đoạn văn.
option_rect = pygame.Rect(500, 400, 760, 100) # Khung hoạt động của các lựa chọn.
ui_rect = pygame.Rect(750, 100, 1000, 600 ) # Khung giao diện (máu, giáp, đói bụng). Chưa làm xong.

# Player Stat và các scene cho demo.

player = {
    "name": "",
    "strength": 0,
    "appetite": 0,
    "coin": 0,
    "magical": "false",
    "magical-number-cast": 0,
    "role": '',
    "will": '',
    "inventory": [],
    "arrow": 0
}

scenes = [
    # Scene 0:
     {
        "text": ("Những năm năm mươi trước Kỷ Định ranh, thời kỳ tiền lập quốc... #Thời kỳ mà những cỗ lò rèn đầy ắp than hồng vẫn bền bỉ tiếp sức cho ngọn lửa chiến tranh. #Thời kỳ mà những cỗ lò rèn đầy ắp than hồng vẫn bền bỉ tiếp sức cho ngọn lửa chiến tranh. #Thời kỳ mà hòa bình chỉ là một phương ngữ tại các vùng địa cực xa xôi. #Thời kỳ mà hạnh phúc chỉ là giấc một mộng hão huyền. #Thời kỳ mà vững mạnh chỉ là những mảnh kí ức khi hồi tưởng về một thời kỳ xưa cũ. #Lục địa Custandel, vùng đất bị các vị thần ruồng bỏ, luôn đắm chìm trong những cuộc tắm máu chẳng biết đến ngày mai... #Rong rủi phi ngựa băng qua khu rừng dưới chân dãy núi Stoughmagne. Âm thanh xào xạc của cơn gió đêm như đang chào đón một linh hồn khác biệt đặt những bước đầu tiên đến vùng đất người ta hay gọi là Grimhold...#Đó là bạn... Bạn đến đây để..."),
        "options": [
            {
                "text": "Tiêu diệt toàn bộ các tông đồ quỷ dữ dưới tư cách là một Sinner - Ma pháp sư quyền năng phục vụ Đế chế...",
                "attributes": {
                    "role": "Sinner",
                    "strength": 6,
                    "magic": True,
                    "magical-number-cast": 3,
                    "will": 'Giết quỷ.',
                    "coin": 10
                }, "next_scene": 1
            },
            {
                "text": "Cố gắng tồn tại... Tôi cần tiền, thức ăn, nước uống để tồn tại... Thứ duy nhất tôi có... là sức mạnh cơ bắp.",
                "attributes": {
                    "role": "Wanderer",
                    "strength": 8,
                    "magic": False,
                    "will": 'Sống.',
                    "coin": 2
                }, "next_scene": 1
            },
            {
                "text": "Gia nhập một quân đoàn. Tôi sẽ tranh thủ thời kỳ vàng son này để kiếm bạc.",
                "attributes": {
                    "role": "Mercenary",
                    "strength": 5,
                    "magic": False,
                    "will": 'Khao khát.',
                    "coin": 20
                }, "next_scene": 1
            },
            {
                "text": "Tìm kiếm sức mạnh ở những con quỷ để thay đổi số phận... Tôi tự hào mình là một tồng đồ...",
                "attributes": {
                    "role": "Demon Believer",
                    "strength": 4,
                    "magic": True,
                    "magical-number-cast": 2,
                    "will": 'Học hỏi quỷ thuật.',
                    "coin": 5
                }, "next_scene": 1
            }
        ]
    },
    {
        # Scene 1:
        "text": ("Ngồi trên lưng chú ngựa Roach, bạn chậm rãi tiến về phía trước trên mặt đất gồ ghề. Những thảm thực vật xanh tươi ở hai bên cánh rừng đang âm thầm vươn mình xóa bỏ những dấu vết cuối cùng của con đường mòn cũ kỹ. Ánh trăng sáng thấp thoáng sau những tán cây rậm, tạo thành những khoảng sáng tối đan xen như một màn kịch bí ẩn diễn ra giữa đêm đen. #Dưới bầu trời đêm đen đặc, dãy núi xa xa hiện lên như những bóng đen u ám, khổng lồ, nuốt chửng lấy bầu trời sao thưa thớt. Ánh trăng bạc vắt ngang qua đỉnh núi, lấp ló sau cạnh biển mây trôi lững lờ.#Ở Lorathern, đặc biệt là Vương đô, chuyện đi đi lại lại dưới ánh trăng mờ chưa bao giờ là điều kỳ lạ... Bạn nhớ lại vô số lần bản thân đã từng dành cả đêm chỉ để đi vòng quanh khắp khu phố thị. #Tuy nhiên... Đây là Northern...#Dù khu rừng dường như chìm vào trong tĩnh lặng, nhưng đôi tai của bạn, đôi tai của một kẻ đã sống đủ lâu để có thể mường tượng được hàng nghìn cách chết của bản thân qua mỗi giây, mỗi phút. Bạn sẽ nhận ra nơi này không hoàn toàn yên ắng. Tiếng gió rít khe khẽ luồn qua những tán lá, tiếng kêu văng vẳng của một loài sinh vật xa lạ khiến không gian thêm phần rùng rợn. Có thứ gì đó đang ẩn nấp trong bóng tối... #Bạn ngay lập tức kiểm tra vũ khí của mình..."),
        "options": [
            {
                "text": "Tôi mang theo một thanh trường kiếm và một tấm khiên gỗ.",
                "requirement": {"role": ["Sinner","Mercenary"]},
                "add_items": ["thanh trường kiếm", "tấm khiên gỗ"],
                "sateless": "Tôi không đủ giàu có để sở hữu một thanh trường kiếm và một tấm khiên gỗ.",
                "next_scene": 2,
            },
            {
                "text": "Xạ kích là sở trường của tôi, tôi mang theo một cây nỏ và một bó mũi tên, cùng cây chủy thủ sau hông.",
                 "requirement": {"role": ["Sinner","Mercenary"]},
                "add_items": ["cây chủy thủ", "chiếc nỏ"],
                "effect": {"arrow": 5 },
                "sateless": "Tôi không thể sử dụng nỏ và chủy thủ...",
                "next_scene": 2,
            },
            {
                "text": "Một cây rìu cán dài sẽ tiện dụng hơn ở các chuyến đi xa... và một cây dao nhỏ.",
                "requirement": {"role": ["Mercenary","Wanderer"]},
                "add_items": ["cây rìu cán dài", "cây dao nhỏ"],
                "sateless": "Tại sao tôi phải mang theo rìu?",
                "next_scene": 2,
            },
            {
                "text": "Tôi chỉ có một con dao găm. Nhưng... ma pháp của tôi là quá đủ...",
                "requirement": {"role": ["Sinner","Demon Believer"]},
                "sateless": "Tôi không thể sử dụng ma pháp.",
                "next_scene": 2,
                "add_items": ["con dao găm"],
            }
        ]
    },
    {
        #Scene 2:
            "text": ("Sau khi đã đảm bảo rằng vũ khí vẫn còn có thể sử dụng, bạn quật dây cương làm khiến cho chú ngựa hí lên một tiếng to và bắt đầu phi nước kiệu. Bạn vẫn không ngừng đảo mắt giữa hai bên cánh rừng để chắc chắn bản thân sẽ không bỏ lỡ bất kỳ dấu hiệu bất thường nào... #Xào xạc... #Từ trên lưng ngựa, bạn dễ dàng nhận ra sự hỗn loạn của những bụi cỏ dày đặc hai bên đường. Chúng lay động dữ dội, theo cùng hướng mà bạn và con ngựa đang phi đến. Trong sự chuyển động bất thường ấy, đôi mắt bạn bắt được một bóng hình — lờ mờ nhưng dễ đoán — một sinh vật bốn chân với bộ lông trắng. Sói tuyết... bầy của nó đang truy đuổi theo bạn và chú ngựa Roach..."),
            "options": [
                {
                    "text": "Tôi thúc ngựa tăng tốc.",
                    "attributes": {"health": 4, "armor": 2},
                    "next_scene": 3,
                },
                {
                    "text": f"Ngựa của tôi không thể nào sánh bằng tốc độ của loài sói tuyết... Tôi rút vũ khí ra và chuẩn bị sẳn sàng cho tình huống xấu nhất.",
                    "requirement": {"items":["thanh trường kiếm", "cây rìu cán dài"]},
                    "attributes": {"health": 4, "armor": 2},
                    "sateless": "Tôi không có vũ khí đủ dài để sử trên lưng ngựa...",
                    "next_scene": 3,
                },
                {
                    "text": "Tôi dùng nỏ, bắn tên vào những lùm cây chuyển động ở gần con đường mòn.",
                    "requirement": {"items":["chiếc nỏ"], "arrow": 1},
                    "sateless": "Tôi không thể dùng nỏ.",
                    "attributes": {"health": 4, "armor": 2},
                    "effect": {"arrow": -3},
                    "next_scene": 4,
                },
                {
                    "text": "Tốn một lượt ma pháp, thi triển hai phép Cầu Lửa bắn những lùm cây, tạo ra ngọn lửa rực giữa cánh.",
                    "requirement": {"role": ["Sinner", "Demon Believer"], "magical-number-cast": 2},
                    "sateless": "Tôi không thể thi triển ma pháp.",
                    "effect": {"magical-number-cast": -2},
                    "attributes": {"health": 4, "armor": 2},
                    "next_scene": 5,
                }
            ]
    },
    {
        #Scene 3:
            "text": (""),
            "options":"",
    }
]

# Các hàm tối ưu hóa cho các dạng lựa chọn

def apply_status(option, player):

    # Gán thông số
    if "attributes" in option:
        for key, value in option["attributes"].items():
            player[key] = value

    # Sửa đổi thông số
    if "effect" in option:
        for key, value in option["effect"].items():
            if isinstance(value, int):
                player[key] += value  # Cộng dồn cho giá trị

    # Thêm item vào inventory
    if "add_items" in option:
        for item in option["add_items"]:
            if item not in player["inventory"]:
                show_popup(screen, f"Bạn đã nhận được một {item}.")
                player["inventory"].append(item)
                print(player)

    # Xóa item
    if "remove_items" in option:
        for item in option["remove_items"]:
            if item in player["inventory"]:
                player["inventory"].remove(item)
                show_popup(screen, f"Bạn đã mất một {item}.")

def check_requirements(option, player):
    requirements = option.get("requirement", {})
    
    for key, value in requirements.items():
        if key == "items":
            # Nếu yêu cầu là item, kiểm tra item của player
            if isinstance(value, list):
                if not any(item in player["inventory"] for item in value):
                    return False, key  
            else:
                if value not in player["inventory"]:
                    return False, key  
                
        elif key == "role":
            # Nếu yêu cầu là role, kiểm tra role của player
            if isinstance(value, list):
                if player.get("role") not in value:
                    return False, key 
            else:
                if player.get("role", '') != value:
                    return False, key 
        else:
                if player.get(key, 0) < value:
                    return False, key
                
    return True, None 



def main():
    current_scene = 0
    fade_in(screen)
    pygame.display.set_caption('Grimhold')
    running = True

    while running:
        scene_data = scenes[current_scene]
        choice = change_scene(scene_data["text"], scene_data["options"], text_rect, option_rect)

        if choice == -1:  # Người chơi thoát khỏi trò chơi
            running = False
            break

        elif running == True and choice != None and choice < len(scenes):  # Chuyển sang scene tiếp theo
            current_scene = choice
        else: 
            pygame.quit()
            

if __name__ == '__main__':
    main()
