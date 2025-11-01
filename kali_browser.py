import sys
from PyQt6.QtCore import QUrl, Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit,
    QPushButton, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from urllib.parse import urlparse, urlunparse
import re


class SecureWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        if not self.validate_url(url.toString()):
            return False
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)

    def validate_url(self, url):
        if not url:
            return False
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ['http', 'https', 'file', 'about']:
                return False
            return True
        except Exception:
            return False


class BrowserTab(QWidget):
    url_changed = pyqtSignal(str)
    title_changed = pyqtSignal(str)
    icon_changed = pyqtSignal(object)
    load_started = pyqtSignal()
    load_finished = pyqtSignal(bool)
    load_progress = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.browser = QWebEngineView()
        self.browser.setPage(SecureWebEnginePage(self.browser))
        self.layout.addWidget(self.browser)

        self.browser.urlChanged.connect(lambda url: self.url_changed.emit(url.toString()))
        self.browser.titleChanged.connect(lambda title: self.title_changed.emit(title))
        self.browser.iconChanged.connect(lambda icon: self.icon_changed.emit(icon))
        self.browser.loadStarted.connect(self.load_started.emit)
        self.browser.loadFinished.connect(self.load_finished.emit)
        self.browser.loadProgress.connect(self.load_progress.emit)

    def load_url(self, url):
        url = self.sanitize_url(url)
        if url:
            self.browser.setUrl(QUrl(url))

    def sanitize_url(self, url):
        url = url.strip()
        if not url:
            return None

        if url.startswith('about:') or url.startswith('file://'):
            return url

        if not re.match(r'^[a-zA-Z]+://', url):
            if '.' in url or url == 'localhost':
                url = 'https://' + url
            else:
                url = 'https://www.google.com/search?q=' + url

        try:
            parsed = urlparse(url)
            if parsed.scheme not in ['http', 'https', 'file', 'about']:
                return None
            return url
        except Exception:
            return None

    def back(self):
        self.browser.back()

    def forward(self):
        self.browser.forward()

    def reload(self):
        self.browser.reload()

    def stop(self):
        self.browser.stop()


class KaliBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kali Browser")
        self.setGeometry(100, 100, 1400, 900)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)

        self.setCentralWidget(self.tabs)

        self.create_toolbar()
        self.apply_styles()

        self.add_new_tab(QUrl("https://www.google.com"))

        self.show()

    def create_toolbar(self):
        toolbar = QToolBar("Navigation")
        toolbar.setMovable(False)
        toolbar.setIconSize(toolbar.iconSize() * 1.2)
        self.addToolBar(toolbar)

        back_btn = QAction("◀", self)
        back_btn.setStatusTip("Back")
        back_btn.triggered.connect(lambda: self.current_tab().back())
        toolbar.addAction(back_btn)

        forward_btn = QAction("▶", self)
        forward_btn.setStatusTip("Forward")
        forward_btn.triggered.connect(lambda: self.current_tab().forward())
        toolbar.addAction(forward_btn)

        reload_btn = QAction("↻", self)
        reload_btn.setStatusTip("Reload")
        reload_btn.triggered.connect(lambda: self.current_tab().reload())
        toolbar.addAction(reload_btn)

        home_btn = QAction("⌂", self)
        home_btn.setStatusTip("Home")
        home_btn.triggered.connect(self.navigate_home)
        toolbar.addAction(home_btn)

        toolbar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Enter URL or search...")
        toolbar.addWidget(self.url_bar)

        self.ssl_indicator = QPushButton("🔒")
        self.ssl_indicator.setFlat(True)
        self.ssl_indicator.setMaximumWidth(40)
        self.ssl_indicator.setStyleSheet("QPushButton { border: none; font-size: 16px; }")
        toolbar.addWidget(self.ssl_indicator)

        toolbar.addSeparator()

        new_tab_btn = QAction("+", self)
        new_tab_btn.setStatusTip("New Tab")
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        toolbar.addAction(new_tab_btn)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
                border-bottom: 1px solid #e0e0e0;
                padding: 8px;
                spacing: 5px;
            }
            QToolBar QAction {
                font-size: 18px;
                padding: 8px 12px;
                margin: 0 2px;
            }
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                padding: 8px 16px;
                background-color: #ffffff;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #4285f4;
                background-color: #ffffff;
            }
            QTabWidget::pane {
                border: none;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background: #e8e8e8;
                border: 1px solid #d0d0d0;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                min-width: 150px;
                max-width: 250px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom: 2px solid #4285f4;
            }
            QTabBar::tab:hover {
                background: #f0f0f0;
            }
        """)

    def add_new_tab(self, url=None):
        if url is None:
            url = QUrl("https://www.google.com")

        tab = BrowserTab()
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)

        tab.url_changed.connect(lambda u: self.update_url_bar(u, tab))
        tab.title_changed.connect(lambda t: self.update_tab_title(t, tab))
        tab.load_started.connect(self.on_load_started)
        tab.load_finished.connect(self.on_load_finished)
        tab.load_progress.connect(self.on_load_progress)

        if url:
            tab.load_url(url.toString())

        return tab

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def tab_changed(self, index):
        if index >= 0:
            tab = self.tabs.widget(index)
            if tab:
                url = tab.browser.url().toString()
                self.update_url_bar(url, tab)

    def current_tab(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.current_tab().load_url(url)

    def navigate_home(self):
        self.current_tab().load_url("https://www.google.com")

    def update_url_bar(self, url, tab):
        if tab == self.current_tab():
            self.url_bar.setText(url)
            self.update_ssl_indicator(url)

    def update_ssl_indicator(self, url):
        if url.startswith('https://'):
            self.ssl_indicator.setText("🔒")
            self.ssl_indicator.setStyleSheet("QPushButton { border: none; font-size: 16px; color: #34a853; }")
        elif url.startswith('http://'):
            self.ssl_indicator.setText("⚠")
            self.ssl_indicator.setStyleSheet("QPushButton { border: none; font-size: 16px; color: #ea4335; }")
        else:
            self.ssl_indicator.setText("ℹ")
            self.ssl_indicator.setStyleSheet("QPushButton { border: none; font-size: 16px; color: #4285f4; }")

    def update_tab_title(self, title, tab):
        index = self.tabs.indexOf(tab)
        if index >= 0:
            self.tabs.setTabText(index, title[:25] + "..." if len(title) > 25 else title)

    def on_load_started(self):
        tab = self.sender()
        index = self.tabs.indexOf(tab)
        if index >= 0:
            self.tabs.setTabText(index, "Loading...")

    def on_load_finished(self, success):
        pass

    def on_load_progress(self, progress):
        pass


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kali Browser")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    browser = KaliBrowser()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
