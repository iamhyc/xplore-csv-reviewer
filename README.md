## XPlore CSV Reviewer

provide item/list colorful review for IEEE Xplore search results

### Sample

![Sample](./Sample.gif)

(black background for better experience, `cmder` for Windows is recommended)

### Instructions

1. python 2.7.x and run `setup.py` in this repo (Windows only, linux user can diy)
2. save your Xplore search results and convert into `,` splitted format (maybe with Microsoft Excel)
3. run `python csv-reviewer.py <path-to-your-csv-file> -b <long_number>` (-l for list-review mode)
4. select the columns index you want to display (split by SPACE)
5. use `Left Arrow` `Right Arrow` `Page Up` `Page Down` for quick navigation

### TODO

* list view mode
* align text print with getConsoleWidth
* reduce keyboard hook range and function
* xplore search integrated, lite database for parsing storage
* (optional) record display sequence order