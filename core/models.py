# json_annotation_tool/core/models.py
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any

@dataclass
class Shape:
    """
    表示单个标注框的数据模型。
    """
    region_name: str  # 区域名称
    is_region_flag: str  # 标记，字符串 'true' 或 'false'
    label: str  # 标签名称
    points: Tuple[Tuple[float, float], Tuple[float, float]]  # 左上和右下坐标
    other: Dict[str, Any] = field(default_factory=dict)  # 其他任意字段

@dataclass
class AnnotationFile:
    """
    表示单个 JSON 注释文件及其关联图像和 shapes 列表。
    """
    json_path: str  # 注释 JSON 文件路径
    image_path: Optional[str]  # 关联图片路径，可为 None
    shapes: List[Shape] = field(default_factory=list)  # Shape 对象列表
