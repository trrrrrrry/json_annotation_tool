# json_annotation_tool
一个基于 Python + PyQt5 的桌面应用，用于浏览并编辑与图像配套的 JSON 格式边界框标注。支持批量操作，一键增删改，极大提升 Labelme 标注后的后处理效率。
## 项目结构
## 📂 Project Structure

```plaintext
json_annotation_tool/             # Project root directory
├── build/                        # PyInstaller build artifacts (ignore)
│   └── main/                     # Bundled library and metadata
├── dist/                         # Distributable output (e.g., executable)
│   └── main.exe
├── core/                         # Core processing modules
│   ├── models.py                 # Data models: Shape, AnnotationFile
│   ├── file_manager.py           # Scan folders & pair images with JSON
│   └── annotation_manager.py     # Load/save/add/edit/delete annotations
├── test_folder/                  # Example data set 1
├── test_folder2/                 # Example data set 2
├── ui/                           # User interface components
│   ├── add_annotation_dialog.py  # Dialog for adding new shapes
│   ├── delete_annotation_dialog.py # Dialog for deleting shapes
│   ├── edit_annotation_dialog.py # Dialog for editing shapes
│   ├── init_annotation_dialog.py # Dialog for bulk JSON initialization
│   ├── main_window.py            # Main application window and toolbar
│   └── preview_widget.py         # Image preview and overlay widget
├── utils/                        # Utility scripts
│   ├── Fortnite_cn_Death-multiple_1920x1080_2509_2.json # Sample JSON
│   └── main.py                   # Legacy or helper script
├── main.spec                     # PyInstaller specification file
├── README.md                     # Project documentation (this file)
├── requirements                  # (optional) alternative dependencies file
└── requirements.txt              # Python dependencies list
```

---
## JSON 格式示例
每个 JSON 文件至少包含一个 ```shapes``` 列表，每项示例如下：
```json
{
  "imagePath": "I_am_a_picture.png",
  "shapes": [
    {
      "region_name": "我是大框！",
      "is_region_flag": "true",
      "label": "我是一个label！",
      "points": [[100, 200], [400, 500]],
      "other_key": "…"    // 其它自定义字段
    }
    // … 更多框
  ]
}
```
工具会在加载/保存时保留除上述字段外的所有额外键值。

---
## 功能一览
- 批量加载
  - 加载指定文件夹下所有 JSON–图片 配对
  - 或者单独打开一个 JSON，并手动选择对应图片

- 可视化预览

  - 原图等比展示，不放大失真
  - 叠加边界框，框内显示 1-based 编号
  - 框上方以文字显示：is_region_flag | label | region_name

  - “上一张/下一张”按钮 + 键盘 ← → 切换
  - 
- 初始化 JSON：

  - 批量为指定文件夹下每张图片生成初始 JSON
  - 支持自定义初始 `flag`、`region_name`、`label`、`points`
  - 自动检测 `imageWidth`、`imageHeight`

- 添加标注

  - 选取已有框作为元数据模板
  - 分别输入四个坐标（x1,y1,x2,y2）
  - 可选覆盖 region_name 与 label

- 编辑标注
  - 按编号（1-based）选择要修改的框
  - 可选修改：is_region_flag、region_name、label、points

- 删除标注
  - 按 is_region_flag、坐标、label、region_name 多条件删除

- 批量操作

  - 增删改一次操作，即可应用于当前加载的所有 JSON 文件
 
---

## 安装与运行
  1. 克隆项目
  ```bash
     git clone https://github.com/trrrrrrry/json_annotation_tool.git
     cd json_annotation_tool
  ```
  2. 安装依赖
  ```bash
    pip install -r requirements.txt  # PyQt5, Pillow
  ```
  3. 启动应用
  ```bash
    python -m json_annotation_tool.main
  ```

---

## 未来扩展
- 可拖拽调整：在预览区直接拖拽框体，实时保存

- 缩放与平移：支持局部放大、平移查看细节

- 多选批量编辑：同时选中多个框统一操作

- 配置化：自定义颜色、文字大小、快捷键等 UI 设置

- 插件扩展：接入更多导出格式或自定义校验逻辑

> _基于 Labelme，Zixiang Huang 2025 年开发_
