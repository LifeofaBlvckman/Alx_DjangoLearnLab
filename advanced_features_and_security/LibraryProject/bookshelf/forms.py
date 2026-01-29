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
