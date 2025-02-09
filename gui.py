# Some Bugs Available
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                             QLabel, QPushButton, QSystemTrayIcon, QMenu,
                             QAction, QMessageBox, QScrollArea)
from PyQt5.QtGui import QIcon, QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from scripts.isSocialMedia import isSocialMedia
from scripts.updateJSON import update_json
import json
from datetime import datetime

class CalendarWidget(QWidget):
    def __init__(self, date_colors):
        super().__init__()
        self.date_colors = date_colors
        self.initUI()
        
    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(2)
        self.layout.setVerticalSpacing(2)
        
        # Add day headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold; color: #666;")
            self.layout.addWidget(label, 0, i)
            
        self.update_calendar()
        self.setLayout(self.layout)
        
    def update_calendar(self):
        # Clear existing widgets
        for i in reversed(range(self.layout.count())): 
            if i >= 7:  # Skip headers
                self.layout.itemAt(i).widget().deleteLater()
                
        # Add dates
        row, col = 1, 0
        for date_str in sorted(self.date_colors.keys()):
            date = datetime.strptime(date_str, "%Y-%m-%d")
            day = date.day
            color = QColor(231, 76, 60) if self.date_colors[date_str] else QColor(46, 204, 113)
            
            day_widget = DayWidget(day, color)
            self.layout.addWidget(day_widget, row, col)
            
            col += 1
            if col > 6:
                col = 0
                row += 1

class DayWidget(QWidget):
    def __init__(self, day, color):
        super().__init__()
        self.day = day
        self.color = color
        self.setFixedSize(40, 40)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background circle
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(5, 5, 30, 30)
        
        # Draw day number
        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial', 10))
        painter.drawText(self.rect(), Qt.AlignCenter, str(self.day))

class MonitorThread(QThread):
    update_signal = pyqtSignal(bool)
    
    def __init__(self, social_media_list, days_file):
        super().__init__()
        self.social_media_list = social_media_list
        self.days_file = days_file
        self.running = True
        
    def run(self):
        while self.running:
            is_active = isSocialMedia(self.social_media_list)
            update_json(self.days_file, is_active)
            self.update_signal.emit(is_active)
            self.msleep(1000)
            
    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self, days_file):
        super().__init__()
        self.days_file = days_file
        self.initUI()
        self.load_data()
        
        # Setup monitoring thread
        self.monitor_thread = MonitorThread(["Facebook", "Youtube"], days_file)
        self.monitor_thread.update_signal.connect(self.update_status)
        self.monitor_thread.start()

        self.hide()
        
    def initUI(self):
        self.setWindowTitle('Social Media Tracker')
        self.setWindowIcon(QIcon('./icon/icon.png'))
        self.setGeometry(100, 100, 800, 600)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout
        main_layout = QGridLayout(central_widget)
        
        # Status Label
        self.status_label = QLabel("Monitoring Social Media Usage...")
        self.status_label.setStyleSheet("font-size: 16px; color: #333;")
        main_layout.addWidget(self.status_label, 0, 0)
        
        # Calendar Scroll Area
        scroll = QScrollArea()
        self.calendar_widget = CalendarWidget({})
        scroll.setWidget(self.calendar_widget)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll, 1, 0)
        
        # Buttons
        btn_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        
        self.minimize_btn = QPushButton("Minimize to Tray")
        self.minimize_btn.setStyleSheet(btn_style)
        self.minimize_btn.clicked.connect(self.hide)
        main_layout.addWidget(self.minimize_btn, 2, 0)
        
        # Setup Tray Icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./icon/icon.png'))
        
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.cleanup_and_exit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def load_data(self):
        try:
            with open(self.days_file, 'r') as f:
                self.date_colors = json.load(f)
                self.calendar_widget.date_colors = self.date_colors
                self.calendar_widget.update_calendar()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {str(e)}")
            
    def update_status(self, is_active):
        status_text = "Currently using social media!" if is_active else "No social media detected"
        color = "#e74c3c" if is_active else "#2ecc71"
        self.status_label.setText(f"<span style='color: {color};'>{status_text}</span>")
        self.load_data()
        
    def cleanup_and_exit(self):
        self.monitor_thread.stop()
        self.monitor_thread.wait()
        self.tray_icon.hide()
        QApplication.quit()
        
    def closeEvent(self, event):
        event.ignore()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow("dates.json")
    
    sys.exit(app.exec_())