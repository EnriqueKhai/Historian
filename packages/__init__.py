import sys, os

file_path = os.path.realpath(__file__)
curr_dir  = os.path.dirname(file_path)

# Enable intra-package references.
if curr_dir not in sys.path:
    sys.path.append(curr_dir)
