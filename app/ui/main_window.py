from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
    QScrollArea,
    QSizePolicy,
)

from app.core.network import NetworkService
from app.core.wifi import WiFiService
from app.core.hotspot import HotspotService
from app.core.devices import DeviceService
from app.core.diagnostics import DiagnosticsService
from app.core.profiles import ProfileService
from app.core.connection import ConnectionManager


BG = "#EDF1F0"
TEXT = "#111615"
MUTED = "#69716F"
LIME = "#DFFF45"
WHITE = "#F8FAF9"
BORDER = "#D9DFDD"


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Utility Connect")
        self.resize(1100, 760)
        self.setMinimumSize(900, 620)

        self.network_service = NetworkService()
        self.wifi_service = WiFiService()
        self.hotspot_service = HotspotService()
        self.device_service = DeviceService()
        self.diagnostics_service = DiagnosticsService()
        self.profile_service = ProfileService()

        self.connection_manager = ConnectionManager(
            self.network_service,
            self.wifi_service,
            self.hotspot_service,
        )

        self.pages = QStackedWidget()

        self.build_ui()
        self.refresh_all()

    def build_ui(self):

        root = QWidget()
        root.setStyleSheet(f"""
            QWidget {{
                background: {BG};
                color: {TEXT};
                font-family: "Segoe UI";
            }}

            QPushButton {{
                border: none;
                border-radius: 12px;
                padding: 11px 18px;
                font-size: 14px;
            }}

            QPushButton:hover {{
                opacity: 0.85;
            }}
        """)

        main = QVBoxLayout(root)
        main.setContentsMargins(42, 30, 42, 30)
        main.setSpacing(0)

        main.addWidget(self.create_header())
        main.addSpacing(42)

        self.pages.addWidget(self.create_overview())
        self.pages.addWidget(self.create_network())
        self.pages.addWidget(self.create_devices())
        self.pages.addWidget(self.create_share())
        self.pages.addWidget(self.create_diagnostics())
        self.pages.addWidget(self.create_settings())

        main.addWidget(self.pages)

        self.setCentralWidget(root)

    def create_header(self):

        header = QHBoxLayout()
        header.setSpacing(8)

        brand = QLabel("Utility")
        brand.setFont(QFont("Segoe UI", 17, QFont.Weight.Bold))

        product = QLabel("Connect")
        product.setFont(QFont("Segoe UI", 17))
        product.setStyleSheet(f"color: {MUTED};")

        header.addWidget(brand)
        header.addWidget(product)
        header.addStretch()

        buttons = [
            ("Overview", 0),
            ("Network", 1),
            ("Devices", 2),
            ("Share", 3),
            ("Diagnostics", 4),
            ("Settings", 5),
        ]

        for text, index in buttons:
            button = QPushButton(text)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {MUTED};
                    padding: 8px 10px;
                }}

                QPushButton:hover {{
                    color: {TEXT};
                }}
            """)
            button.clicked.connect(lambda checked=False, i=index: self.show_page(i))
            header.addWidget(button)

        return self.wrap_layout(header)

    def wrap_layout(self, layout):
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_overview(self):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Your internet,\neverywhere.")
        title.setFont(QFont("Segoe UI", 42, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT};")

        subtitle = QLabel(
            "One simple place to understand, share and manage your connection."
        )
        subtitle.setFont(QFont("Segoe UI", 15))
        subtitle.setStyleSheet(f"color: {MUTED};")

        layout.addWidget(title)
        layout.addSpacing(14)
        layout.addWidget(subtitle)
        layout.addSpacing(45)

        status = QFrame()
        status.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1px solid {BORDER};
                border-radius: 20px;
            }}
        """)

        status_layout = QVBoxLayout(status)
        status_layout.setContentsMargins(28, 24, 28, 24)

        row = QHBoxLayout()

        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Segoe UI", 17))

        self.status_label = QLabel("Checking connection...")
        self.status_label.setFont(QFont("Segoe UI", 17, QFont.Weight.Medium))

        row.addWidget(self.status_dot)
        row.addWidget(self.status_label)
        row.addStretch()

        status_layout.addLayout(row)

        self.connection_detail = QLabel("Detecting your active connection...")
        self.connection_detail.setStyleSheet(f"color: {MUTED};")
        status_layout.addWidget(self.connection_detail)

        layout.addWidget(status)

        layout.addSpacing(20)

        info = QHBoxLayout()

        self.connection_type = self.create_stat("Connection", "—")
        self.device_count = self.create_stat("Devices", "0")

        info.addWidget(self.connection_type)
        info.addWidget(self.device_count)

        layout.addLayout(info)

        layout.addSpacing(28)

        share = QPushButton("Share connection   →")
        share.setCursor(Qt.CursorShape.PointingHandCursor)
        share.setMinimumHeight(54)
        share.setStyleSheet(f"""
            QPushButton {{
                background: {LIME};
                color: {TEXT};
                font-size: 15px;
                font-weight: 600;
                border-radius: 14px;
            }}

            QPushButton:hover {{
                background: #E7FF72;
            }}
        """)
        share.clicked.connect(lambda: self.show_page(3))

        layout.addWidget(share)
        layout.addStretch()

        return page

    def create_stat(self, title, value):

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border-bottom: 1px solid {BORDER};
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 18, 0, 18)

        label = QLabel(title.upper())
        label.setFont(QFont("Segoe UI", 10))
        label.setStyleSheet(f"color: {MUTED};")

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Medium))

        layout.addWidget(label)
        layout.addSpacing(5)
        layout.addWidget(value_label)

        frame.value_label = value_label

        return frame

    def create_network(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Network")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))

        subtitle = QLabel("Available connections around you.")
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 15px;")

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(subtitle)
        layout.addSpacing(30)

        self.network_status = QLabel("Ready to scan.")
        self.network_status.setStyleSheet(f"color: {MUTED};")

        layout.addWidget(self.network_status)

        scan = QPushButton("Scan networks")
        scan.setCursor(Qt.CursorShape.PointingHandCursor)
        scan.setStyleSheet(f"""
            QPushButton {{
                background: {TEXT};
                color: white;
                border-radius: 12px;
            }}
        """)
        scan.clicked.connect(self.scan_networks)

        layout.addWidget(scan)
        layout.addSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.network_container = QWidget()
        self.network_layout = QVBoxLayout(self.network_container)
        self.network_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.network_container)

        layout.addWidget(scroll)

        return page

    def create_devices(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Devices")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))

        subtitle = QLabel("Devices connected through Utility Connect.")
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 15px;")

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(subtitle)
        layout.addSpacing(35)

        self.devices_label = QLabel("No connected devices yet.")
        self.devices_label.setFont(QFont("Segoe UI", 18))
        self.devices_label.setStyleSheet(f"color: {MUTED};")

        layout.addWidget(self.devices_label)

        layout.addStretch()

        return page

    def create_share(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Share")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))

        subtitle = QLabel(
            "Turn your connection into a simple shared network."
        )
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 15px;")

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(subtitle)
        layout.addSpacing(35)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1px solid {BORDER};
                border-radius: 20px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)

        self.share_status = QLabel("Sharing is off")
        self.share_status.setFont(QFont("Segoe UI", 20, QFont.Weight.Medium))

        self.share_detail = QLabel(
            "Start sharing to make this connection available to other devices."
        )
        self.share_detail.setStyleSheet(f"color: {MUTED};")

        self.share_button = QPushButton("Start sharing")
        self.share_button.setMinimumHeight(50)
        self.share_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.share_button.setStyleSheet(f"""
            QPushButton {{
                background: {LIME};
                color: {TEXT};
                font-weight: 600;
            }}
        """)
        self.share_button.clicked.connect(self.toggle_sharing)

        card_layout.addWidget(self.share_status)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.share_detail)
        card_layout.addSpacing(25)
        card_layout.addWidget(self.share_button)

        layout.addWidget(card)
        layout.addStretch()

        return page

    def create_diagnostics(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Diagnostics")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))

        subtitle = QLabel(
            "Understand what's happening with your connection."
        )
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 15px;")

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(subtitle)
        layout.addSpacing(35)

        self.diagnostic_status = QLabel("No diagnostic has been run.")
        self.diagnostic_status.setFont(QFont("Segoe UI", 18))

        layout.addWidget(self.diagnostic_status)

        self.diagnostic_detail = QLabel("")
        self.diagnostic_detail.setStyleSheet(f"color: {MUTED};")

        layout.addWidget(self.diagnostic_detail)

        layout.addSpacing(25)

        button = QPushButton("Run diagnostic")
        button.setMinimumHeight(50)
        button.setStyleSheet(f"""
            QPushButton {{
                background: {TEXT};
                color: white;
            }}
        """)
        button.clicked.connect(self.run_diagnostic)

        layout.addWidget(button)

        layout.addStretch()

        return page

    def create_settings(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))

        subtitle = QLabel("Utility Connect preferences.")
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 15px;")

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(subtitle)
        layout.addSpacing(35)

        settings = [
            ("Start with Windows", "Automatically open Utility Connect."),
            ("Remember networks", "Keep trusted connection profiles."),
            ("Auto reconnect", "Try to restore sharing when connection returns."),
        ]

        for name, description in settings:

            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background: {WHITE};
                    border-bottom: 1px solid {BORDER};
                }}
            """)

            box = QVBoxLayout(frame)
            box.setContentsMargins(22, 18, 22, 18)

            label = QLabel(name)
            label.setFont(QFont("Segoe UI", 15, QFont.Weight.Medium))

            desc = QLabel(description)
            desc.setStyleSheet(f"color: {MUTED};")

            box.addWidget(label)
            box.addWidget(desc)

            layout.addWidget(frame)

        layout.addStretch()

        return page

    def show_page(self, index):
        self.pages.setCurrentIndex(index)

    def refresh_all(self):

        self.refresh_connection()
        self.refresh_devices()

    def refresh_connection(self):

        try:
            connection = self.connection_manager.detect_source()

            if connection:

                self.status_dot.setStyleSheet(
                    f"color: {LIME};"
                )

                self.status_label.setText("Connected")

                interface = connection.get("interface", "Unknown")

                self.connection_detail.setText(
                    f"Active connection: {interface}"
                )

                self.connection_type.value_label.setText(interface)

            else:

                self.status_dot.setStyleSheet(
                    f"color: {MUTED};"
                )

                self.status_label.setText("Offline")
                self.connection_detail.setText(
                    "No active internet connection detected."
                )

                self.connection_type.value_label.setText("Offline")

        except Exception as error:

            self.status_label.setText("Connection unavailable")
            self.connection_detail.setText(str(error))

    def refresh_devices(self):

        try:

            devices = self.device_service.get_connected_devices()

            count = len(devices)

            self.device_count.value_label.setText(str(count))

            if devices:

                self.devices_label.setText(
                    f"{count} device(s) connected."
                )

            else:

                self.devices_label.setText(
                    "No connected devices yet."
                )

        except Exception:

            self.device_count.value_label.setText("0")

    def scan_networks(self):

        self.network_status.setText("Scanning...")

        while self.network_layout.count():

            item = self.network_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        try:

            networks = self.wifi_service.scan_networks()

            if not networks:

                self.network_status.setText(
                    "No networks detected."
                )
                return

            self.network_status.setText(
                f"{len(networks)} network(s) found."
            )

            for network in networks:

                ssid = network.get("ssid", "Unknown")
                signal = network.get("signal", "?")

                row = QFrame()
                row.setStyleSheet(f"""
                    QFrame {{
                        background: {WHITE};
                        border: 1px solid {BORDER};
                        border-radius: 14px;
                    }}
                """)

                row_layout = QHBoxLayout(row)

                name = QLabel(ssid)
                name.setFont(
                    QFont("Segoe UI", 15, QFont.Weight.Medium)
                )

                strength = QLabel(f"{signal}%")
                strength.setStyleSheet(f"color: {MUTED};")

                row_layout.addWidget(name)
                row_layout.addStretch()
                row_layout.addWidget(strength)

                self.network_layout.addWidget(row)

        except Exception as error:

            self.network_status.setText(
                f"Scan error: {error}"
            )

    def toggle_sharing(self):

        try:

            result = self.connection_manager.start_sharing()

            if result:

                self.share_status.setText("Sharing is on")
                self.share_detail.setText(
                    "Your connection is now available to other devices."
                )
                self.share_button.setText("Stop sharing")

            else:

                self.share_status.setText(
                    "Sharing could not be started"
                )

        except Exception as error:

            self.share_status.setText("Sharing unavailable")
            self.share_detail.setText(str(error))

    def run_diagnostic(self):

        self.diagnostic_status.setText("Running diagnostic...")
        self.diagnostic_detail.setText("Please wait...")

        QApplication.processEvents()

        try:

            result = self.diagnostics_service.run_full_diagnostic()

            internet = result.get("internet")

            if internet:

                self.diagnostic_status.setText(
                    "Connection looks healthy."
                )

            else:

                self.diagnostic_status.setText(
                    "Internet connection needs attention."
                )

            self.diagnostic_detail.setText(
                f"Latency: {result.get('latency', '—')}    "
                f"Packet loss: {result.get('packet_loss', '—')}    "
                f"Download: {result.get('download', '—')}    "
                f"Upload: {result.get('upload', '—')}"
            )

        except Exception as error:

            self.diagnostic_status.setText(
                "Diagnostic failed."
            )

            self.diagnostic_detail.setText(
                str(error)
            )


def main():

    app = QApplication([])

    app.setApplicationName("Utility Connect")
    app.setOrganizationName("Utility")

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
