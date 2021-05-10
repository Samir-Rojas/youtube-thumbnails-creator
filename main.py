from image_upload import upload
from thumbnail_maker import make_thumbnail

if __name__ == '__main__':
    # set this to True if you want to automatically open the generated file
    make_thumbnail(show=False)
    # if you just want to see how the thumbnail looks, comment out the call to upload()
    upload()
