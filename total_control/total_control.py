import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea
from PyQt5 import uic
from image_button_utils import create_image_buttons

# Load the UI files
form_class = uic.loadUiType("total_control.ui")[0]

icon_path = "./icon"
mods_path = "C:/Users/Karina/Documents/Work/genshine/Genshin Mods/3dmigoto-GIMI-for-development/3dmigoto/Mods/UnTracked"

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.button_grid_layout = QGridLayout()

        layout.addLayout(self.button_grid_layout)

        # 이미 기본 레이아웃이 설정되어 있으므로 레이아웃을 변경하기 위해선 setCentralWidget을 사용해야 함
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 간격 조절
        self.button_grid_layout.setSpacing(5)  # 픽셀 단위로 간격을 설정
        self.button_grid_layout.setHorizontalSpacing(5)  # 픽셀 단위로 좌우 간격을 설정

        create_image_buttons(icon_path, (100, 100, 10), self.button_grid_layout, self.iconClicked)

        self.setWindowTitle('Total Control')
        self.show()

    def iconClicked(self, image_path):
        image_name = os.path.basename(image_path)
        print(f"{image_name} Clicked")
        if os.path.exists(f"{mods_path}/{image_name}"):
            self.new_window = SubWindow(image_name)
            self.new_window.show()


class SubWindow(QMainWindow, form_class):
    def __init__(self, image_name):
        super().__init__()
        self.setupUi(self)

        print(f"{image_name} Open")
        
        self.image_name = image_name
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.button_grid_layout = QGridLayout()

        update_button = QPushButton('이미지 파일 목록 업데이트', self)
        update_button.clicked.connect(lambda: self.update_image_buttons())
        layout.addWidget(update_button)

        layout.addLayout(self.button_grid_layout)
        
        # 스크롤 가능한 영역을 제공하는 QScrollArea 생성
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 내용 크기에 따라 스크롤 영역 크기 조절

        # 스크롤할 내용을 담을 위젯 생성
        scroll_content_widget = QWidget(self)
        scroll_area.setWidget(scroll_content_widget)

        self.button_grid_layout = QGridLayout(scroll_content_widget)

        layout.addWidget(scroll_area)

        # 이미 기본 레이아웃이 설정되어 있으므로 레이아웃을 변경하기 위해선 setCentralWidget을 사용해야 함
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 간격 조절
        self.button_grid_layout.setSpacing(5)  # 픽셀 단위로 간격을 설정
        self.button_grid_layout.setHorizontalSpacing(5)  # 픽셀 단위로 좌우 간격을 설정

        self.update_image_buttons()

        self.setWindowTitle('이미지 파일 버튼 목록')
        self.show()
        
    def update_image_buttons(self):
        self.clear_image_buttons()
        filePath = f"{mods_path}/{self.image_name}"
        create_image_buttons(filePath, (300, 500, 3), self.button_grid_layout, self.iconClicked)
        
    def clear_image_buttons(self):
        for i in reversed(range(self.button_grid_layout.count())):
            self.button_grid_layout.itemAt(i).widget().setParent(None)
            
    def iconClicked(self, image_path):
        print(f"{image_path} Clicked")
        self.all_disabled_folders()
        self.remove_disabled_prefix(image_path)
            
    def all_disabled_folders(self):
        filePath = f"{mods_path}/{self.image_name}"
        # 지정한 디렉토리의 모든 폴더 목록을 가져옴
        folders = [f for f in os.listdir(filePath) if os.path.isdir(os.path.join(filePath, f))]

        # "DISABLED_"가 없는 폴더에 대해서만 작업 수행
        for folder in folders:
            if not folder.startswith("DISABLED_"):
                original_path = os.path.join(filePath, folder)
                new_folder_name = "DISABLED_" + folder
                new_path = os.path.join(filePath, new_folder_name)

                # 폴더 이름 변경
                os.rename(original_path, new_path)
                print(f'폴더 이름 변경: {folder} -> {new_folder_name}')

    def remove_disabled_prefix(self, image_path):
        default_Path = f"{mods_path}/{self.image_name}"
        # 지정한 디렉토리의 모든 폴더 목록을 가져옴
        folders = [f for f in os.listdir(default_Path) if os.path.isdir(os.path.join(default_Path, f))]
        
        filePath = os.path.dirname(image_path)
        
        for folder in folders:
            compare_path = os.path.join(default_Path, folder)
            if filePath == compare_path.replace("DISABLED_", ""):
                filePath = compare_path
                break

        # 폴더 경로를 나누어서 각 부분을 리스트로 저장
        path_parts = filePath.split(os.path.sep)
        
        # 폴더 이름에 대해 "DISABLED_"를 찾아 ""로 바꿈
        for i, part in enumerate(path_parts):
            if "DISABLED_" in part:
                new_folder_name = part.replace("DISABLED_", "")
                path_parts[i] = new_folder_name

        # 업데이트된 폴더 이름을 포함한 전체 경로 생성
        updated_folder_path = os.path.sep.join(path_parts)

        # 폴더 이름 변경
        try:
            os.rename(filePath, updated_folder_path)
        except Exception as e:
            print(f"오류 발생: {e}")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    sys.exit(app.exec_())
