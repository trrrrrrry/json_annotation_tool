# json_annotation_tool
一个基于 Python + PyQt5 的桌面应用，用于浏览并编辑与图像配套的 JSON 格式边界框标注。支持批量操作，一键增删改，极大提升 Labelme 标注后的后处理效率。
## 项目结构
```bash
json_annotation_tool/
├── core/
│   ├── models.py              # 数据类：Shape、AnnotationFile
│   ├── file_manager.py        # 扫描文件夹或单 JSON → 配对 JSON 与图片路径
│   └── annotation_manager.py  # load/save/add/edit/delete 核心逻辑
├── ui/
│   ├── main_window.py               # 主窗口（工具栏、状态栏、预览区域）
│   ├── preview_widget.py            # 图片预览 + 标注叠加 + 导航
│   ├── add_annotation_dialog.py     # 添加标注对话框
│   ├── edit_annotation_dialog.py    # 编辑标注对话框
│   └── delete_annotation_dialog.py  # 删除标注对话框
├── utils/
│   └── json_utils.py         # JSON 读写辅助函数
├── test_folder/              # 测试用示例 JSON/图片
├── main.py                   # 程序入口
├── requirements.txt          # 依赖列表
└── README.md                 # 项目说明
```
---
## JSON 格式示例
每个 JSON 文件至少包含一个 ```shapes``` 列表，每项示例如下：
```json
{
  "imagePath": "example.png",
  "shapes": [
    {
      "region_name": "金库",
      "is_region_flag": "true",
      "label": "标记1",
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
