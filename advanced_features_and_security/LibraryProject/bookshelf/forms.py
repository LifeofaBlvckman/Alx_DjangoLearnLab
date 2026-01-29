from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """Form for adding/editing books with validation"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'description']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    # ALX Security: Custom validation for security
    def clean_isbn(self):
        """Validate ISBN to prevent malformed data"""
        isbn = self.cleaned_data['isbn']
        if not isbn.isdigit() or len(isbn) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 digits")
        return isbn
    
    def clean_description(self):
        """Sanitize description to prevent XSS"""
        description = self.cleaned_data['description']
        # Basic sanitization - in production use a proper HTML sanitizer
        description = description.replace('<script>', '').replace('</script>', '')
        return description


# ALX REQUIREMENT: Add ExampleForm
class ExampleForm(forms.Form):
    """Example form for ALX security assignment"""
    name = forms.CharField(
        max_length=100,
        label='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    def clean(self):
        """Example of security validation"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        
        # Security: Prevent potential XSS in name field
        if name and '<script>' in name.lower():
            raise forms.ValidationError("Invalid characters in name field")
        
        return cleaned_data


# ALX Security: Another example showing secure form usage
class SearchForm(forms.Form):
    """Secure search form that prevents SQL injection"""
    query = forms.CharField(
        max_length=100,
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search safely...'})
    )
    
    def clean_query(self):
        """Sanitize search query"""
        query = self.cleaned_data['query']
        # Remove potentially dangerous characters
        dangerous = ["'", '"', ';', '--', '/*', '*/']
        for char in dangerous:
            query = query.replace(char, '')
        return query.strip()
