import os
import shutil

def copy_files_recursive(path = './static', dest_path = './public'):
  if os.path.exists(dest_path):
    print(f"Deleting old '{dest_path}' directory...")
    shutil.rmtree(dest_path)
  if not os.path.exists(dest_path):
    print(f"Creating '{dest_path}' directory...")
    os.mkdir(dest_path)

  org_path = path
  def helper_func(path):
    path_list = os.listdir(path)
    for paths in path_list:
      concat_path = os.path.join(path, paths)
      if os.path.isfile(concat_path):
        cleaned_concat_path = concat_path[len(org_path)+1:-len(paths)]
        new_path = os.path.join(dest_path, cleaned_concat_path)
        print(f"Copying file '{paths}' from '{concat_path}' to '{new_path}'...")
        shutil.copy(concat_path, new_path)
      else:
        print(f"Creating new directory '{paths}'...")
        cleaned_concat_path = concat_path[len(org_path)+1:]
        os.mkdir(os.path.join(dest_path, cleaned_concat_path))
        helper_func(concat_path)
  
  helper_func(path)