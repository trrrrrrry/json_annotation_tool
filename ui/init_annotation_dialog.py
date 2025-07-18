import os
from typing import Tuple
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QFileDialog, QMessageBox
)
from core.annotation_manager import create_initial_annotations

class InitAnnotationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Initialize Annotations')

        layout = QFormLayout(self)

        # 文件夹路径
        self.folder_input = QLineEdit()
        btn_browse = QPushButton('Browse...')
        btn_browse.clicked.connect(self._browse_folder)
        layout.addRow('Target Folder:', self.folder_input)
        layout.addRow('', btn_browse)

        # is_region_flag
        self.flag_combo = QComboBox()
        self.flag_combo.addItems(['false', 'true'])
        layout.addRow('is_region_flag:', self.flag_combo)

        # region_name 和 label
        self.region_input = QLineEdit()
        layout.addRow('Region name:', self.region_input)
        self.label_input = QLineEdit()
        layout.addRow('Label:', self.label_input)

        # 坐标输入
        self.x1 = QLineEdit(); self.x1.setPlaceholderText('x1')
        self.y1 = QLineEdit(); self.y1.setPlaceholderText('y1')
        self.x2 = QLineEdit(); self.x2.setPlaceholderText('x2')
        self.y2 = QLineEdit(); self.y2.setPlaceholderText('y2')
        layout.addRow('x1:', self.x1)
        layout.addRow('y1:', self.y1)
        layout.addRow('x2:', self.x2)
        layout.addRow('y2:', self.y2)

        # 确认/取消
        btn_create = QPushButton('Create')
        btn_create.clicked.connect(self._on_create)
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.reject)
        layout.addRow(btn_create, btn_cancel)

    def _browse_folder(self):
        d = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if d:
            self.folder_input.setText(d)

    def _on_create(self):
        folder = self.folder_input.text().strip()
        if not os.path.isdir(folder):
            QMessageBox.warning(self, 'Error', '请选择有效的文件夹')
            return
        try:
            coords: Tuple[float, float, float, float] = (
                float(self.x1.text()), float(self.y1.text()),
                float(self.x2.text()), float(self.y2.text())
            )
        except ValueError:
            QMessageBox.warning(self, 'Error', '坐标必须为数字')
            return

        create_initial_annotations(
            folder=folder,
            is_region_flag=self.flag_combo.currentText(),
            region_name=self.region_input.text().strip(),
            label=self.label_input.text().strip(),
            coords=coords
        )
        QMessageBox.information(self, 'Success', '已生成所有 JSON 文件')
        self.accept()
