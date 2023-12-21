from django import forms

class OTPField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super(OTPField, self).__init__(*args, **kwargs)
        self.validators.append(self.validate_length)

    def validate_length(self, value):
        if len(value) != 6:
            raise forms.ValidationError('OTP must be 6 digits.')