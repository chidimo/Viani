from django.shortcuts import render

def gallery(request):
    template = 'shop/gallery.html'
    context = {}
    return render(request, template, context)
