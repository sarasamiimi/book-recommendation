from django import forms


class Booksearchform(forms.Form):
    book_title = forms.CharField( max_length=200  , required=False)
  
   