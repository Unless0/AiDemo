"""
为整个工程提供同一的绝对路径
"""

import os


def get_project_root() -> str:
    """
    获取项目根目录
    :return:
    """
    # 当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    # 获取的工程的根目录，先获取文件所在的文件夹绝对路径
    current_dir = os.path.dirname(current_file)
    # 获取工程根目录
    projetc_root = os.path.dirname(current_dir)
    return projetc_root

def get_abs_path(relative_path):
    """
    获取绝对路径
    :param relative_path: 相对路径
    :return:
    """
    return os.path.join(get_project_root(), relative_path)

if __name__ == '__main__':
    print(get_abs_path("config\config.txt"))