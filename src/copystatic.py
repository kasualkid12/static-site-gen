import os
import shutil

def copy_files_recursive(path = './static', dst_path = './public'):
  if os.path.exists(dst_path):
    print(f"Deleting old '{dst_path}' directory...")
    shutil.rmtree(dst_path)
  if not os.path.exists(dst_path):
    print(f"Creating '{dst_path}' directory...")
    os.mkdir(dst_path)

  org_path = path
  def helper_func(path):
    path_list = os.listdir(path)
    for paths in path_list:
      concat_path = os.path.join(path, paths)
      if os.path.isfile(concat_path):
        cleaned_concat_path = concat_path[len(org_path)+1:-len(paths)]
        new_path = os.path.join(dst_path, cleaned_concat_path)
        print(f"Copying file '{paths}' from '{concat_path}' to '{new_path}'...")
        shutil.copy(concat_path, new_path)
      else:
        print(f"Creating new directory '{paths}'...")
        cleaned_concat_path = concat_path[len(org_path)+1:]
        os.mkdir(os.path.join(dst_path, cleaned_concat_path))
        helper_func(concat_path)
  
  helper_func(path)