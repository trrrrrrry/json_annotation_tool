# json_annotation_tool
A desktop application built with Python and PyQt5 for browsing and editing JSON‑based bounding‑box annotations linked to images. It supports batch operations—adding, deleting, and modifying annotations with a single click—dramatically streamlining the post‑processing workflow for Labelme.

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
## JSON format example
```json
{
  "imagePath": "I_am_a_picture.png",
  "shapes": [
    {
      "region_name": "I am a region！",
      "is_region_flag": "true",
      "label": "I am a label！",
      "points": [[100, 200], [400, 500]],
      "other_key": "…"    // other keys
    }
    // … more shapes
  ]
}
```
The tool will load/save any other keys and values besides the ones specified above.

---
## Features

- **One‑click batch load** (`open folder`)  
  Select a folder and the tool will automatically find and open all matching images and their `JSON` annotation files.

- **Visual preview**  
  Display each image with overlaid bounding boxes. Each box shows:
  - Index (1‑based)
  - `label`
  - `region_name`
  - `is_region_flag`

- **Add new box** (`Add Annotation`)  
  Click `Add Annotation`, enter four coordinates (`points`), select `is_region_flag`, `region_name` and `label`. The new box is added to all open `JSON` files.

- **Edit existing box** (`Edit Annotation`)  
  Click `Edit Annotation`, enter the box index, then optionally update any of:
  - `points`
  - `is_region_flag`
  - `region_name`
  - `label`

- **Delete boxes** (`Delete Annotation`)  
  Click `Delete Annotation`, specify any combination of:
  - `points`
  - `label`
  - `region_name`
  - `is_region_flag`  
  All matching boxes will be removed.

- **Bulk initialization** (`Init Annotations`)  
  For a new project, click `Init Annotations`, choose an empty image folder, enter default:
  - `points`
  - `is_region_flag`
  - `region_name`
  - `label`  
  The tool creates a new `JSON` for each image, auto‑detecting its width and height.

- **Quick navigation**  
  Use the `Previous` / `Next` buttons or the keyboard arrows (`←` / `→`) to cycle through images quickly.

---

## Installation & Usage

### 1. Using the Python package
  1. clone the project
  ```bash
     git clone https://github.com/trrrrrrry/json_annotation_tool.git
     cd json_annotation_tool
  ```
  2. Install dependencies
  ```bash
    pip install -r requirements.txt  # PyQt5, Pillow
  ```
  3. Run the application
  ```bash
    python -m json_annotation_tool. json_annotation
  ```

### 2. Using the bundled executable
  1. After building or downloading, open the `dist/` folder

  2. Double‑click `main.exe` (Windows) to launch the tool directly

  3. No Python or additional dependencies required
---

## Future Enhancements
- Draggable boxes: Drag bounding boxes directly in the preview area with immediate saving

- Zoom & pan: Support local zoom and pan to inspect details

- Multi‑select batch editing: Select multiple boxes and apply changes simultaneously

- Configuration: Customize UI settings such as colors, font sizes, and keyboard shortcuts

- Plugin extensions: Add more export formats or custom validation logic

> _Based on Labelme, developed by Zixiang Huang, 2025_
