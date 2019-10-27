import ImageUtil

class ImageUploader():

    def __init__(self):
        self.dimension = [0,0]

    def cacheImageInMemory(self, imageFile):
        # ...
        return

    def uploadToServers(self, imageFile):
        # ...
        return

    def upload(self, imageFile):
        test = {}
        test["maxWidth"] = 10
        test["maxHeight"] = 20
        if not self.validate(imageFile, test):
            return

        self.uploadToServer(imageFile)
        self.cacheImageInMemory(imageFile)

    def validate(self, imageFile, test):
        # imageFile needs to be valid
        if imageFile is not None:
            self.dimension[0] = ImageUtil.getWidth(imageFile)
            self.dimension[1] = ImageUtil.getHeight(imageFile)

            mw = test.get("maxWidth") # maxWidth

#            if self.dimension[0] > 0 && mw > 0:
            if self.dimension[0] > 0:

                if self.dimension[0] <= mw and self.dimension[0] > 1:
                    mh = test.get("maxHeight") # maxHeight

#                    if self.dimension[1] > 0 && mh > 0:
                    if self.dimension[1] > 0:

                        if self.dimension[1] <= mh and self.dimension[1] > 1:
                            return True
                        else:
                            return False

                        return False

                    else:
                        raise Exception("Invalid height")

                else:
                    return False

            else:
                raise Exception("Invalid width")

        else:
            raise Exception("imageFile is null")