from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QPixmap
import qrcode


def create_qr_pixmap(ssid, password):
    data = f"WIFI:T:WPA;S:{ssid};P:{password};;"

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image()

    image = image.convert("RGB")

    image.save("qr_temp.png")

    pixmap = QPixmap("qr_temp.png")
    return pixmap.scaled(
        260,
        260
    )
