from copystatic import copy_files_recursive

static_path = './static'
public_path = './public'

def main():
  print('Copying static files to public directory...')
  copy_files_recursive(static_path, public_path)


main()