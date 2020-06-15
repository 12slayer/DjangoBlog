from django import forms
from .models import Comment

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if email.endswith(".edu"):
            raise forms.ValidationError("this is not approprate email")
        return email



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']