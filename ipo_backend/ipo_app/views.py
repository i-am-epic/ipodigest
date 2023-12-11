# ipo_backend/ipo_app/views.py

from django.http import JsonResponse
from .models import IPO

def get_ipo_data(request):
    try:
        # Dummy data for demonstration purposes
        dummy_ipo_data = [
            {'slNumber': i, 'logo': f'logo{i}.png', 'name': f'Company {i}', 'symbol': f'CMP{i}',
             'priceBand': f'100-{120 + i}', 'industry': 'Tech', 'status': 'Open',
             'closeDate': '2023-12-31', 'type': 'Book Built', 'totalMarketCap': f'{i} Billion',
             'subscriptionNumber': f'{i}x'} for i in range(1, 21)
        ]

        return JsonResponse(dummy_ipo_data, safe=False)
    except Exception as e:
        print(f"Error getting IPO data: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
