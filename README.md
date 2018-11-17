## Python script to convert RepoSense code view to markdown

Usage: `reposense.py [-h] [--formats FORMATS [FORMATS ...]] [--directory [DIRECTORY]] [--minlines [MINLINES]] 
        [--datadir [DATADIR]] [--subdir [SUBDIR]]` <br/>
Sample: `python3 reposense.py --formats java fxml --directory C:\Users\user\Desktop\ --datadir src/main --subdir functional`

* `--formats`: File formats to be included. Default: all files will be included.
* `--directory`: Directory that contains the `reposense-report`. Default: looks for `reposense-report` in the current working directory.
* `--minlines`: Minimum number of consecutive lines for acceptance. 
Chunks that does not meet the requirement will not be extracted to the markdown file. Default: 3.
* `--datadir`: Data files' directory to be included. Default: all data files will be included.
* `--subdir`: Create a sub-directory in the group folder to store the author files.
Default: author files will be placed directly in the group folder.



The results will be generated in the current working directory's `output` folder.