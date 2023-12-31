import os
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon

def create_image_buttons(folder_path, icon_info, button_layout, click_callback):
    files = os.listdir(folder_path)
    image_files = [os.path.join(root, os.path.splitext(file)[0]) for root, dirs, files in os.walk(folder_path ) 
               for file in files 
               if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]


    icon_width, icon_height, icon_column = icon_info

    # 이미지 파일 이름을 갖는 버튼 생성 및 추가
    row, col = 0, 0
    for image_file in image_files:
        button = QPushButton(button_layout.parentWidget())  # 부모 위젯을 전달하여 같은 레이아웃에 속하게 함
        
        # 버튼에 아이콘 추가
        icon_path = os.path.join(os.path.dirname(image_file), os.path.basename(image_file))
        button.setIcon(QIcon(icon_path))
        
        # 버튼 크기 조절
        button.setFixedSize(icon_width, icon_height)  # 가로 100, 세로 100 크기로 조절
        
        # 아이콘 크기 조절
        button.setIconSize(button.size())
        
        button.clicked.connect(lambda _, path=image_file: click_callback(path))

        button_layout.addWidget(button, row, col)
        
        col += 1
        if col == icon_column:
            row += 1
            col = 0
