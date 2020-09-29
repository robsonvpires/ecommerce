from django.forms import *
from .models import *

class ListingForm(ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all(), widget=Select)

    class Meta:
        model = Listing
        fields = [
            'name', 'price', 'description', 'category', 'image'
        ]
        widgets = {
            'name': TextInput(attrs={'class' : 'form-control','placeholder':'Insert the name of the listing'}),
            'price': NumberInput(attrs={'class' : 'form-control','placeholder':'Insert the value of the listing'}),
            'description': Textarea(attrs={'class' : 'form-control','placeholder':'Insert the description of the listing'}),
            'image': URLInput(attrs={"class": "form-control","placeholder": "URL Link"})
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
        widgets = {
            'content': Textarea(attrs={
                'class' : 'form-control',
                'placeholder':'Insert your comment here'
            })
        }

        labels = {
            'content': 'comment',
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']
        widgets = {
            'value': NumberInput(attrs={
                'class' : 'form-control',
                'placeholder':'Insert your bid here'
            })
        }