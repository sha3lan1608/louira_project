# forms.py - Create this file in your Django app directory
from django import forms
from .models import ContactInquiry


class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800",
                "placeholder": "Enter your first name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800",
                "placeholder": "Enter your last name",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800",
                "placeholder": "Enter your email address",
            }
        )
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800",
                "placeholder": "Enter your phone number",
            }
        ),
    )

    subject = forms.ChoiceField(
        choices=ContactInquiry.INQUIRY_TYPES,
        widget=forms.Select(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800"
            }
        ),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800",
                "rows": 5,
                "placeholder": "Tell us about your dream project...",
            }
        )
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and len(phone) < 10:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800",
                "placeholder": "Enter your email for updates",
            }
        )
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-gray-800",
                "placeholder": "Search collections, furniture, news...",
            }
        ),
    )
