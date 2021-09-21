from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput( attrs={
        'placeholder':'Enter Password',
        'class' : 'form-control',
    }))

    confirm_password = forms.CharField(widget = forms.PasswordInput( attrs={
        'placeholder':'Enter Password',
        'class' : 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_no','password']

    def __init__(self, *args, **kwargs):

        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            placehold = field.split('_')

            try:
                placehold = 'Enter ' +placehold[0] + ' ' + placehold[1]
            except:
                placehold = 'Enter '  + placehold[0]

            self.fields[field].widget.attrs={
                'placeholder': placehold,
                'class' : 'form-control'}

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            print(cleaned_data)
            raise forms.ValidationError(
                "Password  and Confirm Password doesn't match"
            )

