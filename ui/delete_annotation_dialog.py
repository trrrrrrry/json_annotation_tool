# json_annotation_tool/ui/delete_annotation_dialog.py
from PyQt5.QtWidgets import QDialog, QFormLayout, QComboBox, QLineEdit, QPushButton
from json_annotation_tool.core.annotation_manager import delete_shapes_in_file

class DeleteAnnotationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Delete Annotation')
        self.parent = parent

        layout = QFormLayout(self)

        # is_region_flag 下拉（可选）
        self.flag_combo = QComboBox()
        self.flag_combo.addItem('')  # 空，代表不使用此条件
        self.flag_combo.addItems(['false', 'true'])
        layout.addRow('is_region_flag (optional):', self.flag_combo)

        # Points 输入
        self.points_input = QLineEdit()
        self.points_input.setPlaceholderText('x1, y1, x2, y2')
        layout.addRow('Points (optional):', self.points_input)

        # Label 输入
        self.label_input = QLineEdit()
        layout.addRow('Label (optional):', self.label_input)

        # Region name 输入
        self.region_input = QLineEdit()
        layout.addRow('Region name (optional):', self.region_input)

        # 按钮
        btn_del = QPushButton('Delete')
        btn_del.clicked.connect(self.on_delete)
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.reject)
        layout.addRow(btn_del, btn_cancel)

    def on_delete(self):
        criteria = {}
        flag = self.flag_combo.currentText()
        if flag:
            criteria['is_region_flag'] = flag
        pts_text = self.points_input.text().strip()
        if pts_text:
            try:
                pts = tuple(map(float, pts_text.split(',')))
                if len(pts) == 4:
                    criteria['points'] = pts
            except ValueError:
                self.points_input.setFocus()
                return
        label = self.label_input.text().strip()
        if label:
            criteria['label'] = label
        region = self.region_input.text().strip()
        if region:
            criteria['region_name'] = region

        if not criteria:
            return

        for ann in self.parent.preview.annotations:
            delete_shapes_in_file(ann.json_path, criteria)
        self.accept()