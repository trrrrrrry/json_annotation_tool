# json_annotation_tool/ui/add_annotation_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QComboBox, QLineEdit, QSpinBox, QPushButton, QMessageBox
)
from core.annotation_manager import add_shape_to_file

class AddAnnotationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Annotation')
        self.parent = parent

        layout = QFormLayout(self)

        # is_region_flag 下拉
        self.flag_combo = QComboBox()
        self.flag_combo.addItems(['false', 'true'])
        layout.addRow('is_region_flag:', self.flag_combo)

        # 可选 region_name
        self.region_input = QLineEdit()
        self.region_input.setPlaceholderText('Optional: new region_name')
        layout.addRow('Region name (optional):', self.region_input)

        # 可选 label
        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText('Optional: new label')
        layout.addRow('Label (optional):', self.label_input)

        # 坐标输入 (四个文本框)
        self.x1_input = QLineEdit()
        self.x1_input.setPlaceholderText('x1')
        layout.addRow('x1:', self.x1_input)
        self.y1_input = QLineEdit()
        self.y1_input.setPlaceholderText('y1')
        layout.addRow('y1:', self.y1_input)
        self.x2_input = QLineEdit()
        self.x2_input.setPlaceholderText('x2')
        layout.addRow('x2:', self.x2_input)
        self.y2_input = QLineEdit()
        self.y2_input.setPlaceholderText('y2')
        layout.addRow('y2:', self.y2_input)

        # 模板索引 (0 = none; >0 表示复制对应框)
        self.template_spin = QSpinBox()
        self.template_spin.setMinimum(0)
        max_shapes = 1
        if parent and hasattr(parent, 'preview') and parent.preview.annotations:
            idx = parent.preview.image_list.currentRow()
            if idx >= 0:
                max_shapes = max(len(parent.preview.annotations[idx].shapes), 1)
        self.template_spin.setMaximum(max_shapes)
        layout.addRow('Template shape # (0 = none):', self.template_spin)

        # 按钮
        btn_add = QPushButton('Add')
        btn_add.clicked.connect(self.on_add)
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.reject)
        layout.addRow(btn_add, btn_cancel)

    def on_add(self):
        flag = self.flag_combo.currentText()
        region_override = self.region_input.text().strip() or None
        label_override = self.label_input.text().strip() or None

        # 坐标解析和校验
        try:
            x1 = float(self.x1_input.text())
            y1 = float(self.y1_input.text())
            x2 = float(self.x2_input.text())
            y2 = float(self.y2_input.text())
            coords = (x1, y1, x2, y2)
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Coordinates must be numeric.')
            return

        spin_val = self.template_spin.value()
        template_idx = None if spin_val == 0 else spin_val - 1

        # 对所有预览文件执行添加操作
        for ann in self.parent.preview.annotations:
            add_shape_to_file(
                json_path=ann.json_path,
                is_region_flag=flag,
                coords=coords,
                template_idx=template_idx,
                region_name=region_override,
                label=label_override
            )
        self.accept()