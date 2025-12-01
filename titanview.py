import sys
import os
import mmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QPlainTextEdit, QScrollBar, QFrame, QLineEdit, 
                             QComboBox, QMessageBox, QSlider, QListWidget, 
                             QListWidgetItem, QMenu, QToolButton, QAbstractItemView,
                             QTabWidget, QGraphicsOpacityEffect, QStyleOption)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QEvent, QPoint, QSize, QTimer
from PyQt6.QtGui import (QFont, QColor, QTextCharFormat, QTextCursor, QAction, 
                         QDragEnterEvent, QDropEvent, QIcon, QPalette, QPainter, QBrush)
from PyQt6.QtWidgets import QTextEdit, QStyle

# Styles

STYLES = {
    "Dark": """
        QMainWindow { background-color: #1e1e1e; color: #d4d4d4; }
        QWidget { background-color: #1e1e1e; color: #cccccc; font-family: 'Segoe UI', sans-serif; font-size: 13px; }
        
        QPlainTextEdit { 
            background-color: #1e1e1e; 
            color: #d4d4d4; 
            border: none; 
            padding: 10px; 
            font-family: 'Consolas', 'Cascadia Code', monospace; 
            selection-background-color: #264f78;
        }

        QFrame#SideBar { background-color: #252526; border-right: 1px solid #333333; }
        QFrame#TopBar { background-color: #252526; border-bottom: 1px solid #333333; }
        QFrame#BottomBar { background-color: #007acc; border-top: none; }
        
        QTabWidget::pane { border: 0; }
        QTabBar::tab { background: #2d2d2d; color: #969696; padding: 8px 15px; border: none; }
        QTabBar::tab:selected { background: #1e1e1e; color: #ffffff; font-weight: bold; border-top: 2px solid #007acc; }

        QListWidget { background-color: #252526; border: none; outline: none; }
        QListWidget::item { padding: 4px; border-bottom: 1px solid #2d2d2d; color: #cccccc; }
        QListWidget::item:selected { background-color: #37373d; color: #ffffff; border-left: 2px solid #007acc; }

        /* --- SOLID BUBBLE MENU --- */
        QWidget#FloatMenu { 
            background-color: #252526; 
            border: 1px solid #454545; 
            border-radius: 8px;
        }
        QLineEdit#FloatInput {
            background-color: #1e1e1e;
            border: 1px solid #3c3c3c;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
        }
        QPushButton#FloatBtn {
            background-color: #333333;
            color: #E0E0E0;
            border: 1px solid #3c3c3c;
            padding: 5px 12px;
            font-weight: 600;
            border-radius: 4px;
        }
        QPushButton#FloatBtn:hover {
            background-color: #007ACC;
            color: white;
            border-color: #007ACC;
        }
        /* Vertical Separator in Bubble */
        QFrame#BubbleSep {
            background-color: #444;
            width: 1px;
        }

        /* Standard Inputs */
        QLineEdit, QComboBox { 
            background-color: #3c3c3c; 
            color: #cccccc; 
            border: 1px solid #3c3c3c; 
            padding: 6px; 
            border-radius: 2px; 
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #007acc; background-color: #444444; }

        QPushButton { 
            background-color: #3c3c3c; 
            color: #cccccc;
            border: none; 
            padding: 6px 12px; 
            border-radius: 2px; 
        }
        QPushButton:hover { background-color: #444444; }
        QPushButton:pressed { background-color: #007acc; color: white; }
        
        QPushButton#PrimaryBtn { background-color: #007acc; color: white; font-weight: 600; }
        QPushButton#PrimaryBtn:hover { background-color: #0062a3; }
        
        QPushButton#GhostBtn { background-color: transparent; border: 1px solid #444; }
        QPushButton#GhostBtn:hover { background-color: #333; }
        QPushButton#ManageActive { background-color: #8B0000; color: white; }

        QScrollBar:vertical { background: #1e1e1e; width: 12px; }
        QScrollBar::handle:vertical { background: #424242; border-radius: 0px; min-height: 20px; }
        
        QSlider::groove:horizontal { border: none; height: 4px; background: #3c3c3c; margin: 2px 0; }
        QSlider::handle:horizontal { background: #007acc; width: 10px; height: 10px; margin: -3px 0; border-radius: 5px; }
    """,
    "Light": """
        QMainWindow { background-color: #f8f8f8; color: #333333; }
        QWidget { background-color: #f8f8f8; color: #333333; font-family: 'Segoe UI', sans-serif; font-size: 13px; }
        
        QPlainTextEdit { 
            background-color: #ffffff; 
            color: #222222; 
            border: none; 
            padding: 10px; 
            font-family: 'Consolas', 'Cascadia Code', monospace; 
            selection-background-color: #add6ff;
            selection-color: #000000;
        }

        QFrame#SideBar { background-color: #f3f3f3; border-right: 1px solid #e0e0e0; }
        QFrame#TopBar { background-color: #f3f3f3; border-bottom: 1px solid #e0e0e0; }
        QFrame#BottomBar { background-color: #007acc; border-top: none; }
        
        QTabWidget::pane { border: 0; }
        QTabBar::tab { background: #e6e6e6; color: #555; padding: 8px 15px; border: none; }
        QTabBar::tab:selected { background: #ffffff; color: #000; font-weight: bold; border-top: 2px solid #007acc; }

        QListWidget { background-color: #f3f3f3; border: none; outline: none; }
        QListWidget::item { padding: 4px; border-bottom: 1px solid #e0e0e0; color: #444; }
        QListWidget::item:selected { background-color: #e8e8e8; color: #000; border-left: 2px solid #007acc; }

        /* --- SOLID BUBBLE MENU (Light) --- */
        QWidget#FloatMenu { 
            background-color: #FFFFFF; 
            border: 1px solid #CCCCCC; 
            border-radius: 8px;
        }
        QLineEdit#FloatInput {
            background-color: #F0F0F0;
            border: 1px solid #DDD;
            color: #333;
            padding: 4px 8px;
            border-radius: 4px;
        }
        QPushButton#FloatBtn {
            background-color: #F5F5F5;
            color: #444;
            border: 1px solid #DDD;
            padding: 5px 12px;
            font-weight: 600;
            border-radius: 4px;
        }
        QPushButton#FloatBtn:hover {
            background-color: #E0E0E0;
            color: #000;
            border-color: #CCC;
        }
        QFrame#BubbleSep {
            background-color: #DDD;
            width: 1px;
        }

        QLineEdit, QComboBox { 
            background-color: #ffffff; 
            color: #333333; 
            border: 1px solid #cccccc; 
            padding: 6px; 
            border-radius: 2px; 
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #007acc; background-color: #ffffff; }

        QPushButton { 
            background-color: #ffffff; 
            color: #333333;
            border: 1px solid #cccccc; 
            padding: 6px 12px; 
            border-radius: 2px; 
        }
        QPushButton:hover { background-color: #f0f0f0; border-color: #bbbbbb; }
        QPushButton:pressed { background-color: #e0e0e0; }
        
        QPushButton#PrimaryBtn { background-color: #007acc; color: white; border: none; font-weight: 600; }
        QPushButton#PrimaryBtn:hover { background-color: #0062a3; }
        
        QPushButton#GhostBtn { background-color: transparent; border: 1px solid #ccc; }
        QPushButton#ManageActive { background-color: #d32f2f; color: white; border: none;}

        QScrollBar:vertical { background: #f0f0f0; width: 12px; }
        QScrollBar::handle:vertical { background: #cdcdcd; border-radius: 0px; min-height: 20px; }
        
        QSlider::groove:horizontal { border: none; height: 4px; background: #e0e0e0; margin: 2px 0; }
        QSlider::handle:horizontal { background: #007acc; width: 10px; height: 10px; margin: -3px 0; border-radius: 5px; }
    """
}

