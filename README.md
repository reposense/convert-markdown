## Python script to convert RepoSense code view to markdown

Usage: `reposense.py [-h] [--formats FORMATS [FORMATS ...]]
                            [--directory [DIRECTORY]]` <br/>
Sample: `python3 reposense.py --formats java fxml --directory C:\Users\user\Desktop\`

* `--formats`: File formats to be included. Default: all files will be included.
* `--directory`: Directory to perform the conversion. Default: current working directory.

The results will be generated in the current working directory's `output` folder.