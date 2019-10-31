"""
ImageUploader exception classes.
"""


class ImagePropertyTooBigError(Exception):
    """An attribute of the image falls outside the required range."""

    pass


class InvalidImageError(Exception):
    """The reference does not contain a valid image."""

    pass
