# json_annotation_tool/ui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QAction, QToolBar, QStatusBar
)
import os
from json_annotation_tool.core.file_manager import find_annotation_pairs
from json_annotation_tool.core.annotation_manager import load_annotation
from json_annotation_tool.ui.preview_widget import PreviewWidget
from json_annotation_tool.ui.add_annotation_dialog import AddAnnotationDialog
from json_annotation_tool.ui.delete_annotation_dialog import DeleteAnnotationDialog
from json_annotation_tool.ui.edit_annotation_dialog import EditAnnotationDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('JSON Annotation Tool')
        self.resize(900, 600)

        # —— 工具栏 ——
        toolbar = QToolBar('Main Toolbar', self)
        self.addToolBar(toolbar)

        open_folder = QAction('Open Folder', self)
        open_folder.triggered.connect(self.open_folder)
        open_json = QAction('Open JSON', self)
        open_json.triggered.connect(self.open_json)
        add_ann = QAction('Add Annotation', self)
        add_ann.triggered.connect(self.open_add_dialog)
        edit_ann = QAction('Edit Annotation', self)
        edit_ann.triggered.connect(self.open_edit_dialog)
        del_ann = QAction('Delete Annotation', self)
        del_ann.triggered.connect(self.open_delete_dialog)

        for act in (open_folder, open_json, add_ann, edit_ann, del_ann):
            toolbar.addAction(act)

        # 设置部分按钮背景色为浅蓝
        for action in (open_folder, add_ann, del_ann):
            btn = toolbar.widgetForAction(action)
            if btn:
                btn.setStyleSheet("background-color: #C8E4F2;")

        # —— 预览区 ——
        self.preview = PreviewWidget()
        self.setCentralWidget(self.preview)

        # —— 状态栏 ——
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if not folder:
            print("folder not found")
            return
        print("folder found")
        pairs = find_annotation_pairs(folder)
        print(pairs)
        anns = [load_annotation(p.json_path) for p in pairs]
        self.preview.load_annotations(anns)
        print("loaded succesfully")
        self.status.showMessage(f'Loaded {len(anns)} files from "{folder}"')

    def open_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 'Select JSON File', filter='JSON Files (*.json)'
        )
        if not path:
            return
        ann = load_annotation(path)
        if not ann.image_path:
            img, _ = QFileDialog.getOpenFileName(
                self, 'Select Image for JSON',
                filter='Images (*.jpg *.jpeg *.png *.bmp)'
            )
            if img:
                ann.image_path = img
        self.preview.load_annotations([ann])
        name = os.path.basename(path)
        self.status.showMessage(f'Loaded JSON "{name}"')

    def open_add_dialog(self):
        dlg = AddAnnotationDialog(self)
        if dlg.exec_():
            self._refresh_preview()

    def open_delete_dialog(self):
        dlg = DeleteAnnotationDialog(self)
        if dlg.exec_():
            self._refresh_preview()

    def open_edit_dialog(self):
        dlg = EditAnnotationDialog(self)
        if dlg.exec_():
            # 编辑完后刷新当前预览
            self._refresh_preview()


    def _refresh_preview(self):
        idx = self.preview.image_list.currentRow()
        self.preview._on_image_change(idx)
