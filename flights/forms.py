from django import forms
from .models import Ticket

class TicketUploadForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['pdf_file']
