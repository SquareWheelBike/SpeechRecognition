import os
import sys

# delete all subfolders and their contents, but not the current folder's contents
def delete_subfolders(path='.', verbose=False):
    for root, dirs, files in os.walk(".", topdown=False):
        print('root:', root) if verbose else None
        for name in dirs:
            os.rmdir(os.path.join(root, name))
            print('removed dir:', os.path.join(root, name)) if verbose else None
        for name in files:
            os.remove(os.path.join(root, name))
            print('removed file:', os.path.join(root, name)) if verbose else None

if __name__ == '__main__':
    # delete all uname folders already existing
    assert(len(sys.argv) == 2)
    delete_subfolders(path=sys.argv[1])