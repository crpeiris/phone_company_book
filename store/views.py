from django.shortcuts import render


# This view returns the 'storehome.html' file.
def storehome(request):
    return render(request, 'store/storehome.html', {})


# This view returns the 'store/aboutus.html' file.
def aboutus(request):
    return render(request, 'store/aboutus.html', {'title': 'About Us'})


# This view returns the 'store/reviews.html' file.
def reviews(request):
    return render(request, 'store/reviews.html', {'title': 'Reviews'})

# This view returns the 'store/shop.html' file.
def shop(request):
    return render(request, 'store/shop.html', {'title': 'All Phones'})
