from django import forms
from coreapp.models import Txt
from django.core.files.uploadedfile import InMemoryUploadedFile

# Really simple naturalsize that is missing from django humanize :( return the size of the file
def naturalsize(count):
    fcount = float(count)
    k = 1024
    m = k * k
    g = m * k
    if fcount < k:
        return str(count) + 'B'
    if fcount >= k and fcount < m:
        return str(int(fcount / (k/10.0)) / 10.0) + 'KB'
    if fcount >= m and fcount < g:
        return str(int(fcount / (m/10.0)) / 10.0) + 'MB'
    return str(int(fcount / (g/10.0)) / 10.0) + 'GB'

# Create the form class. ACHAR UM JEITO MELHOR E MAIS COMPRIENSIVEL E MALEAVEL!!!
class CreateForm(forms.ModelForm):
    max_upload_limit = 5 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'file' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    file = forms.FileField(required=True, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'pickle.dump.txt'

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Txt
        fields = ['title', 'text', 'file']  # File is manual

    # Validate the size of the file
    def clean(self):
        cleaned_data = super().clean()
        txt = cleaned_data.get('file')
        if txt is None:
            return
        if len(txt) > self.max_upload_limit:
            self.add_error('file', "File must be < "+self.max_upload_limit_text+" bytes")
            
    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        if commit:
            instance.save()

        return instance

# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other