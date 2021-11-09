from django import forms
from django.core.validators import MinValueValidator

from .models import Auction, Comment, Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'image_url', 'category', 'starting_bid')
        exclude = ('owner',)

        labels = {
            'title': 'Auction title',
            'description': 'Description',
            'category': 'Category',
            'starting_bid': 'Starting bid',
            'image_url': 'Url to image'
        }

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'image_url': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'starting_bid': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1
                }
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        exclude = ('auction', 'comment_user', 'datetime')

        labels = {
            'text': 'Add comment'
        }

        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows':3, 
                    'cols':15
                }
            )
        }


class BidForm(forms.ModelForm):    
    class Meta:
        model = Bid
        fields = ('value',)
        exclude = ('auction', 'bid_user', 'datetime')

        labels = {
            'value': 'Enter bid'
        }

        widgets = {
            'value': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }
