# 修补 PIL.Image.ANTIALIAS 问题
import PIL.Image

# 检查 ANTIALIAS 是否已存在
if not hasattr(PIL.Image, 'ANTIALIAS'):
    # 添加 ANTIALIAS 属性
    try:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
    except AttributeError:
        try:
            PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
        except AttributeError:
            # 如果都不存在，使用一个整数值（0是PIL的NEAREST模式）
            PIL.Image.ANTIALIAS = 1  # 使用一个整数常量

print("已修补 PIL.Image.ANTIALIAS") 