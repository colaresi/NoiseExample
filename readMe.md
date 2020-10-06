---
title: Pittsburgh noise measurement project
author: Michael Colaresi

---

# Pittsburgh noise measurement 

This is a project to create interactive graphics from a time series of noise measurements


## Running

Once the requirements are installed (see below)

The programs can be run through your shell. 

```bash
git clone https://github.com/colaresi/NoiseExample 
cd NoiseExample 
make 
```

The visualizations should be in the propertyLineViolations and 75feetViolations folders.



## Requirements

- bash or zsh (other shells not tested)
- tail utility (should be available on any linux or mac install)
- gnu make (installed on most linux systems, available from homebrew on mac as gmake)
- yq (available [here](https://mikefarah.gitbook.io/yq/))
- python (>3.6), and modules:
   - altair 
   - pandas
   - yaml
   - numpy 








