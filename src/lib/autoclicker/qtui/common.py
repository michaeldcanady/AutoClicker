import enum
import functools

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer

ICON_PATH_PREFIX = "src\Images"

class AutClickerIcon(enum.Enum):
    AUTOKEY = "icon.png"
    AUTOKEY_SCALABLE = "icon.svg"
    #SYSTEM_TRAY = "autokey-status.svg"
    #SYSTEM_TRAY_DARK = "autokey-status-dark.svg"
    #SYSTEM_TRAY_ERROR = "autokey-status-error.svg"

@functools.lru_cache()
def load_icon(name: AutClickerIcon) -> QIcon:
    file_path = ICON_PATH_PREFIX + "/" + name.value
    icon = QIcon(file_path)
    if not icon.availableSizes() and file_path.endswith(".svg"):
        # FIXME: Work around Qt Bug: https://bugreports.qt.io/browse/QTBUG-63187
        # Manually render the SVG to some common icon sizes.
        icon = QIcon()  # Discard the bugged QIcon
        renderer = QSvgRenderer(file_path)
        for size in (16, 22, 24, 32, 64, 128):
            pixmap = QPixmap(QSize(size, size))
            pixmap.fill(QColor(255, 255, 255, 0))
            renderer.render(QPainter(pixmap))
            icon.addPixmap(pixmap)
    return icon