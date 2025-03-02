from django import forms
from .models import Promotion, Watch, Brand, Warranty, WatchFeature, Feature, MovementType, Material, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date, datetime


class WatchFilterForm(forms.Form):
    name = forms.CharField(label='Name', required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, label='Brand')
    min_price = forms.DecimalField(label='Min Price', required=False, min_value=0)
    max_price = forms.DecimalField(label='Max Price', required=False, min_value=0)
    min_water_resistance = forms.IntegerField(label='Min Water Resistance (m)', required=False, min_value=0)
    movement_type = forms.ModelChoiceField(queryset=MovementType.objects.all(), required=False, label='Movement Type')
    warranty = forms.ModelChoiceField(queryset=Warranty.objects.all(), required=False, label='Warranty')
    material = forms.ModelChoiceField(queryset=Material.objects.all(), required=False, label='Material')
    feature = forms.ModelChoiceField(queryset=Feature.objects.all(), required=False, label='Feature')


class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="fil in your birth date (format YYYY-MM-DD)."
    )
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        help_text="Fill in a valid phone number, ex: +40712345678."
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Fill in the full address"
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Write a bit about yourself",
    )
    has_premium = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Check if you want premium account"
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name',
            'date_of_birth', 'phone_number', 'address', 'bio', 'has_premium')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.date_of_birth = self.cleaned_data["date_of_birth"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.address = self.cleaned_data["address"]
        user.bio = self.cleaned_data['bio']
        user.has_premium = self.cleaned_data['has_premium']
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=10,
        required=True,
        label="Name",
        error_messages={'required': 'Name is required.'},
        widget=forms.TextInput(attrs={'placeholder': 'Name'})
    )
    surname = forms.CharField(
        required=False,
        label="Surname",
        widget=forms.TextInput(attrs={'placeholder': 'Surname'})
    )
    birthdate = forms.DateField(
        required=True,
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    confirm_email = forms.EmailField(
        required=True,
        label="Confirm Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Confirm Email'})
    )
    message_type = forms.ChoiceField(
        choices=[
            ('reclamatie', 'Complaint'),
            ('intrebare', 'Question'),
            ('review', 'Review'),
            ('cerere', 'Request'),
            ('programare', 'Appointment')
        ],
        required=True,
        label="Message Type"
    )
    subject = forms.CharField(
        required=True,
        label="Subject",
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})
    )
    min_wait_days = forms.IntegerField(
        required=True,
        label="Minimum Wait Days",
        min_value=1,
        widget=forms.NumberInput()
    )
    message = forms.CharField(
        required=True,
        label="Message (Please sign at the end)",
        widget=forms.Textarea(attrs={'placeholder': 'Type your message here...'}),
    )

    def clean_birthdate(self):
        birthdate = self.cleaned_data['birthdate']
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old.")
        return birthdate

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        message = cleaned_data.get("message")
        name = cleaned_data.get("name")

        if email and confirm_email and email != confirm_email:
            self.add_error('confirm_email', "Emails do not match.")

        if message:
            word_count = len(message.split())
            if word_count < 5 or word_count > 100:
                self.add_error('message', "Message must contain between 5 and 100 words.")
            if "http://" in message or "https://" in message:
                self.add_error('message', "Message cannot contain links.")
            if not message.strip().endswith(name):
                self.add_error('message', "Message must end with your name as a signature.")
        return cleaned_data

class WatchForm(forms.ModelForm):
    purchase_date = forms.DateField(
        required=True,
        label="Purchase Date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Enter the date the watch was purchased."
    )
    estimated_usage_years = forms.ChoiceField(
    required=True,
    label="Estimated Usage (Years)",
    help_text="Select the number of years you expect to use the watch.",
    choices=[(2, "2 years"), (5, "5 years")], 
    error_messages={
        'required': "Please select the estimated usage in years.",
        'invalid_choice': "Please select a valid option (2 or 4)."
    },
    widget=forms.Select
)

    class Meta:
        model = Watch
        fields = ['name', 'brand', 'price', 'water_resistance']
        labels = {
            'name': "Watch Name",
            'brand': "Brand Name",
            'price': "Price (USD)",
            'water_resistance': "Water Resistance (meters)"
        }
        help_texts = {
            'price': "Enter the retail price in USD."
        }
        error_messages = {
            'name': {
                'max_length': "The watch name cannot exceed 100 characters."
            },
            'price': {
                'required': "Please provide a price.",
                'invalid': "Please enter a valid decimal value."
            },
            'water_resistance': {
                'required': "Please specify the water resistance level in meters.",
                'invalid': "This field accepts only integer values."
            }
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError("The price must be greater than zero.")
        return price

    def clean_water_resistance(self):
        water_resistance = self.cleaned_data.get('water_resistance')
        if water_resistance and water_resistance < 0:
            raise forms.ValidationError("Water resistance cannot be negative.")
        return water_resistance

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.istitle():
            raise forms.ValidationError("The watch name must start with an uppercase letter.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        purchase_date = cleaned_data.get('purchase_date')
        estimated_usage_years = cleaned_data.get('estimated_usage_years')

        if purchase_date and estimated_usage_years:
            today = datetime.today().date()
            estimated_usage_years = int(estimated_usage_years)
            totalUsageTime = int(estimated_usage_years) - today.year - purchase_date.year
            if purchase_date > today:
                raise forms.ValidationError("Purchase date cannot be in the future.")
            if totalUsageTime <= 0:
                raise forms.ValidationError("Estimated usage must be greater than zero.")

        return cleaned_data

    def save(self, commit=True):
        watch = super().save(commit=False)
        purchase_date = self.cleaned_data.get('purchase_date')
        estimated_usage_years = self.cleaned_data.get('estimated_usage_years')
        
        if purchase_date and estimated_usage_years:
            totalUsageTime = int(estimated_usage_years) - datetime.today().date().year - purchase_date.year
            if totalUsageTime <= 4:
                watch.warranty = Warranty.objects.filter(duration_years=2)[0] 
            else:
                watch.warranty = Warranty.objects.filter(duration_years=5)[0]
        if commit:
            watch.save()
        return watch


class CustomAuthenticationForm(AuthenticationForm):
    stay_logged_in = forms.BooleanField(
        required=False,
        initial=False,
        label= "Stay logged in"
    )
    def clean(self):
        cleaned_data = super().clean()
        stay_logged_in = self.cleaned_data.get('stay_logged_in')
        return cleaned_data

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['name', 'expires_at', 'subject', 'message', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(), 
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }