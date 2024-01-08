from django import forms
from .models import ClientRequest, CollectorReport, User

class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequest
        fields = ['location', 'type_of_waste']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname' ,'mobile_number' ,'collector']

# forms.py
class ReportForm(forms.ModelForm):
    class Meta:
        model = CollectorReport
        fields = ['client_request', 'material', 'quantity', 'detail', 'finalprice']

    def __init__(self, request_id,*args, **kwargs):
        collector = kwargs.pop('collector', None)
        client_request_id = kwargs.pop('client_request_id', request_id)
        super(ReportForm, self).__init__(*args, **kwargs)

        if collector and client_request_id:
            # Get the requests allocated to the collector
            allocated_requests = ClientRequest.objects.filter(
                allocation__collector=collector
            )

            # Exclude requests made by the collector
            allocated_requests = allocated_requests.exclude(
                user=collector
            )

            # Set the initial value for the client_request field
            self.fields['client_request'].initial = client_request_id
            self.fields['client_request'].disabled = True  # Mark the field as disabled

class ReportForm2(forms.ModelForm):
    class Meta:
        model = CollectorReport
        fields = ['transaction_completed']
        
class CollectorReportForm(forms.ModelForm):
    class Meta:
        model = CollectorReport
        fields = ['client_request', 'material', 'quantity', 'detail', 'finalprice']
        
    def __init__(self, *args, **kwargs):
        collector = kwargs.pop('collector', None)
        super(CollectorReportForm, self).__init__(*args, **kwargs)
        if collector:
            # Get the requests allocated to the collector
            allocated_requests = ClientRequest.objects.filter(
                allocation__collector=collector
            )