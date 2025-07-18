# json_annotation_tool/ui/edit_annotation_dialog.py
from typing import Optional
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QComboBox, QLineEdit, QSpinBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from core.annotation_manager import edit_shape_in_file

class EditAnnotationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Annotation')
        self.parent = parent

        layout = QFormLayout(self)

        # 选择要编辑的框编号
        self.index_spin = QSpinBox()
        self.index_spin.setMinimum(1)
        max_shapes = 1
        if parent and hasattr(parent, 'preview') and parent.preview.annotations:
            idx = parent.preview.image_list.currentRow()
            if idx >= 0:
                max_shapes = max(len(parent.preview.annotations[idx].shapes), 1)
        self.index_spin.setMaximum(max_shapes)
        layout.addRow('Shape # (1-based):', self.index_spin)

        # is_region_flag 可选
        self.flag_combo = QComboBox()
        self.flag_combo.addItem('')  # 空表示不修改
        self.flag_combo.addItems(['false', 'true'])
        layout.addRow('is_region_flag (optional):', self.flag_combo)

        # region_name 可选
        self.region_input = QLineEdit()
        self.region_input.setPlaceholderText('Optional new region_name')
        layout.addRow('Region name (optional):', self.region_input)

        # label 可选
        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText('Optional new label')
        layout.addRow('Label (optional):', self.label_input)

        # coordinates 可选（四个输入框）
        self.x1_input = QLineEdit()
        self.x1_input.setPlaceholderText('x1')
        layout.addRow('x1 (optional):', self.x1_input)
        self.y1_input = QLineEdit()
        self.y1_input.setPlaceholderText('y1')
        layout.addRow('y1 (optional):', self.y1_input)
        self.x2_input = QLineEdit()
        self.x2_input.setPlaceholderText('x2')
        layout.addRow('x2 (optional):', self.x2_input)
        self.y2_input = QLineEdit()
        self.y2_input.setPlaceholderText('y2')
        layout.addRow('y2 (optional):', self.y2_input)

        # 按钮
        btn_apply = QPushButton('Apply')
        btn_apply.clicked.connect(self.on_apply)
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.reject)
        layout.addRow(btn_apply, btn_cancel)

    def on_apply(self):
        # 构建 updates 字典
        updates = {}
        flag = self.flag_combo.currentText().strip()
        if flag:
            updates['is_region_flag'] = flag
        region = self.region_input.text().strip()
        if region:
            updates['region_name'] = region
        label = self.label_input.text().strip()
        if label:
            updates['label'] = label
        # 坐标
        x1_text = self.x1_input.text().strip()
        y1_text = self.y1_input.text().strip()
        x2_text = self.x2_input.text().strip()
        y2_text = self.y2_input.text().strip()
        if x1_text or y1_text or x2_text or y2_text:
            try:
                x1 = float(x1_text)
                y1 = float(y1_text)
                x2 = float(x2_text)
                y2 = float(y2_text)
                updates['points'] = (x1, y1, x2, y2)
            except ValueError:
                QMessageBox.warning(self, 'Input Error', 'Coordinates must be numeric.')
                return
        if not updates:
            # 没有修改项就关闭
            return

        shape_idx = self.index_spin.value() - 1
        for ann in self.parent.preview.annotations:
            try:
                edit_shape_in_file(ann.json_path, shape_idx, updates)
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to edit shape: {e}')
                return
        self.accept()