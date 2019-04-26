from . import query_factory
import os, fnmatch
from app import app
import datetime
from flask import send_from_directory

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
Server_path = app.config['SERVER_PATH']


def create_url(filename):
    """
                    The function return url of the image .
                    *Parameters*:
                        - *filename (str)*: The name of the profile image.
                    *Returns*:
                        - url of image .
    """
    # Check that the file exists
    if filename is None:
        return None
    search_path = os.path.join(APP_ROOT, 'images/media')
    filename = filename + ".*"
    file_found = False
    for root, dirs, files in os.walk(search_path):
        for name in files:
            if fnmatch.fnmatch(name, filename):
                file_found = True
    # Create url
    if file_found:
        url = Server_path + 'media/get/'+ filename
    else:
        url = None
    return url


def allowed_file(filename):
    """
        The function checks if the uploaded file has allowed extension.

        *Parameters*:
            - *filename*: The name of the uploaded file .
        *Returns*:
            - *True or False*: in the allowed extension or not.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    """
        This function saves a certain file in the directory.

        *Parameters*:
            - *file (file)*: The image which will be updated.
        *Returns*:
            - *filename*: the image name saved in the media directory  .
    """
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        images = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(images):
            os.mkdir(images)
        target = os.path.join(APP_ROOT, 'images/media/')
        if not os.path.isdir(target):
            os.mkdir(target)
        filename, ext = os.path.splitext(file.filename)
        filename = str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
        filename_no_ext=filename
        filename+=ext
        destination = "/".join([target, filename])
        file.save(destination)
        return filename_no_ext
    else:
        return 'not allowed extensions'


def get_extension_file(filename):
    """
        this function gets the file extension from media directory.

        *Parameters*:
            - *filename (file)*: The filename to be searched for.
        *Returns*:
            - *filename*: file name with extension.
    """

    search_path = os.path.join(APP_ROOT, 'images/media')
    filename = filename+ ".*"
    for root, dirs, files in os.walk(search_path):
        for name in files:
            if fnmatch.fnmatch(name, filename):
                return name
    raise Exception("file is not found")


def send_file(filename):
    """
    this function sends the file from media directory .

    *Parameters*:
        - *filename (file)*: The filename to be sent.
    *Returns*:
        - *filename*: file name with extension.
    """

    os.chdir(os.path.dirname(APP_ROOT))
    return send_from_directory('images/media', filename)
