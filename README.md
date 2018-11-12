## Python script to convert RepoSense code view to markdown

Usage: `reposense.py [-h] [--formats FORMATS [FORMATS ...]]
                            [--directory [DIRECTORY]]` <br/>
Sample: `python3 reposense.py --formats java fxml --directory C:\Users\user\Desktop\`

* `--formats`: File formats to be included. Default: all files will be included.
* `--directory`: Directory to perform the conversion. Default: current working directory.
* `--minlines`: Minimum number of consecutive lines for acceptance. 
Chunks that does not meet the requirement will not be extracted to the markdown file. Default: 3.

The results will be generated in the current working directory's `output` folder.