#!/usr/bin/env python3
# © Bob Dowling, <bob.dowling.64@gmail.com>

# TO DO: Better metadata merging.

import argparse

import PIL.Image

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#png
# n.b. the caution to use load()
import PIL.PngImagePlugin


def md_merge(
    image_filename: str,
    mdata_filename: str,
    merge_filename: str,
) -> None:
    """md_merge(): A quick & dirty ComfyUI workflow+prompt metadata copier.

    image_filename: The file to take the image data from.
        e.g. after you have edited it to add a logo and blown away ComfyUI’s workflow metadata.
    mdata_filename: The file to take the ComfyUI metadata from.
        e.g. the original file from ComfyUI before you edited it
    merge_filename: The file to create with the image from image_filename and the ComfyUI metadata from mdata_filename
    """
    with PIL.Image.open(mdata_filename) as mdata_source:
        mdata_source.load()
        if mdata_source.format != "PNG":
            raise ValueError(
                f"Metadata source file must be PNG: {mdata_filename}: {mdata_source.format}"
            )
        mdata = mdata_source.text

    pnginfo = PIL.PngImagePlugin.PngInfo()

    for key, value in mdata.items():
        pnginfo.add_text(key, value)

    with PIL.Image.open(image_filename) as image_source:
        image_source.load()
        if image_source.format != "PNG":
            raise ValueError(
                f"Image source file must be PNG: {image_filename}: {image_source.format}"
            )

    image_source.save(merge_filename, pnginfo=pnginfo, format="PNG")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="""Take (in order) the filenames of:
a PNG file with image data,
a PNG file with ComfyUI metadata, and
a PNG file to be created which has the image from the first and the ComfyUI metadata from the second.
NB1: This ignores any text metadata that might have been in the image source. 
NB2: Over-writing in place is possible but not required.
""",
    )
    parser.add_argument(
        "image_filename", help="Name of the file to take the image data from."
    )
    parser.add_argument(
        "mdata_filename", help="Name of the file to take the ComfyUI metadata from."
    )
    parser.add_argument("merge_filename", help="Name of the file to create.")
    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    md_merge(args.image_filename, args.mdata_filename, args.merge_filename)
