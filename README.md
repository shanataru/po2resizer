# po2resizer 
The resizer rescales the dimensions of an image to the power of 2 and tries to keep the proportions as well. It uses a Lanczos filter to resample the images.

Works with filetypes: ".jpg", ".png", ".gif", ".bmp", ".tif", ".tga"
Currently not working for subfolders. Keep all the images in one folder only. I suggest you always save the resized images in a new folder because there's no undo button if you overwrite your images in the folder.


Usage:
1. Browse an input folder with the images you want resized
2. Browse an output folder where you want to save your new resized images
3. Choose a upscale threshold. Ranges from 0.0 to 1.0
	Threshold is how close a dimension has to be to a larger power of 2 before it will be scaled up. Default is 0.5 this means that the program will choose whatever power of 2 is closer.
        It works is as follows: If you had an image of size 1280 and a threshold of 0.75, it would be scaled down to 1024 (1024 + (1024 * (1-0.75)) = 1280). Anything above 1280 would be scaled up to 2048. 
	Value of 0.5 will choose whatever power of 2 is closer.
	Value of 0.0 will always scale down (2047 will be changed to 1024).
	Value of 1.0 will always scale up (1025 will be changed to 2048).
4. Choose the maximum size of the dimensions (the highest power of two you want for your images)
5. Choose whether the images should also be converted to JPG format
6. (Optional) If you opted for JPG conversion, choose the JPG compression quality. Default value is 95
7. Press run - you can see the terminal printing image filenames that are being processed.




