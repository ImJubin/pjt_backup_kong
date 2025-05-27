

from .api import fetch_and_save_deposit_products, fetch_and_save_savings_products
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DepositProduct, SavingsProduct

from .serializers import DepositProductDetailSerializer, SavingsProductDetailSerializer

@api_view(['GET'])
def deposit_products_view(request):
    fetch_and_save_deposit_products()
    products = DepositProduct.objects.all()
    serializer = DepositProductDetailSerializer(
        products,
        many=True,
        context={'amount': request.query_params.get('amount', 1000000)}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def savings_products_view(request):
    fetch_and_save_savings_products()
    products = SavingsProduct.objects.all()
    serializer = SavingsProductDetailSerializer(
        products,
        many=True,
        context={'amount': request.query_params.get('amount', 1000000)}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.generics import RetrieveAPIView
from .models import DepositProduct, SavingsProduct
from .serializers import DepositProductDetailSerializer, SavingsProductDetailSerializer

class DepositProductDetailView(RetrieveAPIView):
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductDetailSerializer


class SavingsProductDetailView(RetrieveAPIView):
    queryset = SavingsProduct.objects.all()
    serializer_class = SavingsProductDetailSerializer


#추천 알고리즘
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DepositProduct  # 예금 상품 모델
from users.models import Account  # 계좌 모델
from datetime import date

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Account  # 유저 계좌 모델
from .models import DepositOption  # 예금 옵션 기준 추천
from datetime import date


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    user = request.user
    amount = request.data.get('amount')

    if request.method == 'GET':
        deposit = Account.objects.filter(
            user_id=user,
            deposit_detail__isnull=False
        ).order_by('deposit_detail__ends_at').first()

        savings = Account.objects.filter(
            user_id=user,
            savings_detail__isnull=False
        ).order_by('savings_detail__ends_at').first()

        def get_ends_at(account, detail):
            return getattr(account, detail).ends_at if account else None

        d_ends = get_ends_at(deposit, 'deposit_detail')
        s_ends = get_ends_at(savings, 'savings_detail')

        if d_ends and (not s_ends or d_ends <= s_ends):
            amount = deposit.current_balance
        elif s_ends:
            amount = savings.savings_detail.goal_amount
        else:
            amount = 1000000  # fallback

        return Response({'amount': amount})
    
    # 금액이 없거나 0 이하일 경우 → 유저 계좌 중 만기 빠른 예적금 기준으로 설정
    if not amount or int(amount) <= 0:
        # 예금 계좌
        deposit = Account.objects.filter(
            user_id=user,
            deposit_detail__isnull=False
        ).order_by('deposit_detail__ends_at').first()

        # 적금 계좌
        savings = Account.objects.filter(
            user_id=user,
            savings_detail__isnull=False
        ).order_by('savings_detail__ends_at').first()

        # 만기일 비교
        def get_ends_at(account, detail):
            return getattr(account, detail).ends_at if account else None

        d_ends = get_ends_at(deposit, 'deposit_detail')
        s_ends = get_ends_at(savings, 'savings_detail')

        if d_ends and (not s_ends or d_ends <= s_ends):
            amount = deposit.current_balance
        elif s_ends:
            amount = savings.savings_detail.goal_amount
        else:
            return Response({'error': '추천 기준이 될 만기 계좌가 없습니다.'}, status=400)

    amount = int(amount)

    # 1. 예금 옵션에서 추천 기준 추출
    options = DepositOption.objects.select_related('deposit_product').all()

    product_data = []
    for option in options:
        if not option.intr_rate2 or not option.save_trm:
            continue  # 값이 없으면 스킵

        rate = float(option.intr_rate2) / 100  # 퍼센트 → 실수
        months = option.save_trm
        predicted_profit = round(amount * rate * months / 12)

        product_data.append({
            'id': option.deposit_product.id,
            'fin_prdt_nm': option.deposit_product.fin_prdt_nm,
            'kor_co_nm': option.deposit_product.kor_co_nm,
            'intr_rate2': option.intr_rate2,
            'save_trm': months,
            'predicted_profit': predicted_profit,
        })

    # 2. 정렬: 예상 수익 높은 순 → 기간 짧은 순
    product_data.sort(key=lambda x: (-x['predicted_profit'], x['save_trm']))

    # 3. 상위 3개 추천 반환
    return Response(product_data[:3])





# views.py
# from openai import OpenAI
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import DepositProduct, SavingsProduct
# from .serializers import DepositProductDetailSerializer, SavingsProductDetailSerializer
# from django.conf import settings

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# @api_view(['POST'])
# def recommend_products(request):
#     amount = int(request.data.get('amount', 1000000))
    
#     deposits = DepositProduct.objects.all()
#     savings = SavingsProduct.objects.all()

#     deposit_data = DepositProductDetailSerializer(deposits, many=True).data
#     savings_data = SavingsProductDetailSerializer(savings, many=True).data
#     all_data = deposit_data + savings_data

#     prompt = f"""
# 다음은 사용자의 예적금 상품 목록입니다. 
# 금액은 {amount}원이며, 최고 금리를 기준으로 추천 상품 3개를 골라주세요.
# 상품명, 금리, 은행명, 추천 이유를 알려주세요.

# {all_data[:10]}  # 데이터가 너무 크면 일부만 전달
# """

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=600,
#         temperature=0.7,
#     )

#     return Response({"recommendation": response.choices[0].message.content})
