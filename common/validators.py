from django.core.exceptions import ValidationError
from django.core import validators


pin_validator = validators.RegexValidator(
    regex='^[0-9]{6}$'
)

phone_validator = validators.RegexValidator(
    regex='^[0-9]*$',
    message='Invalid phone number.'
)

gst_validator = validators.RegexValidator(
    regex='^[0-9][1-9][A-Z]{3}[PCHABGJLFT][A-Z][0-9]{4}[A-Z][0-9][Z][a-zA-Z0-9]$',
    message='Invalid GST Number.'
)

country_validator = validators.RegexValidator(
    regex='^[A-Z]{2}$',
    message='Invalid characters in country.'
)



def image_validator(self):
    """ This function is an amalgamation of two validations,
        file size validation, file type validation, anf file extension validation"""

    import os
    ext = os.path.splitext(self.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    # valid extension.

    if not ext.lower() in valid_extensions:
        raise ValidationError('Invalid file type/extension. Valid file types include: pdf, jpeg, gif, png, doc, odt, docx, csv, ODS ,xls, xlsx.')

    file_size = self.size

    if file_size > 2621440:  # 2.5MB
        raise ValidationError("2.5MB is The maximum file size that can be upload")
    else:
        return self