# Custom Widgets

class FloatingMenu(QWidget):
    """ Solid, High-Visibility Popup Menu """
    bookmark_clicked = pyqtSignal(str) 
    export_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FloatMenu")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8) 
        layout.setSpacing(8)
        
        # Name Input
        self.name_input = QLineEdit()
        self.name_input.setObjectName("FloatInput")
        self.name_input.setPlaceholderText("Name bookmark...")
        self.name_input.setFixedWidth(130)
        
        # Separator 1
        sep1 = QFrame()
        sep1.setObjectName("BubbleSep")
        sep1.setFrameShape(QFrame.Shape.VLine)
        sep1.setFixedWidth(1)
        sep1.setFixedHeight(22)

        # Bookmark Button
        btn_bk = QPushButton("Save")
        btn_bk.setObjectName("FloatBtn")
        btn_bk.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_bk.clicked.connect(self.on_bookmark)
        
        # Separator 2
        sep2 = QFrame()
        sep2.setObjectName("BubbleSep")
        sep2.setFrameShape(QFrame.Shape.VLine)
        sep2.setFixedWidth(1)
        sep2.setFixedHeight(22)
        
        # Export Button
        btn_ex = QPushButton("Export")
        btn_ex.setObjectName("FloatBtn")
        btn_ex.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ex.clicked.connect(self.export_clicked.emit)
        
        layout.addWidget(self.name_input)
        layout.addWidget(sep1)
        layout.addWidget(btn_bk)
        layout.addWidget(sep2)
        layout.addWidget(btn_ex)
        
        # Deep Drop Shadow
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 90))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        text_color = self.palette().color(QPalette.ColorRole.WindowText)
        if text_color.lightness() < 128: 
            p.setBrush(QBrush(QColor(255, 255, 255, 250))) 
            p.setPen(QColor(200, 200, 200))
        else:
            p.setBrush(QBrush(QColor(37, 37, 38, 250))) 
            p.setPen(QColor(70, 70, 70))
            
        p.drawRoundedRect(self.rect().adjusted(1,1,-1,-1), 8, 8)

    def on_bookmark(self):
        name = self.name_input.text().strip()
        self.bookmark_clicked.emit(name if name else "Untitled")
        self.name_input.clear()

