#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def create_symlinks():
    # 定义源目录和目标目录
    source_dir = '/Users/zhangxy/GAFile/产品设计开发规范'
    target_dir = os.getcwd()  # 使用当前工作目录作为目标目录

    print(f'源目录: {source_dir}')
    print(f'目标目录: {target_dir}')

    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f'错误: 源目录 {source_dir} 不存在!')
        return False

    try:
        # 遍历源目录中的所有文件
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            target_path = os.path.join(target_dir, item)

            # 如果目标路径已存在，先删除
            if os.path.exists(target_path):
                if os.path.islink(target_path):
                    os.unlink(target_path)
                    print(f'已删除现有链接: {item}')
                elif os.path.isdir(target_path):
                    shutil.rmtree(target_path)
                    print(f'已删除现有目录: {item}')
                else:
                    os.remove(target_path)
                    print(f'已删除现有文件: {item}')

            # 创建软链接
            os.symlink(source_path, target_path)
            print(f'已创建链接: {item}')

    except PermissionError:
        print('错误: 没有足够的权限执行操作!')
        return False
    except OSError as e:
        print(f'系统错误: {str(e)}')
        return False
    except Exception as e:
        print(f'发生未知错误: {str(e)}')
        return False

    print('所有文件链接创建完成！')
    return True

if __name__ == '__main__':
    create_symlinks() 