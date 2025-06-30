# core/file_manager.py
import os
from typing import List, Optional
from json_annotation_tool.core.models import AnnotationFile
from json_annotation_tool.utils.json_utils import read_json

# 支持的图片扩展名
IMAGE_EXTS = ['.jpg', '.png']


def find_annotation_pairs(path: str) -> List[AnnotationFile]:
    """
    扫描给定路径，如果是文件夹，则遍历所有 .json 文件并尝试配对同名图片；
    如果是单个 JSON 文件，则仅返回该文件的 AnnotationFile 对象。
    返回的 AnnotationFile.shapes 初始化为空，由 annotation_manager 加载。
    """
    print(path)
    annotations: List[AnnotationFile] = []

    if os.path.isdir(path):
        # 遍历目录
        for fname in sorted(os.listdir(path)):
            if not fname.lower().endswith('.json'):
                continue
            json_path = os.path.join(path, fname)
            base, _ = os.path.splitext(fname)
            img_path: Optional[str] = None
            # 查找同名图片
            for ext in IMAGE_EXTS:
                candidate = os.path.join(path, base + ext)
                if os.path.isfile(candidate):
                    img_path = candidate
                    break
            annotations.append(AnnotationFile(json_path=json_path,
                                              image_path=img_path,
                                              shapes=[]))
        print("annotations loaded successfully")
    else:
        # 单个 JSON 文件
        if path.lower().endswith('.json') and os.path.isfile(path):
            annotations.append(AnnotationFile(json_path=path,
                                              image_path=None,
                                              shapes=[]))
        else:
            raise ValueError(f"路径既不是文件夹，也不是有效的 JSON 文件: {path}")

    return annotations
