# json_annotation_tool/ui/preview_widget.py
import random
from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt
import os
from core.models import AnnotationFile

class PreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Image list control
        self.image_list = QListWidget()
        self.image_list.setMinimumWidth(300)
        self.image_list.currentRowChanged.connect(self._on_image_change)

        # Canvas label
        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setScaledContents(False)

        # Layout: canvas on left, list on right
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.canvas, 5)
        top_layout.addWidget(self.image_list, 1)

        # Navigation buttons
        btn_prev = QPushButton('< Previous (←)')
        btn_next = QPushButton('Next > (→)')
        btn_prev.clicked.connect(self.show_previous)
        btn_next.clicked.connect(self.show_next)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_prev)
        btn_layout.addWidget(btn_next)
        btn_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        self.annotations: list[AnnotationFile] = []

    def load_annotations(self, annotations: list[AnnotationFile]):
        """
        Load list of AnnotationFile and update image_list.
        """
        self.annotations = annotations
        self.image_list.clear()
        for ann in annotations:
            name = os.path.basename(ann.image_path) if ann.image_path else os.path.basename(ann.json_path)
            self.image_list.addItem(name)

    def _on_image_change(self, index: int):
        """
        Load image at 'index' and draw bounding boxes in random colors.
        """
        if index < 0 or index >= len(self.annotations):
            self.canvas.clear()
            return
        ann = self.annotations[index]
        path = ann.image_path
        if not path:
            self.canvas.clear()
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Failed to load image: {path}")
            self.canvas.clear()
            return

        # Scale pixmap to fit canvas
        cw = max(self.canvas.width(), 1)
        ch = max(self.canvas.height(), 1)
        scaled = pixmap.scaled(cw, ch, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        painter = QPainter(scaled)
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        sx = scaled.width() / pixmap.width() if pixmap.width() else 1
        sy = scaled.height() / pixmap.height() if pixmap.height() else 1

        for i, shp in enumerate(ann.shapes):
            # Random color for each box
            color = QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            pen = QPen(color)
            pen.setWidth(2)
            painter.setPen(pen)

            # Compute rectangle positions
            (x1, y1), (x2, y2) = shp.points
            rx1, ry1 = int(x1 * sx), int(y1 * sy)
            rx2, ry2 = int(x2 * sx), int(y2 * sy)

            # Draw rectangle and text
            painter.drawRect(rx1, ry1, rx2 - rx1, ry2 - ry1)
            info = f"{i+1}. is_region_flag: {shp.is_region_flag} | label: {shp.label} | region_name: {shp.region_name}"
            painter.drawText(rx1 + 2, ry1 - 5, info)

        painter.end()
        self.canvas.setPixmap(scaled)

    def show_previous(self):
        idx = self.image_list.currentRow()
        if idx > 0:
            self.image_list.setCurrentRow(idx - 1)

    def show_next(self):
        idx = self.image_list.currentRow()
        if idx < len(self.annotations) - 1:
            self.image_list.setCurrentRow(idx + 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.show_previous()
        elif event.key() == Qt.Key_Right:
            self.show_next()
        else:
            super().keyPressEvent(event)
