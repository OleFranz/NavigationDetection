# Dataset
The training code expects the following dataset format:
- The dataset should contain a set of image files in `.png`, `.jpg`, or `.jpeg` format.
- For each image file, there should be a corresponding text file with the same name and a `.txt` extension, which contains the label for that image.
- The label file should have the format: `ValueName:Value,ValueName:Value,...` where each `ValueName` can be any descriptor and does not need to be unique. Each `Value` can be either `True` or `False`.