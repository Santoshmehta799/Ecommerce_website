# https://www.geeksforgeeks.org/uuidfield-django-models/
import uuid
from django.utils.deconstruct import deconstructible


@deconstructible
class FileUploadPath(object):
    # print('helper file',object)

    def __init__(self, file_type):
        # print('helper file', file_type)
        self.file_type = file_type

    def __call__(self, obj, f):
        # print('helper file',obj,f)
        extension = f[f.rfind('.'):]
        # print('helper ext',extension)
        return f"proof/user_data_{obj.user.id}/{self.file_type}{uuid.uuid4()}{extension}"