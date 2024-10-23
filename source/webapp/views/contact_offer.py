from django.shortcuts import render

def contract_offer(request):
    return render(request, 'contact_offers/contract_offer.html')

def privacy_policy(request):
    return render(request, 'contact_offers/privacy_policy.html')

def terms_of_use(request):
    return render(request, 'contact_offers/terms_of_use.html')

def product_docs(request):
    return render(request, 'contact_offers/product_docs.html')

def brand_style(request):
    return render(request, 'contact_offers/brand_style.html')
