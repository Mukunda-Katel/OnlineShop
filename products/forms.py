from django import forms 
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'stock']
        widgets= {
            'name' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter product name'
            }),
            'description': forms.Textarea( attrs={
                'class': 'form-control',
                'row':4,
                'placeholder':'Enter product description' 
            }),
            'price':forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter product name',
                'step':'0.01',
                'min':'0'
            }),
            'category':forms.Select(attrs={
                'class': 'form-control'
            }),
            
            'image':forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'stock':forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter product stock',
                'min':'0'
            })
        }
        
        
        