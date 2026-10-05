from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget,
    QListWidget, QListWidgetItem, QLineEdit, QMessageBox
)

from app.ui.styles import APP_STYLE
from app.core.network import NetworkService
from app.core.hotspot import HotspotService
from app.core.wifi import WiFiService
from app.utils.qr import create_qr_pixmap


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.network = NetworkService()
        self.hotspot = HotspotService()
        self.wifi = WiFiService()

        self.setWindowTitle("Utility WiFi")
        self.setMinimumSize(1050, 700)
        self.resize(1150, 760)
        self.setStyleSheet(APP_STYLE)

        self.build_ui()
        self.refresh_home()

    def build_ui(self):
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(20)

        sidebar = self.build_sidebar()
        root_layout.addWidget(sidebar)

        self.pages = QStackedWidget()
        self.pages.addWidget(self.build_home())
        self.pages.addWidget(self.build_networks())
        self.pages.addWidget(self.build_share())
        self.pages.addWidget(self.build_devices())

        root_layout.addWidget(self.pages, 1)

        self.setCentralWidget(root)

    def build_sidebar(self):
        panel = QFrame()
        panel.setObjectName("sidebar")
        panel.setFixedWidth(230)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 24, 22, 24)
        layout.setSpacing(10)

        logo = QLabel("UTILITY")
        logo.setObjectName("logo")

        product = QLabel("WiFi")
        product.setObjectName("product")

        layout.addWidget(logo)
        layout.addWidget(product)
        layout.addSpacing(35)

        buttons = [
            ("¦   Overview", 0),
            ("?   Networks", 1),
            ("?   Share", 2),
            ("?   Devices", 3),
        ]

        for text, index in buttons:
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.clicked.connect(lambda checked=False, i=index: self.pages.setCurrentIndex(i))
            layout.addWidget(button)

        layout.addStretch()

        status = QLabel("UTILITY WIFI\nv0.1")
        status.setObjectName("version")
        layout.addWidget(status)

        return panel

    def card(self):
        frame = QFrame()
        frame.setObjectName("card")
        return frame

    def build_home(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(18)

        title = QLabel("Your internet.\nEverywhere.")
        title.setObjectName("heroTitle")

        subtitle = QLabel(
            "Connect once. Share your connection with the devices around you."
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)

        self.connection_card = self.card()
        card_layout = QVBoxLayout(self.connection_card)

        self.connection_status = QLabel("? Checking connection…")
        self.connection_status.setObjectName("status")

        self.connection_name = QLabel("Detecting network")
        self.connection_name.setObjectName("cardTitle")

        self.connection_info = QLabel("Please wait…")
        self.connection_info.setObjectName("cardText")

        card_layout.addWidget(self.connection_status)
        card_layout.addWidget(self.connection_name)
        card_layout.addWidget(self.connection_info)

        layout.addWidget(self.connection_card)

        self.share_button = QPushButton("Share connection")
        self.share_button.setObjectName("primaryButton")
        self.share_button.clicked.connect(self.start_sharing)

        layout.addWidget(self.share_button)

        devices_card = self.card()
        devices_layout = QHBoxLayout(devices_card)

        label = QLabel("Connected devices")
        label.setObjectName("cardTitle")

        self.device_count = QLabel("0")
        self.device_count.setObjectName("bigNumber")

        devices_layout.addWidget(label)
        devices_layout.addStretch()
        devices_layout.addWidget(self.device_count)

        layout.addWidget(devices_card)
        layout.addStretch()

        return page

    def build_networks(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Networks")
        title.setObjectName("pageTitle")

        description = QLabel("Available Wi-Fi networks.")
        description.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(description)

        self.network_list = QListWidget()
        self.network_list.setObjectName("networkList")
        layout.addWidget(self.network_list)

        refresh = QPushButton("Scan again")
        refresh.setObjectName("secondaryButton")
        refresh.clicked.connect(self.refresh_networks)

        layout.addWidget(refresh)

        return page

    def build_share(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Share your connection")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Turn your Windows PC into a secure Wi-Fi hotspot."
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        card = self.card()
        form = QVBoxLayout(card)

        form.addWidget(QLabel("Network name"))

        self.ssid = QLineEdit("Utility WiFi")
        self.ssid.setObjectName("input")
        form.addWidget(self.ssid)

        form.addWidget(QLabel("Password"))

        self.password = QLineEdit("utility2026")
        self.password.setObjectName("input")
        self.password.setEchoMode(QLineEdit.Password)
        form.addWidget(self.password)

        self.hotspot_status = QLabel("? Hotspot stopped")
        self.hotspot_status.setObjectName("status")
        form.addWidget(self.hotspot_status)

        buttons = QHBoxLayout()

        start = QPushButton("Start sharing")
        start.setObjectName("primaryButton")
        start.clicked.connect(self.start_sharing)

        stop = QPushButton("Stop")
        stop.setObjectName("secondaryButton")
        stop.clicked.connect(self.stop_sharing)

        buttons.addWidget(start)
        buttons.addWidget(stop)

        form.addLayout(buttons)

        layout.addWidget(card)

        qr_card = self.card()
        qr_layout = QVBoxLayout(qr_card)

        qr_title = QLabel("Connect with QR")
        qr_title.setObjectName("cardTitle")

        self.qr_image = QLabel("QR code will appear here")
        self.qr_image.setAlignment(Qt.AlignCenter)
        self.qr_image.setMinimumHeight(220)

        generate = QPushButton("Generate QR")
        generate.setObjectName("secondaryButton")
        generate.clicked.connect(self.generate_qr)

        qr_layout.addWidget(qr_title)
        qr_layout.addWidget(self.qr_image)
        qr_layout.addWidget(generate)

        layout.addWidget(qr_card)
        layout.addStretch()

        return page

    def build_devices(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Connected devices")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Devices currently using Utility WiFi."
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.devices_list = QListWidget()
        self.devices_list.addItem("Device discovery will be enabled in the next build.")
        layout.addWidget(self.devices_list)

        refresh = QPushButton("Refresh")
        refresh.setObjectName("secondaryButton")
        refresh.clicked.connect(self.refresh_devices)

        layout.addWidget(refresh)

        return page

    def refresh_home(self):
        info = self.network.get_connection_info()

        if info["connected"]:
            self.connection_status.setText("? INTERNET CONNECTED")
            self.connection_name.setText(info["name"])
            self.connection_info.setText(
                f"Interface: {info['interface']}\n"
                f"IP: {info['ip']}"
            )
        else:
            self.connection_status.setText("? NO INTERNET")
            self.connection_name.setText("No active connection")
            self.connection_info.setText(
                "Connect to Wi-Fi, Ethernet or a satellite terminal first."
            )

    def refresh_networks(self):
        self.network_list.clear()

        networks = self.wifi.scan()

        if not networks:
            self.network_list.addItem("No networks detected.")
            return

        for network in networks:
            text = (
                f"{network['ssid'] or '(Hidden network)'}   "
                f"{network['signal']}%"
            )

            item = QListWidgetItem(text)
            self.network_list.addItem(item)

    def start_sharing(self):
        ssid = self.ssid.text().strip()
        password = self.password.text()

        if len(ssid) < 1:
            QMessageBox.warning(self, "Utility WiFi", "Enter a network name.")
            return

        if len(password) < 8:
            QMessageBox.warning(
                self,
                "Utility WiFi",
                "The Wi-Fi password must contain at least 8 characters."
            )
            return

        result = self.hotspot.start(ssid, password)

        if result["success"]:
            self.hotspot_status.setText("? HOTSPOT ACTIVE")
            self.share_button.setText("Connection shared")
            QMessageBox.information(
                self,
                "Utility WiFi",
                "Utility WiFi is now sharing the connection."
            )
        else:
            QMessageBox.warning(
                self,
                "Could not start hotspot",
                result["message"]
            )

    def stop_sharing(self):
        result = self.hotspot.stop()

        if result["success"]:
            self.hotspot_status.setText("? Hotspot stopped")
            self.share_button.setText("Share connection")

    def generate_qr(self):
        ssid = self.ssid.text().strip()
        password = self.password.text()

        pixmap = create_qr_pixmap(ssid, password)
        self.qr_image.setPixmap(pixmap)

    def refresh_devices(self):
        self.devices_list.clear()
        self.devices_list.addItem(
            "Device discovery will be connected to Windows tethering clients."
        )
