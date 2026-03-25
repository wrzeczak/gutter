# Gutter

Turn a highly nested directory structure into a flat one.

```
example/ ----------> gutter_output/
*- folder1/          *- IMG_1 (1).JPG
*--- IMG_1.JPG       *- IMG_1 (2).JPG
*--- IMG_2.JPG       *- IMG_1.JPG
*--- IMG_3.JPG       *- IMG_2 (1).JPG
*- folder2/          *- IMG_2 (2).JPG
*--- folderA/        *- IMG_2.JPG
*----- IMG_1.JPG     *- IMG_3 (1).JPG
*----- IMG_2.JPG     *- IMG_3.JPG
*----- IMG_3.JPG     *- IMG_4.JPG
*--- IMG_1.JPG
*--- IMG_2.JPG
```

This utility automatically creates unique filenames where collisions would exist in the output folder. By default, this utility copies, but it can also move (`-mv`) and delete subdirectories, such that `example/` above would be an empty folder after being "gutted." By default, it outputs to `./gutter_output`, but it can be redirected (`-o`). By default, it will print out information on each subfolder, but this can be silenced with (`-s`).

```
py gutter.py <input_folder> [-s/--silent] [-mv/--move_files] [-o/--output <output_folder>]
EX: py gutter.py example/
```

Try `py gutter.py -h` for more information.
