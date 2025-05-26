# commodities/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CommodityPrice
from django.utils.dateparse import parse_datetime

@api_view(['GET'])
def commodity_history(request):
    symbol = request.GET.get('symbol')
    if not symbol:
        return Response({"error": "symbol query param is required"}, status=400)

    # 최근 100개 데이터 조회 (최신순)
    prices = CommodityPrice.objects.filter(symbol=symbol).order_by('-timestamp')[:100]
    
    # 시간 순으로 다시 정렬
    prices = reversed(prices)

    data = [
        {"x": price.timestamp.isoformat(), "y": float(price.price)}
        for price in prices
    ]

    return Response(data)