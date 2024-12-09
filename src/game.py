import pygame
import pygame.freetype
import random
from popup import show_popup
from display_stats import display_stats

pygame.init()

screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)

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

    #Vẽ các đường để tạo thành các phần trong UI.
    draw_line(screen, line_color, (screen_width // 3 - 80, 30), (screen_width // 3 - 80, screen_height - 30), line_width)
    draw_line(screen, line_color, (screen_width - 300, 30), (screen_width - 300, screen_height - 30), line_width)
    draw_line(screen, line_color, (screen_width - 30, 30), (screen_width - 30, screen_height - 30), line_width)
    draw_line(screen, line_color, (30, 30), (30, screen_height - 30), line_width)
    draw_line(screen, line_color, (30, 30), (screen_width - 30, 30), line_width)
    draw_line(screen, line_color, (30, screen_height - 30), (screen_width - 30, screen_height - 30), line_width)


def draw_line(screen, line_color, line_start, line_end, line_width):
    pygame.draw.line(screen, line_color, line_start, line_end, line_width)

def fade_in(surface, speed=5):
    fade = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
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
            if event.type == pygame.MOUSEBUTTONDOWN:  # Khi click chuột.
                return  # Dừng hiệu ứng fade-in và thoát khỏi hàm.

        if current_time - start_time > delay:
            current_length += 5
            start_time = current_time

        if status == False:
            break

        # Vẽ HUD và text với hiệu ứng fade-in
        surface.fill(BG_COLOR)
        draw_hud()  # Luôn vẽ HUD nếu có cập nhật
        drawText(surface, text[:current_length], color, rect, font)
        display_stats(screen, player)

        pygame.display.update()  # Cập nhật màn hình một lần mỗi vòng lặp


def drawText(surface, text, color, rect, font, bkg=None): # Code em mượn được từ forum pygame.
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

            while font.get_rect(line[:i]).width < rect.width and i < len(line): # Đây là hàm kiểm tra chiều rộng từ đầu văn bản đến thứ tự thứ i.
                i += 1  #Nếu vẫn bé hơn chiều rộng của khung và text vẫn còn, cộng +1 cho i.

            if i < len(line): # Nếu hết dòng rồi mà đoạn văn vẫn chưa hết.
                i = line.rfind(" ", 0, i) + 1 #Tìm vị trí của dấu cách gần i nhất để không thay ngựa giữa dòng.

            if bkg: #Render thẳng lên surface.
                font.render_to(surface, (indent_x, y), line[:i], fgcolor=color, bgcolor=bkg)
            else:
                font.render_to(surface, (indent_x, y), line[:i], fgcolor=color)

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
        has_requirements, _ = check_requirements(option, player) #Kiểm tra xem lựa chọn này có yêu cầu gì không.
        option_text = option["text"] if has_requirements else option.get("sateless", "Không thể thực hiện hành động này")
        #Nếu có, thì kiểm tra xem có thỏa mãn được yêu cầu đó không, nếu không thì get biến sateless thay vì text.

        option_color = HIGHLIGHT_COLOR if i == highlighted_index and has_requirements else (150, 150, 150) if not has_requirements else OPTION_COLOR
        #Màu của option sẽ phụ thuộc vào việc, nó có đang được hover, đang bị khóa không thể chọn, hay đang bình thường.

        current_y = option_y
        hitbox_height = 0 

        while option_text:
            j = 1
            #Tương tự như draw_text, nhưng vì không không có các đoạn văn nên đơn giản hơn.
            rendered_width = font.get_rect(option_text[:j]).width
            while rendered_width < option_rect.width and j < len(option_text):
                j += 1
                rendered_width = font.get_rect(option_text[:j]).width

            if j < len(option_text):
                j = option_text.rfind(" ", 0, j) + 1
            font.render_to(surface, (option_rect.left, current_y), option_text[:j], option_color)
            current_y += option_height + lineSpacing

            option_text = option_text[j:] #Cắt bỏ phần đã hiển thị, như draw_text.
            hitbox_height += option_height + lineSpacing #Tính chiều cao của dòng chữ, để tạo hitbox.

        if has_requirements: #Kiểm tra xem là requirements có được thỏa mãn không, nếu có tạo 1 rect để người dùng tương tác.
            option_hitboxes.append(pygame.Rect(option_rect.left, option_y, option_rect.width, hitbox_height))
        else:                #Nếu không, không tạo rect.
            option_hitboxes.append(None)

        option_y += hitbox_height #Xuống dòng, render tiếp option còn lại.

    # Xử lý sự kiện chuột tách biệt để không phải tính toán hitbox khi render.
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
    lines = text.split('#')  # Chia đoạn văn thành các đoạn nhỏ dựa vào dấu #.
    font_height = font.get_sized_height()
    line_spacing = 10  # Khoảng cách giữa các dòng.
    total_height = 0

    # Tính chiều cao của từng đoạn văn bản.
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
        display_stats(screen, player)

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
ui_rect = pygame.Rect(750, 100, 1000, 600 ) # Khung giao diện (máu, giáp, đói bụng).

# Player Stat và các scene cho demo.

player = {
    "name": "",
    "strength": 0,
    "coin": 0,
    "experiment": 0,
    "magical": "false",
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
                    "experiment": 3,
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
                    "experiment": 5,
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
                    "experiment": 3,
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
                    "experiment": 1,
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
                    "next_scene": 11,
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
            "text": ("Vì bị lũ sói ở hai bên đường thu hút hoàn toàn sự chú ý, bạn đã vô tình bỏ qua chiếc lưới đã được lũ quái vật giăng sẳn. Roach hí lên một tiếng kêu đầy sợ hãi, trước mặt nó ngay bây giờ là hai sinh vật nhỏ bé với lớp da xanh, tay cầm mấy cây gỗ dài được chuốt nhọn làm giáo. Cách ăn mặc của bọn chúng không khác gì người tiền sử, chỉ có một chiếc khố cùng vài hiện vật trang trí đeo trên cổ hoặc tay. Chúng gào lên thứ ngôn ngữ kì dị khi lao thẳng về phía bạn... Goblin... Bạn thì thầm trong miệng khi nhớ về lời cảnh báo của thầy cũ... Ông ấy đã qua đời trong một lần lũ goblin và hob tấn công vào làng."),
            "options": [
                {
                    "text" : "Tìm cách nhảy qua đầu của hai con goblin.",
                    "effect" : {"health": -1},
                    "next_scene": 4,
                },
            ]
    },
    {
        #Scene 4:
            "text": ("Bạn lựa chọn một hành động táo bạo, nhưng bạn biết mình không còn cách nào khác. Bạn giật mạnh dây cương ra hiệu cho chú ngựa Roach và nó biết bạn đang muốn làm gì. Giậm chân một phát đầy uy lực, Roach bay qua đầu hai sinh vật gớm ghiếc và thành công đáp xuống đất, tạo khoảng cách với lũ goblin... nhưng chỉ trong chốc lát. Một tiếng gào khác vang lên, từ xa, bạn nhận ra đây không chỉ là hai con goblin đơn lẻ mà là cả một đàn. Ít nhất năm, có thể là mười con... Bọn chúng đang dần tiến lại phía bạn, ánh lửa từ ngọn đuốc của chúng làm sáng cả một góc rừng."),
            "options": [
            {
                "text": "Tôi vung vũ khí lao thẳng vào lũ goblin, hy vọng đánh bại càng nhiều càng tốt trước khi kiệt sức.",
                "requirement": {"strength": 6},
                "attributes": {"health": -3},
                "sateless": "Tôi không có đủ sức để chiến đấu trực tiếp với lũ goblin.",
                "next_scene": 12,
            },
            {
                "text": "Chạy vào rừng, hy vọng rằng bóng tối sẽ giúp tôi trốn thoát.",
                "attributes": {"health": -1},
                "next_scene": 6,
            }
        ]
    },
    {
        #Scene 5:
            "text": ("Bạn bị thương không nhẹ, máu từ những vết trầy xước và đâm cắt khiến bạn yếu dần. Tuy nhiên, sau vài giờ chạy trốn, bạn cuối cùng cũng thoát khỏi khu vực nguy hiểm. Trước mặt bạn là một hang động, bên trong phát ra ánh sáng lập lòe của lửa. Có lẽ đây là nơi trú ẩn của một ai đó... hoặc thứ gì đó."),
            "options": [
            {
                "text": "Tiến vào hang động, hy vọng tìm được nơi nghỉ chân hoặc điều gì hữu ích.",
                "next_scene": 7,
            },
            {
                "text": "Tôi không tin vào những điều bất ngờ. Tôi tìm chỗ nghỉ ngơi ngoài trời, dù nguy hiểm nhưng an toàn hơn vào hang.",
                "attributes": {"health": -1},
                "next_scene": 8,
            }
        ]
    },
    {
        #Scene 6:
            "text": ("Bóng tối rừng già thực sự đáng sợ, đặc biệt khi bạn không biết rõ phương hướng. Bạn cảm thấy như có những đôi mắt dõi theo từ mọi hướng. Tiếng bước chân của những sinh vật lạ vang lên gần hơn. Bạn dừng lại, cảm nhận không khí xung quanh... Có điều gì đó đang đến gần."),
            "options": [
            {
                "text": "Sử dụng vũ khí, chuẩn bị cho một trận chiến trong bóng tối.",
                "requirement": {"items": ["thanh trường kiếm", "cây rìu cán dài"]},
                "attributes": {"health": -2},
                "sateless": "Tôi không có vũ khí đủ mạnh.",
                "next_scene": 9,
            },
            {
                "text": "Tôi dùng ma pháp để thắp sáng khu vực xung quanh, tạo ra một ngọn lửa lớn để dọa địch.",
                "requirement": {"magical-number-cast": 1, "role": ["Sinner", "Demon Believer"]},
                "effect": {"magical-number-cast": -1},
                "next_scene": 9,
            },
            {
                "text": "Tôi tiếp tục chạy, không dừng lại bất kỳ giây phút nào.",
                "attributes": {"health": -2},
                "next_scene": 8,
            }
        ]
    },
    {
        #Scene 7:
            "text": ("Bạn nhẹ nhàng tiến vào hang động. Ánh sáng từ ngọn lửa lập lòe chiếu sáng từng vách đá thô ráp. Bên trong, bạn nhìn thấy một người đàn ông già với mái tóc bạc trắng, tay cầm một cây gậy dài. Ông ta mặc một chiếc áo choàng bạc phơ, ánh mắt đầy kinh nghiệm nhưng lại toát lên vẻ nguy hiểm. Ông nhìn bạn, mỉm cười mời bạn lại gần. \"Ta đã chờ ngươi,\" ông nói, giọng trầm ấm nhưng đầy bí ẩn. Đây có phải là một cái bẫy?"),
            "options": [
            {
                "text": "Tiến lại gần và trò chuyện, cố gắng tìm hiểu lý do ông ấy biết bạn.",
                "next_scene": 10,
            },
            {
                "text": "Tôi không tin ông ta. Tôi rút vũ khí và yêu cầu ông giải thích ngay.",
                "requirement": {"items": ["thanh trường kiếm", "cây dao nhỏ"]},
                "sateless": "Tôi không có vũ khí để đe dọa ông ta.",
                "next_scene": 11,
            },
            {
                "text": "Tôi quay người rời khỏi hang động, cảm giác nơi này không an toàn.",
                "next_scene": 8,
            }
        ]
    },
    {
        #Scene 8:
            "text": ("Bạn tìm được một gò đất cao, có thể quan sát xung quanh và tránh bị tấn công bất ngờ. Trăng vẫn sáng trên bầu trời, nhưng không đủ để xua tan đi sự cô đơn và mệt mỏi của bạn. Ngồi xuống, bạn kiểm tra vết thương của mình. Dù không nghiêm trọng, chúng cũng đủ khiến bạn mất đi sức lực. Bạn ngủ thiếp đi trong khi vẫn giữ chặt vũ khí trong tay, sẵn sàng cho bất kỳ điều gì."),
            "options": [
            {
                "text": "Tôi sẽ cố gắng ngủ để hồi phục sức lực.",
                "attributes": {"health": 2},
                "next_scene": 12,
            },
            {
                "text": "Tôi không thể ngủ. Tôi phải đi tiếp để giữ khoảng cách với lũ goblin.",
                "attributes": {"health": -1},
                "next_scene": 9,
            }
        ]
    },
    {
        #Scene 9:
            "text": ("Tiếng gió rít qua những tán cây và tiếng chân nhẹ nhàng vang lên. Bạn quay người, phát hiện một sinh vật nhỏ bé nhưng nhanh nhẹn đang lao về phía mình — một goblin. Nó gào lên khi lao tới, tay cầm một thanh dao thô sơ nhưng sắc bén. Bạn có rất ít thời gian để phản ứng."),
            "options": [
        {
                "text": "Tôi dùng vũ khí để chống trả.",
                "requirement": {"items": ["thanh trường kiếm", "cây rìu cán dài"]},
                "attributes": {"health": -2},
                "sateless": "Tôi không có vũ khí để đối phó.",
                "next_scene": 10,
            },
            {
                "text": "Tôi dùng phép thuật để bắn hạ nó trước khi nó tới gần.",
                "requirement": {"magical-number-cast": 1, "role": ["Sinner", "Demon Believer"]},
                "effect": {"magical-number-cast": -1},
                "attributes": {"health": -1},
                "sateless": "Tôi không thể thi triển phép thuật ngay bây giờ.",
                "next_scene": 10,
            },
            {
                "text": "Tôi né sang một bên và cố gắng chạy thoát.",
                "attributes": {"health": -3},
                "next_scene": 8,
            }
        ]
    },
    {   
        #Scene 10:
            "text": ("Người đàn ông già nhìn bạn một cách chăm chú. \"Ngươi không phải một kẻ tầm thường. Số mệnh đã dẫn dắt ngươi đến đây,\" ông nói, giọng nói dường như vang vọng trong đầu bạn. Ông đưa cho bạn một vật — một viên pha lê phát sáng yếu ớt. \"Hãy cầm lấy, nó sẽ dẫn đường cho ngươi khi bóng tối bao trùm.\" Bạn cảm thấy một luồng sức mạnh nhỏ bé truyền vào cơ thể mình khi chạm vào viên pha lê."),
            "options": [
            {
                "text": "Tôi nhận viên pha lê và cảm ơn ông ta.",
                "add_items": ["viên pha lê ánh sáng"],
                "attributes": {"health": 2},
            },
            {
                "text": "Tôi từ chối món quà và hỏi ông ta về lý do thực sự của sự giúp đỡ này.",
            },
            {
                "text": "Tôi rút vũ khí và đe dọa ông ta, nghĩ rằng đây có thể là một cái bẫy.",
                "requirement": {"items": ["cây rìu cán dài", "thanh trường kiếm"]},
                "sateless": "Tôi không có vũ khí đủ mạnh để đe dọa ông ta.",
            }
        ]
    },
    {
        #Scene 11:
            "text": ("Những mũi tên sắc lẹm của bạn rít lên khi chúng dũng mãnh lao vào cánh rừng già... Từ sau những bụi cỏ âm u, một dòng nước bắn lên không trung, phết lên không gian xung quanh một màu đỏ chết chóc...#Bạn đã làm được, lũ thú săn mồi có thể vẫn chưa mất mạng, nhưng chắc chắn bọn chúng đã không còn đủ sức để có thể bắt kịp tốc độ của chú ngựa Roach... Những tưởng đến đây, bạn đã có thể an toàn mà đến đích. Nhưng không, từ phía cuối con đường, hai sinh vật nhỏ bé với lớp da xanh bước ra, tay cầm mấy cây gỗ dài được chuốt nhọn làm giáo. Cách ăn mặc của bọn chúng không khác gì người tiền sử, chỉ có một chiếc khố cùng vài hiện vật trang trí đeo trên cổ hoặc tay. Chúng gào lên thứ ngôn ngữ kì dị khi lao thẳng về phía bạn... #Goblin... Bạn thì thầm trong miệng khi nhớ về lời cảnh báo của thầy cũ... Ông ấy đã qua đời trong một lần lũ goblin và hob tấn công vào làng."),
            "options": [
            {       
                    "text" : "Tôi chỉ có một lựa chọn duy nhất... Tìm cách nhảy qua đầu của hai con goblin.",
                    "effect" : {"health": -1},
                    "next_scene": 4,
            }
        ]
    },
    {
        #Scene 12:
            "text": ("Bạn bị đè bẹp bởi bầy goblin, chú ngựa Roach bị một ngọn giáo thô sơ đâm xuyên qua ngực và ngã ngụy. Bạn rớt xuống lưng ngựa và nằm bất lực giữa bầy goblin. Chúng dùng mọi loại vũ khí mà chúng góp nhặt được để đánh vào bụng bạn, đập vào đầu bạn, và chặt hết tay chân của bạn... #Dù có là một tay mạo hiểm giả cừ khôi, bạn vẫn chỉ là con người, bạn đã quá tự cao vào bản thân... #Game over..."),
            "options": [
            {
                    "text" : "Chơi lại từ đầu...",
                    "next_scene" : 0,
            }
        ]
    }
]

# Các hàm tối ưu hóa cho các dạng lựa chọn

def apply_status(option, player):

    # Gán stat.
    if "attributes" in option:
        for key, value in option["attributes"].items():
            player[key] = value
            print(player)

    # Sửa đổi stat.
    if "effect" in option:
        for key, value in option["effect"].items():
            if isinstance(value, int):
                player[key] += value  # Cộng dồn cho giá trị

    # Thêm item vào inventory.
    if "add_items" in option:
        for item in option["add_items"]:
            if item not in player["inventory"]:
                show_popup(screen, f"Bạn đã nhận được một {item}.")
                player["inventory"].append(item)


    # Xóa item.
    if "remove_items" in option:
        for item in option["remove_items"]:
            if item in player["inventory"]:
                player["inventory"].remove(item)
                show_popup(screen, f"Bạn đã mất một {item}.")

def check_requirements(option, player):
    requirements = option.get("requirement", {})
    
    for key, value in requirements.items():
        if key == "items":
            # Nếu yêu cầu là item, kiểm tra item của player.
            if isinstance(value, list):
                if not any(item in player["inventory"] for item in value):
                    return False, key  
            else:
                if value not in player["inventory"]:
                    return False, key  
                
        elif key == "role":
            # Nếu yêu cầu là role, kiểm tra role của player.
            if isinstance(value, list):
                if player.get("role") not in value:
                    return False, key 
            else:
                if player.get("role", '') != value:
                    return False, key 
        else:
            # Nếu không, kiểm tra chỉ số.
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