class BookmarkItemWidget(QWidget):
    """ Custom List Row """
    up_clicked = pyqtSignal()
    down_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setObjectName("BookmarkItem")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        icon_label = QLabel("🔖")
        self.label = QLabel(text)
        self.label.setObjectName("BkLabel")
        layout.addWidget(icon_label)
        layout.addWidget(self.label)
        
        layout.addStretch()
        
        # Controls
        btn_up = QToolButton()
        btn_up.setText("▲")
        btn_up.setToolTip("Move Up")
        btn_up.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_up.clicked.connect(self.up_clicked.emit)
        
        btn_down = QToolButton()
        btn_down.setText("▼")
        btn_down.setToolTip("Move Down")
        btn_down.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_down.clicked.connect(self.down_clicked.emit)
        
        btn_del = QToolButton()
        btn_del.setText("✕")
        btn_del.setObjectName("DelBtn")
        btn_del.setToolTip("Delete")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.clicked.connect(self.delete_clicked.emit)
        
        layout.addWidget(btn_up)
        layout.addWidget(btn_down)
        layout.addWidget(btn_del)

# Worker Threads

class SearchWorker(QThread):
    found = pyqtSignal(int)
    not_found = pyqtSignal()
    
    def __init__(self, file_path, search_term, start_pos, direction="forward", encoding="utf-8"):
        super().__init__()
        self.file_path = file_path
        try:
            self.search_term = search_term.encode(encoding)
        except:
            self.search_term = search_term.encode('utf-8') 
            
        self.start_pos = start_pos
        self.direction = direction

    def run(self):
        if not os.path.exists(self.file_path):
            self.not_found.emit()
            return
        try:
            with open(self.file_path, 'r+b') as f:
                mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                if self.direction == "forward":
                    search_start = min(self.start_pos + 1, mmapped_file.size())
                    mmapped_file.seek(search_start)
                    loc = mmapped_file.find(self.search_term)
                else:
                    scan_end = max(0, self.start_pos)
                    chunk_scan_size = 50 * 1024 * 1024 
                    scan_start = max(0, scan_end - chunk_scan_size)
                    loc = mmapped_file.rfind(self.search_term, scan_start, scan_end)

                if loc != -1: self.found.emit(loc)
                else: self.not_found.emit()
                mmapped_file.close()
        except Exception as e:
            print(f"Search Worker Error: {e}")
            self.not_found.emit()

