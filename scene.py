scenes = [
    # Scene 1:
     {
        "text": ("Những năm năm mươi trước Kỷ Định ranh, thời kỳ tiền lập quốc... #Thời kỳ mà những cỗ lò rèn đầy ắp than hồng vẫn bền bỉ tiếp sức cho ngọn lửa chiến tranh. #Thời kỳ mà những cỗ lò rèn đầy ắp than hồng vẫn bền bỉ tiếp sức cho ngọn lửa chiến tranh. #Thời kỳ mà hòa bình chỉ là một phương ngữ tại các vùng địa cực xa xôi. #Thời kỳ mà hạnh phúc chỉ là giấc một mộng hão huyền. #Thời kỳ mà vững mạnh chỉ là những mảnh kí ức khi hồi tưởng về một thời kỳ xưa cũ. #Lục địa Custandel, vùng đất bị các vị thần ruồng bỏ, luôn đắm chìm trong những cuộc tắm máu chẳng biết đến ngày mai... #Rong rủi phi ngựa băng qua khu rừng dưới chân dãy núi Stoughmagne. Âm thanh xào xạc của cơn gió đêm như đang chào đón một linh hồn khác biệt đặt những bước đầu tiên đến vùng đất người ta hay gọi là Grimhold...#Đó là bạn... Bạn đến đây để..."),
        "options": [
            {
                "text": "Tiêu diệt toàn bộ các tông đồ quỷ dữ dưới tư cách là một Sinner - Ma pháp sư quyền năng phục vụ Đế chế...",
                "attributes": {
                    "role": "Sinner",
                    "armor": 1,
                    "strength": 3,
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
                    "armor": 2,
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
                    "armor": 4,
                    "strength": 4,
                    "magic": False,
                    "will": 'Khao khát.',
                    "coin": 20
                }, "next_scene": 1
            },
            {
                "text": "Tìm kiếm sức mạnh ở những con quỷ để thay đổi số phận... Tôi là một tồng đồ...",
                "attributes": {
                    "role": "Demon Believer",
                    "armor": 2,
                    "strength": 2,
                    "magic": True,
                    "magical-number-cast": 3,
                    "will": 'Học hỏi quỷ thuật.',
                    "coin": 5
                }, "next_scene": 1
            }
        ]
    },
    {
        "text": ("Ngồi trên lưng chú ngựa Roach, bạn chậm rãi tiến về phía trước trên mặt đất gồ ghề. Những thảm thực vật xanh tươi ở hai bên cánh rừng đang âm thầm vươn mình xóa bỏ những dấu vết cuối cùng của con đường mòn cũ kỹ. Ánh trăng sáng thấp thoáng sau những tán cây rậm, tạo thành những khoảng sáng tối đan xen như một màn kịch bí ẩn diễn ra giữa đêm đen. #Dưới bầu trời đêm đen đặc, dãy núi xa xa hiện lên như những bóng đen u ám, khổng lồ, nuốt chửng lấy bầu trời sao thưa thớt. Ánh trăng bạc vắt ngang qua đỉnh núi, lấp ló sau cạnh biển mây trôi lững lờ.#Ở Lorathern, đặc biệt là Vương đô, chuyện đi đi lại lại dưới ánh trăng mờ chưa bao giờ là điều kỳ lạ... Bạn nhớ lại vô số lần bản thân đã từng dành cả đêm chỉ để đi vòng quanh khắp khu phố thị. #Tuy nhiên... Đây là Northern...#Dù khu rừng dường như chìm vào trong tĩnh lặng, nhưng đôi tai của bạn, đôi tai của một kẻ đã sống đủ lâu để có thể mường tượng được hàng nghìn cách chết của bản thân qua mỗi giây, mỗi phút. Bạn sẽ nhận ra nơi này không hoàn toàn yên ắng. Tiếng gió rít khe khẽ luồn qua những tán lá, tiếng kêu văng vẳng của một loài sinh vật xa lạ khiến không gian thêm phần rùng rợn. Có thứ gì đó đang ẩn nấp trong bóng tối... #Bạn ngay lập tức kiểm tra vũ khí của mình..."),
        "options": [
            {
                "text": "Tôi mang theo một thanh trường kiếm và một tấm khiên gỗ.",
                "requirement": {"role": ["Sinner","Mercenary"]},
                "items": ["Trường kiếm", "Khiên gỗ"],
                "sateless": "Tôi không đủ giàu có để sở hữu một thanh trường kiếm và một tấm khiên gỗ.",
                "next_scene": 2,
            },
            {
                "text": "Xạ kích là sở trường của tôi, tôi mang theo một cây nỏ và một bó mũi tên, cùng cây chủy thủ sau hông.",
                 "requirement": {"role": ["Sinner","Mercenary"]},
                "items": ["Nỏ", "Chủy thủ", "Bó tên"],
                "effect": {"arrow": 5 },
                "sateless": "Tôi không thể sử dụng nỏ và chủy thủ...",
                "next_scene": 2,
            },
            {
                "text": "Một cây rìu cán dài sẽ tiện dụng hơn ở các chuyến đi xa... và một cây dao nhỏ.",
                "requirement": {"role": ["Mercenary","Wanderer"]},
                "items": ["Rìu cán dài", "Cây dao nhỏ"],
                "sateless": "Tại sao tôi phải mang theo rìu?",
                "next_scene": 2,
            },
            {
                "text": "Chỉ cần sức mạnh ma pháp của tôi là đủ...",
                "requirement": {"role": ["Sinner","Demon Believer"]},
                "sateless": "Tôi không thể sử dụng ma pháp.",
                "next_scene": 2,
            }
        ]
    },
]