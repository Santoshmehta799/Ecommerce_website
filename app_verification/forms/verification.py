from django import forms
from app_verification.models import GstDetail


class GstDetailForms(forms.ModelForm):
    half_2 = []
    half_3 = []
    half_4 = []
    half = []
    half_7 = []
    half_8 = []
    half_9 = []
    half_10 = []

    company_gst_number = forms.CharField(
        max_length=15,
        label="GST No.",
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'GST No.',
                'oninput': 'this.value = this.value.toUpperCase();',
            }
        ),
    )

    field_order = ['company_gst_number',]

    class Meta:
        model = GstDetail
        fields = ['company_gst_number',]
        
    def __init__(self, *args, **kwargs):
        super(GstDetailForms, self).__init__(*args, **kwargs)
