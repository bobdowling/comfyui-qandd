# A collection of utility scripts for working with ComfyUI

## mdclone.py
Takes the ComfyUI workflow metadata and stuffs it into another image file (PNG only). 
Designed for when an image file created by ComfyUI is edited (and loses
its ComfyUI magic metadata inthe process).

# TO DO
* Add tests.
* Do metadata merging rather than overwriting.
* Syntactic sugar for updating a file in place.
