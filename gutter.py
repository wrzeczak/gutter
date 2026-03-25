from os import walk, mkdir, rmdir, remove, listdir
from os.path import join, isdir, isfile, splitext
import argparse as ap
from termcolor import colored
from shutil import copyfile

#------------------------------------------------------------------------------
# ARGUMENT PARSING

argparser = ap.ArgumentParser(prog="WRZ: Gutter", description="Program to gut nested directories and dump their contents in a single folder.")
argparser.add_argument("input_folder")
argparser.add_argument("-s", "--silent", action="store_true", help="Silence all but the final two print() calls if passed.")
argparser.add_argument("-o", "--output_folder", default="gutter_output/", help="Set output folder path. By default, this is ./gutter_output/")
argparser.add_argument("-mv", "--move_files", action="store_true", help="Move files rather than copying them, deleting subfolders after they're emptied.")

args = argparser.parse_args()
input_folder_path = args.input_folder
silent = args.silent
output_folder_path = args.output_folder
move_files = args.move_files

walk_result = walk(input_folder_path, topdown=False)
if not isdir(output_folder_path):
    mkdir(output_folder_path)

#------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
# move() and copy() overwrite filenames; these functions automatically create unique ones in the typical style of `file`, `file (1)`, etc.

mvuq_depth = 0
def move_unique(root: str, path : str):
    global mvuq_depth
    basename, ext = splitext(path)
    fmtstr = f"{basename} ({mvuq_depth}){ext}" if mvuq_depth > 0 else path

    if isfile(join(output_folder_path, fmtstr)):
        mvuq_depth += 1
        move_unique(root, path)
    else:
        copyfile(join(root, path), join(output_folder_path, fmtstr))
        remove(join(root, path))
        mvuq_depth = 0

cpuq_depth = 0
def copy_unique(root: str, path: str):
    global cpuq_depth
    basename, ext = splitext(path)
    fmtstr = f"{basename} ({cpuq_depth}){ext}" if cpuq_depth > 0 else path

    # print(f"copy_unique({root}, {path}, [{cpuq_depth}]): {'not' if isfile(join(output_folder_path, path)) else 'is'} unique.")
    if isfile(join(output_folder_path, fmtstr)):
        cpuq_depth += 1
        copy_unique(root, path)
    else:
        copyfile(join(root, path), join(output_folder_path, fmtstr))
        mvuq_depth = 0

#------------------------------------------------------------------------------
# TRAVERSAL LOGIC

if not silent: 
    print(colored("Gutting", "light_yellow", attrs=["bold"]), f"\"{input_folder_path}\"...")

total_files = 0
for root, dirs, files in walk_result:
    if len(files) > 0:
        if move_files:
            for f in files:
                move_unique(root, f)
                total_files += 1
            rmdir(root)
        else:
            for f in files:
                copy_unique(root, f)
                total_files += 1

    if not silent: print(colored(root, "light_yellow", attrs=["bold"]), f"has {colored(len(dirs), "light_blue", attrs=["bold"]) if (len(dirs) > 0) else "no"} subdirecto{"ry" if len(dirs) == 1 else "ries"} and {colored(len(files), "light_blue", attrs=["bold"]) if (len(files) > 0) else "no"} file{"" if len(files) == 1 else "s"}.")

print(colored("Gutted", "light_yellow", attrs=["bold"]), f"{colored(total_files, 'light_blue' if total_files > 0 else 'light_red', attrs=['bold'])} file{'' if total_files == 1 else 's'}.")
total_dir_files = len([fname for fname in listdir(output_folder_path) if isfile(join(output_folder_path, fname))])
print(colored(output_folder_path, "light_yellow", attrs=["bold"]), f"contains {colored(total_dir_files, 'light_blue' if total_dir_files > 0 else 'light_red', attrs=['bold'])} file{'' if total_dir_files == 1 else 's'}.")