class FindAllWorker(QThread):
    match_found = pyqtSignal(int)
    finished_scan = pyqtSignal(int) 
    
    def __init__(self, file_path, search_term, encoding="utf-8"):
        super().__init__()
        self.file_path = file_path
        self.is_running = True
        
        if search_term:
            try:
                self.search_term = search_term.encode(encoding)
            except:
                self.search_term = search_term.encode('utf-8')
        else:
            self.search_term = None

    def run(self):
        if not os.path.exists(self.file_path) or not self.search_term:
            self.finished_scan.emit(0)
            return

        count = 0
        try:
            with open(self.file_path, 'r+b') as f:
                mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                pos = 0
                while self.is_running:
                    loc = mmapped_file.find(self.search_term, pos)
                    if loc == -1: break
                    self.match_found.emit(loc)
                    count += 1
                    pos = loc + 1
                    if count > 2000: break 
                mmapped_file.close()
        except Exception as e:
            print(e)
        self.finished_scan.emit(count)
        
    def stop(self):
        self.is_running = False

# Main App

class TitanViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TitanView v4.9 | Professional Edition")
        self.resize(1360, 850)
        self.setAcceptDrops(True)
        
        # State
        self.file_path = None
        self.file_size = 0
        self.chunk_size = 50 * 1024 
        self.current_pos = 0 
        self.mmapped_file = None
        self.file_handle = None
        self.current_theme = "Dark"
        self.current_encoding = "utf-8"
        self.is_manage_mode = False
        self.is_navigating_programmatically = False
        
        self.init_ui()
        self.apply_theme("Dark")
        
        # Floating Menu
        self.float_menu = FloatingMenu(self)
        self.float_menu.hide()
        self.float_menu.bookmark_clicked.connect(self.add_bookmark_from_selection_with_name)
        self.float_menu.export_clicked.connect(self.export_selection)
        
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("SideBar")
        sidebar.setFixedWidth(300)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(15, 20, 15, 20)
        
        # Header
        title = QLabel("TITAN VIEW")
        title.setStyleSheet("font-weight: 900; font-size: 20px; color: #007ACC; letter-spacing: 1.5px;")
        sb_layout.addWidget(title)
        sb_layout.addSpacing(20)
        
        self.btn_open = QPushButton("📂 Open File")
        self.btn_open.setObjectName("PrimaryBtn")
        self.btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open.clicked.connect(self.open_file_dialog)
        sb_layout.addWidget(self.btn_open)
        
        sb_layout.addSpacing(15)
        
        # Tabs
        self.sidebar_tabs = QTabWidget()
        
        # Tab 1 - Bookmarks
        tab_bk = QWidget()
        bk_layout = QVBoxLayout(tab_bk)
        bk_layout.setContentsMargins(0, 10, 0, 0)
        
        bk_toolbar = QHBoxLayout()
        self.btn_manage = QPushButton("Manage")
        self.btn_manage.setObjectName("GhostBtn")
        self.btn_manage.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_manage.clicked.connect(self.toggle_manage_mode)
        bk_toolbar.addWidget(QLabel("Saved Locations"))
        bk_toolbar.addStretch()
        bk_toolbar.addWidget(self.btn_manage)
        bk_layout.addLayout(bk_toolbar)
        
        self.bookmark_list = QListWidget()
        self.bookmark_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.bookmark_list.itemClicked.connect(self.on_bookmark_click)
        bk_layout.addWidget(self.bookmark_list)
        
        self.btn_bulk_delete = QPushButton("🗑️ Delete Selected")
        self.btn_bulk_delete.setObjectName("ManageActive")
        self.btn_bulk_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_bulk_delete.clicked.connect(self.delete_selected_bookmarks)
        self.btn_bulk_delete.hide()
        bk_layout.addWidget(self.btn_bulk_delete)
        
        self.sidebar_tabs.addTab(tab_bk, "🔖 Bookmarks")
        
        # Tab 2 - History
        tab_search = QWidget()
        sr_layout = QVBoxLayout(tab_search)
        sr_layout.setContentsMargins(0, 10, 0, 0)
        
        sr_toolbar = QHBoxLayout()
        self.btn_find_all = QPushButton("Scan All")
        self.btn_find_all.setObjectName("GhostBtn")
        self.btn_find_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_find_all.clicked.connect(self.find_all_matches)
        sr_toolbar.addWidget(QLabel("Search Results"))
        sr_toolbar.addStretch()
        sr_toolbar.addWidget(self.btn_find_all)
        sr_layout.addLayout(sr_toolbar)
        
        self.search_results_list = QListWidget()
        self.search_results_list.itemClicked.connect(self.on_search_result_click)
        sr_layout.addWidget(self.search_results_list)
        
        self.sidebar_tabs.addTab(tab_search, "🔎 Results")
        
        sb_layout.addWidget(self.sidebar_tabs)
        
        sb_layout.addSpacing(10)
        sb_layout.addWidget(QLabel("Text Encoding"))
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["utf-8", "latin-1", "ascii", "cp1252", "utf-16"])
        self.encoding_combo.currentTextChanged.connect(self.change_encoding)
        sb_layout.addWidget(self.encoding_combo)

        sb_layout.addStretch()
        self.lbl_file_info = QLabel("No File Loaded")
        self.lbl_file_info.setWordWrap(True)
        self.lbl_file_info.setStyleSheet("color: #777; font-size: 11px;")
        sb_layout.addWidget(self.lbl_file_info)

        main_layout.addWidget(sidebar)

        content_area = QWidget()
        ca_layout = QVBoxLayout(content_area)
        ca_layout.setContentsMargins(0, 0, 0, 0)
        ca_layout.setSpacing(0)

        # Navigation Bar
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_bar.setFixedHeight(60)
        tb_layout = QHBoxLayout(top_bar)
        tb_layout.setContentsMargins(20, 0, 20, 0)
        tb_layout.setSpacing(15)
        
        self.timeline = QSlider(Qt.Orientation.Horizontal)
        self.timeline.setRange(0, 10000)
        self.timeline.setEnabled(False)
        self.timeline.setCursor(Qt.CursorShape.PointingHandCursor)
        self.timeline.sliderReleased.connect(self.on_timeline_release)
        self.timeline.sliderMoved.connect(self.on_timeline_move)
        tb_layout.addWidget(self.timeline)
        
        self.lbl_pos_pct = QLabel("0%")
        self.lbl_pos_pct.setFixedWidth(50)
        self.lbl_pos_pct.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        tb_layout.addWidget(self.lbl_pos_pct)
        
        # Vertical Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet("color: #444;")
        tb_layout.addWidget(sep)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search document...")
        self.search_input.setFixedWidth(240)
        self.search_input.returnPressed.connect(self.smart_search_next)
        tb_layout.addWidget(self.search_input)
        
        self.btn_search_prev = QPushButton("⬆")
        self.btn_search_prev.setFixedWidth(30)
        self.btn_search_prev.setToolTip("Previous Match")
        self.btn_search_prev.clicked.connect(self.search_prev)
        tb_layout.addWidget(self.btn_search_prev)

        self.btn_search_next = QPushButton("⬇")
        self.btn_search_next.setFixedWidth(30)
        self.btn_search_next.setToolTip("Next Match")
        self.btn_search_next.clicked.connect(self.smart_search_next)
        tb_layout.addWidget(self.btn_search_next)
        
        self.theme_btn = QPushButton("🌙/☀️")
        self.theme_btn.setFixedWidth(50)
        self.theme_btn.clicked.connect(self.toggle_theme)
        tb_layout.addWidget(self.theme_btn)
        
        ca_layout.addWidget(top_bar)

        # Editor
        self.text_editor = QPlainTextEdit()
        self.text_editor.setReadOnly(True)
        self.text_editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.text_editor.verticalScrollBar().valueChanged.connect(self.check_scroll)
        self.text_editor.selectionChanged.connect(self.on_text_selection)
        self.text_editor.cursorPositionChanged.connect(self.on_cursor_position_changed)
        ca_layout.addWidget(self.text_editor)

        # Status Bar
        bottom_bar = QFrame()
        bottom_bar.setObjectName("BottomBar")
        bottom_bar.setFixedHeight(30)
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(15, 0, 15, 0)
        
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setStyleSheet("color: white; font-weight: 600;")
        bb_layout.addWidget(self.lbl_status)
        
        bb_layout.addStretch()
        
        self.lbl_dev = QLabel("Developed by Mutahar")
        self.lbl_dev.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 10px;") 
        bb_layout.addWidget(self.lbl_dev)
        
        bb_layout.addSpacing(15)
        
        self.lbl_hex_pos = QLabel("Offset: 0x0")
        self.lbl_hex_pos.setStyleSheet("color: white; font-family: 'Consolas'; opacity: 0.8;")
        bb_layout.addWidget(self.lbl_hex_pos)

        ca_layout.addWidget(bottom_bar)
        main_layout.addWidget(content_area)

    # UI/ Theme
    def apply_theme(self, name):
        self.setStyleSheet(STYLES[name])
        if self.search_input.text(): self.smart_search_next() 

    def toggle_theme(self):
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        self.apply_theme(self.current_theme)

    # Highlight and Menu Logic
    def on_text_selection(self):
        cursor = self.text_editor.textCursor()
        if not cursor.hasSelection():
            self.float_menu.hide()
            return
        
        rect = self.text_editor.cursorRect(cursor)
        global_pos = self.text_editor.viewport().mapToGlobal(rect.topRight())
        menu_pos = global_pos + QPoint(15, -60) 
        
        self.float_menu.move(menu_pos)
        self.float_menu.show()
        self.float_menu.raise_()
        self.float_menu.name_input.setFocus() 

    def on_cursor_position_changed(self):
        if not self.is_navigating_programmatically:
            if self.text_editor.extraSelections():
                self.text_editor.setExtraSelections([])

    # Bookmark Logic
    def add_bookmark_from_selection_with_name(self, custom_name):
        self.float_menu.hide()
        if not self.file_path: return
        
        cursor = self.text_editor.textCursor()
        if not cursor.hasSelection(): return
        
        sel_start = cursor.selectionStart()
        all_text = self.text_editor.toPlainText()
        prefix_text = all_text[:sel_start]
        
        try:
            prefix_bytes = len(prefix_text.encode(self.current_encoding))
            abs_byte_start = self.current_pos + prefix_bytes 
            
            selected_str = cursor.selectedText().replace('\u2029', '\n')
            byte_len = len(selected_str.encode(self.current_encoding))
            
            label = custom_name if custom_name != "Untitled" else f"Bk @ {hex(abs_byte_start)}"
            
            bk_data = {
                "offset": abs_byte_start,
                "length": byte_len,
                "label": label
            }
            
            self.create_bookmark_item(bk_data)
            self.lbl_status.setText(f"Bookmarked: {label}")
            
        except Exception as e:
            self.lbl_status.setText(f"Bookmark Error: {e}")

    def create_bookmark_item(self, data):
        item = QListWidgetItem(self.bookmark_list)
        item.setSizeHint(QSize(0, 42))
        item.setData(Qt.ItemDataRole.UserRole, data)
        
        widget = BookmarkItemWidget(data['label'])
        widget.up_clicked.connect(lambda: self.move_bookmark(item, -1))
        widget.down_clicked.connect(lambda: self.move_bookmark(item, 1))
        widget.delete_clicked.connect(lambda: self.delete_single_bookmark(item))
        
        self.bookmark_list.setItemWidget(item, widget)

    def on_bookmark_click(self, item):
        if self.is_manage_mode: return
        data = item.data(Qt.ItemDataRole.UserRole)
        self.jump_and_highlight(data['offset'], data['length'], highlight_row=False)

    def jump_and_highlight(self, offset, length=0, highlight_row=False):
        self.is_navigating_programmatically = True
        
        load_start = max(0, offset - 500)
        self.load_chunk(load_start, align_to_newline=True)
        
        if self.current_pos > offset:
            load_start = max(0, offset - 100)
            self.load_chunk(load_start, align_to_newline=False)
        
        relative_byte_offset = offset - self.current_pos
        
        try:
            self.mmapped_file.seek(self.current_pos)
            gap_bytes = self.mmapped_file.read(relative_byte_offset)
            char_offset = len(gap_bytes.decode(self.current_encoding, errors='replace'))
            
            char_length = 0
            if length > 0 and not highlight_row:
                self.mmapped_file.seek(offset)
                target_bytes = self.mmapped_file.read(length)
                char_length = len(target_bytes.decode(self.current_encoding, errors='replace'))
            
            cursor = QTextCursor(self.text_editor.document())
            cursor.setPosition(char_offset)
            
            if highlight_row:
                cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            elif char_length > 0:
                cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, char_length)
            else:
                cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
            
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#00BCD4") if self.current_theme == "Dark" else QColor("#007ACC")) 
            selection.format.setForeground(QColor("white"))
            selection.cursor = cursor
            
            self.text_editor.setExtraSelections([selection])
            self.text_editor.setTextCursor(cursor)
            self.text_editor.centerCursor()
            
        except Exception as e:
            print(f"Jump Error: {e}")
            
        QTimer.singleShot(150, lambda: setattr(self, 'is_navigating_programmatically', False))

    def find_all_matches(self):
        term = self.search_input.text()
        
        if not self.file_path: 
            return
        
        if not term or len(term.strip()) == 0:
            QMessageBox.warning(self, "Search Error", "Please enter text in the top search bar to scan.")
            return
        
        self.search_results_list.clear()
        self.btn_find_all.setText("Scanning...")
        self.btn_find_all.setEnabled(False)
        self.lbl_status.setText("Finding all matches (Background)...")
        
        self.fa_worker = FindAllWorker(self.file_path, term, self.current_encoding)
        self.fa_worker.match_found.connect(self.add_search_result)
        self.fa_worker.finished_scan.connect(self.on_scan_finished)
        self.fa_worker.start()

    def add_search_result(self, offset):
        item = QListWidgetItem(f"Match @ {hex(offset)}")
        item.setData(Qt.ItemDataRole.UserRole, offset)
        self.search_results_list.addItem(item)

    def on_search_result_click(self, item):
        offset = item.data(Qt.ItemDataRole.UserRole)
        self.jump_and_highlight(offset, length=0, highlight_row=True)

    def on_scan_finished(self, count):
        self.btn_find_all.setText("Scan All")
        self.btn_find_all.setEnabled(True)
        self.lbl_status.setText(f"Scan complete. Found {count} matches.")

    # Bookmark Management
    def toggle_manage_mode(self):
        self.is_manage_mode = not self.is_manage_mode
        if self.is_manage_mode:
            self.btn_manage.setText("Done")
            self.btn_manage.setStyleSheet("background-color: #C42B1C; color: white;")
            self.bookmark_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.btn_bulk_delete.show()
        else:
            self.btn_manage.setText("Manage")
            self.btn_manage.setStyleSheet("")
            self.bookmark_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.bookmark_list.clearSelection()
            self.btn_bulk_delete.hide()

    def move_bookmark(self, item, direction):
        row = self.bookmark_list.row(item)
        new_row = row + direction
        if 0 <= new_row < self.bookmark_list.count():
            data = item.data(Qt.ItemDataRole.UserRole)
            self.bookmark_list.takeItem(row)
            new_item = QListWidgetItem()
            new_item.setData(Qt.ItemDataRole.UserRole, data)
            new_item.setSizeHint(QSize(0, 42))
            self.bookmark_list.insertItem(new_row, new_item)
            
            widget = BookmarkItemWidget(data['label'])
            widget.up_clicked.connect(lambda: self.move_bookmark(new_item, -1))
            widget.down_clicked.connect(lambda: self.move_bookmark(new_item, 1))
            widget.delete_clicked.connect(lambda: self.delete_single_bookmark(new_item))
            self.bookmark_list.setItemWidget(new_item, widget)
            self.bookmark_list.setCurrentRow(new_row)

    def delete_single_bookmark(self, item):
        row = self.bookmark_list.row(item)
        self.bookmark_list.takeItem(row)

    def delete_selected_bookmarks(self):
        items = self.bookmark_list.selectedItems()
        for item in items:
            row = self.bookmark_list.row(item)
            self.bookmark_list.takeItem(row)
        self.lbl_status.setText(f"Deleted {len(items)} bookmarks")

    # Files and Utils
    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Large File")
        if path: self.load_file(path)

    def load_file(self, path):
        if self.mmapped_file: self.mmapped_file.close()
        if self.file_handle: self.file_handle.close()
        try:
            self.file_path = path
            self.file_size = os.path.getsize(path)
            self.file_handle = open(path, "r+b")
            self.mmapped_file = mmap.mmap(self.file_handle.fileno(), 0, access=mmap.ACCESS_READ)
            self.lbl_file_info.setText(f"{os.path.basename(path)}\n{self.format_size(self.file_size)}")
            self.timeline.setEnabled(True)
            self.timeline.setValue(0)
            self.bookmark_list.clear()
            self.search_results_list.clear()
            self.load_chunk(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_chunk(self, byte_offset, align_to_newline=True):
        if not self.mmapped_file: return
        self.is_navigating_programmatically = True
        self.text_editor.setExtraSelections([])
        
        byte_offset = max(0, min(byte_offset, self.file_size - self.chunk_size))
        self.mmapped_file.seek(byte_offset)
        
        if align_to_newline and byte_offset != 0:
            self.mmapped_file.readline() 
            byte_offset = self.mmapped_file.tell()
            
        self.current_pos = byte_offset
        data = self.mmapped_file.read(self.chunk_size)
        try:
            text = data.decode(self.current_encoding)
        except:
            text = data.decode('latin-1', errors='replace')
            
        self.text_editor.setPlainText(text)
        self.text_editor.verticalScrollBar().setValue(0)
        
        if not self.timeline.isSliderDown():
            val = int((self.current_pos / self.file_size) * 10000)
            self.timeline.blockSignals(True)
            self.timeline.setValue(val)
            self.lbl_pos_pct.setText(f"{int(val/100)}%")
            self.timeline.blockSignals(False)
            
        self.lbl_hex_pos.setText(f"Offset: {hex(byte_offset)}")
        self.is_navigating_programmatically = False

    def smart_search_next(self):
        term = self.search_input.text()
        if not term: return
        if self.text_editor.find(term):
            self.lbl_status.setText("Match found in View")
            return
        self.lbl_status.setText("Scanning Disk...")
        start_scan = self.current_pos + self.chunk_size
        self.worker = SearchWorker(self.file_path, term, start_scan, "forward", self.current_encoding)
        self.worker.found.connect(self.on_search_found)
        self.worker.not_found.connect(lambda: self.lbl_status.setText("Not found"))
        self.worker.start()

    def search_prev(self):
        term = self.search_input.text()
        if not term: return
        if self.text_editor.find(term, QTextCursor.FindFlag.FindBackward):
            self.lbl_status.setText("Match found (Prev)")
            return
        self.worker = SearchWorker(self.file_path, term, self.current_pos, "backward", self.current_encoding)
        self.worker.found.connect(self.on_search_found)
        self.worker.start()

    def on_search_found(self, loc):
        term = self.search_input.text()
        term_bytes = len(term.encode(self.current_encoding))
        self.jump_and_highlight(loc, term_bytes, highlight_row=False)

    def check_scroll(self, value):
        if value >= self.text_editor.verticalScrollBar().maximum() - 5:
            if self.current_pos + self.chunk_size < self.file_size:
                next_pos = int(self.current_pos + (self.chunk_size * 0.9))
                self.load_chunk(next_pos)

    def on_timeline_move(self, val):
        pct = val / 10000
        self.lbl_pos_pct.setText(f"{int(pct*100)}%")
    def on_timeline_release(self):
        val = self.timeline.value()
        target = int((val / 10000) * self.file_size)
        self.load_chunk(target)
    def change_encoding(self, enc):
        self.current_encoding = enc
        if self.file_path: self.load_chunk(self.current_pos)
    def export_selection(self):
        self.float_menu.hide()
        cursor = self.text_editor.textCursor()
        if not cursor.hasSelection(): return
        path, _ = QFileDialog.getSaveFileName(self, "Save Selection", "snippet.txt")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(cursor.selectedText().replace('\u2029', '\n'))
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024: return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()
    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files: self.load_file(files[0])
    def closeEvent(self, event):
        if self.mmapped_file: self.mmapped_file.close()
        if self.file_handle: self.file_handle.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TitanViewer()
    viewer.show()
    sys.exit(app.exec())
