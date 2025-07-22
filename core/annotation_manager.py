# json_annotation_tool/core/annotation_manager.py
from PIL import Image
import json
import os
from typing import Dict, Tuple, Optional, Any
from core.models import AnnotationFile, Shape
from utils.json_utils import read_json, write_json


def load_annotation(
    json_path: str,
    default_image_path: Optional[str] = None
) -> AnnotationFile:
    """
    从 JSON 文件读取并解析成 AnnotationFile 对象。
    支持从 JSON 内部或默认路径获取图片。
    """
    data = read_json(json_path)

    raw_image = data.get('imagePath') or data.get('image_path') or default_image_path
    image_path = None
    if raw_image:
        if not os.path.isabs(raw_image):
            image_path = os.path.join(os.path.dirname(json_path), raw_image)
        else:
            image_path = raw_image

    ann = AnnotationFile(json_path=json_path, image_path=image_path)
    for s in data.get('shapes', []):
        region_name    = s.get('region_name', '')
        is_region_flag = s.get('is_region_flag', '')
        label          = s.get('label', '')
        pts            = s.get('points', [])
        if len(pts) < 2:
            continue
        p1 = tuple(pts[0])
        p2 = tuple(pts[1])
        other = {
            k: v for k, v in s.items()
            if k not in ('region_name', 'is_region_flag', 'label', 'points')
        }
        shape = Shape(
            region_name=region_name,
            is_region_flag=is_region_flag,
            label=label,
            points=(p1, p2),
            other=other
        )
        ann.shapes.append(shape)
    return ann


def save_annotation(ann: AnnotationFile) -> None:
    """
    将 AnnotationFile 写回 JSON 文件，更新 shapes 字段。
    """
    data = read_json(ann.json_path)
    data['shapes'] = []
    for shp in ann.shapes:
        entry = {
            'region_name': shp.region_name,
            'is_region_flag': shp.is_region_flag,
            'label': shp.label,
            'points': [
                [shp.points[0][0], shp.points[0][1]],
                [shp.points[1][0], shp.points[1][1]]
            ]
        }
        entry.update(shp.other)
        data['shapes'].append(entry)
    write_json(ann.json_path, data)


def add_shape_to_file(
    json_path: str,
    is_region_flag: str,
    coords: Tuple[float, float, float, float],
    template_idx: Optional[int] = None,
    region_name: Optional[str] = None,
    label: Optional[str] = None
) -> None:
    """
    在 JSON 中添加新的 shape，可覆盖 region_name 和 label。
    """
    ann = load_annotation(json_path, default_image_path=None)

    if template_idx is None:
        new_region = region_name or ''
        new_label = label or ''
        other = {}
    else:
        if template_idx < 0 or template_idx >= len(ann.shapes):
            raise IndexError(f"Template index out of range: {template_idx}")
        tpl = ann.shapes[template_idx]

        new_region = region_name if region_name is not None else tpl.region_name
        new_label  = label        if label        is not None else tpl.label

        other = tpl.other.copy()

    p1 = (coords[0], coords[1])
    p2 = (coords[2], coords[3])

    new_shape = Shape(
        region_name=new_region,
        is_region_flag=is_region_flag,
        label=new_label,
        points=(p1, p2),
        other=other
    )
    ann.shapes.append(new_shape)
    save_annotation(ann)


def edit_shape_in_file(
    json_path: str,
    shape_idx: int,
    updates: Dict[str, Any]
) -> None:
    """
    修改指定 shape 的字段。
    updates 支持：
      - 'points': Tuple[x1, y1, x2, y2]
      - 'region_name', 'is_region_flag', 'label', 或任意其它字段
    """
    ann = load_annotation(json_path, default_image_path=None)
    if shape_idx < 0 or shape_idx >= len(ann.shapes):
        raise IndexError(f"Shape index out of range: {shape_idx}")
    shp = ann.shapes[shape_idx]

    for key, val in updates.items():
        if key == 'points' and isinstance(val, (list, tuple)) and len(val) == 4:
            shp.points = ((val[0], val[1]), (val[2], val[3]))
        elif hasattr(shp, key):
            setattr(shp, key, val)
        else:
            shp.other[key] = val

    save_annotation(ann)


def delete_shapes_in_file(
    json_path: str,
    criteria: Dict[str, Any]
) -> None:
    """
    根据 criteria 删除符合条件的 shapes。
    """
    ann = load_annotation(json_path, default_image_path=None)

    def matches(shp: Shape) -> bool:
        for key, val in criteria.items():
            if key == 'points':
                pts = ((val[0], val[1]), (val[2], val[3]))
                if shp.points != pts:
                    return False
            elif hasattr(shp, key):
                if getattr(shp, key) != val:
                    return False
            else:
                if shp.other.get(key) != val:
                    return False
        return True

    ann.shapes = [shp for shp in ann.shapes if not matches(shp)]
    save_annotation(ann)

def create_initial_annotations(
    folder: str,
    is_region_flag: str,
    region_name: str,
    label: str,
    coords: Tuple[float, float, float, float],
    version: str = '5.2.1',
    shape_type: str = 'rectangle'
) -> None:
    """
    为 folder 下的每张图片创建一个 JSON:
    - imagePath: 文件名
    - imageHeight/Width: 读取自图片
    - shapes: 只有一个元素，带 flag/name/label/points + 默认模板字段
    """
    IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.bmp']
    for fname in sorted(os.listdir(folder)):
        base, ext = os.path.splitext(fname)
        if ext.lower() not in IMAGE_EXTS:
            continue
        img_fp = os.path.join(folder, fname)
        with Image.open(img_fp) as img:
            w, h = img.size

        json_fp = os.path.join(folder, base + '.json')
        shape = {
            'is_region_flag': is_region_flag,
            'region_name':    region_name,
            'label':          label,
            'points':         [[coords[0], coords[1]], [coords[2], coords[3]]],
            'group_id':       None,
            'description':    '',
            'shape_type':     shape_type,
            'flags':          {},
            "mask":           None

        }
        data = {
            'version':     version,
            'flags':       {},
            'shapes':      [shape],
            'imagePath':   fname,
            "imageData": None,
            'imageHeight': h,
            'imageWidth':  w,
            "metadata": {},
            "imageID": None
        }
        with open(json_fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)