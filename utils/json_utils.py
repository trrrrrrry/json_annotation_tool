import json
import os

def read_json(path: str) -> dict:
    """
    读取指定路径的 JSON 文件，并返回解析后的字典。
    会对文件不存在或 JSON 格式错误进行捕获并抛出异常。
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON 文件未找到: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"无法解析 JSON 文件 {path}: {e}") from e

def write_json(path: str, data: dict) -> None:
    """
    将给定字典写出到指定路径，格式化缩进并保留非 ASCII 字符。
    如果目标目录不存在，会自动创建。
    """
    # 确保目录存在
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
