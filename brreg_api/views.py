import requests
from django.shortcuts import render
from brreg_api.models import Company
from django.core.paginator import Paginator
from .models import Company
from django.db.models import Count
from django.http import JsonResponse

def dashboard(request):
    total_count = Company.objects.count()
    as_count = Company.objects.filter(is_as=True).count()
    bankrupt_count = Company.objects.filter(is_bankrupt=True).count()
    
    context = {
        'total_count': total_count,
        'as_count': as_count,
        'bankrupt_count': bankrupt_count,
    }
    return render(request, 'dashboard.html', context)

def get_as_count(request):
    BASE_URL = 'https://data.brreg.no/enhetsregisteret/api/enheter'
    params = {"organisasjonsform": "AS"}
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        as_count = data['page']['totalElements']
        return JsonResponse({'as_count': as_count})
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


def bankrupt_companies(request):
    return render(request, 'bankrupt_companies.html')

def get_bankrupt_companies(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    sort_by = request.GET.get('sort_by', 'name')
    search = request.GET.get('search', '')

    companies = Company.objects.filter(is_bankrupt=True)

    if search:
        companies = companies.filter(name__icontains=search)

    if sort_by == 'name':
        companies = companies.order_by('name')
    elif sort_by == 'kommunenummer':
        companies = companies.order_by('forretningsadresse__kommunenummer')
    elif sort_by == 'postnummer':
        companies = companies.order_by('forretningsadresse__postnummer')

    paginator = Paginator(companies, per_page)

def as_companies(request):
    as_count = Company.objects.filter(is_as=True).count()
    context = {
        'as_count': as_count,
    }
    return render(request, 'as_companies.html', context)