"""
ImageUploader exception classes.
"""


class ImagePropertySizeError(Exception):
    """An attribute of the image falls outside the required range."""

    def __init__(self, message):
        self.message = message


class InvalidImageError(Exception):
    """The reference does not contain a valid image."""

    def __init__(self, message):
        self.message = message
