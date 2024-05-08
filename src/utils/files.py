def slice_path_in_file(path):
    slice_index = path.rfind('/') + 1
    return path[slice_index:]
