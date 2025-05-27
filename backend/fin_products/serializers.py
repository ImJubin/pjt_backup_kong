from rest_framework import serializers
from .models import DepositOption, DepositProduct, SavingsOption, SavingsProduct


# ✅ 1. 예금 옵션 시리얼라이저
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'


# ✅ 2. 예금 상세 시리얼라이저
class DepositProductDetailSerializer(serializers.ModelSerializer):
    options = DepositOptionSerializer(many=True, read_only=True)
    bestRate = serializers.SerializerMethodField()
    predictedProfit = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = DepositProduct
        fields = [
            'id', 'dcls_month', 'fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm',
            'join_way', 'mtrt_int', 'spcl_cnd', 'join_member', 'etc_note',
            'max_limit', 'dcls_strt_day', 'dcls_end_day', 'fin_co_subm_day', 'created_at',
            'options', 'bestRate', 'predictedProfit','type'
        ]
    
    def get_type(self, obj):
        return 'deposit'

    def get_bestRate(self, obj):
        options = obj.options.all()
        if not options:
            return None
        max_option = options.order_by('-intr_rate2').first()
        return float(max_option.intr_rate2) if max_option.intr_rate2 else None

    def get_predictedProfit(self, obj):
        try:
            amount = int(self.context.get('amount', 1000000))
        except:
            return None
        rate = self.get_bestRate(obj)
        if rate is None:
            return None
        return int(amount * (rate / 100))


# ✅ 3. 예금 기본 정보용 시리얼라이저 (선택)
class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'


# ✅ 4. 적금 옵션 시리얼라이저
class SavingsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsOption
        fields = '__all__'


# ✅ 5. 적금 상세 시리얼라이저
class SavingsProductDetailSerializer(serializers.ModelSerializer):
    options = SavingsOptionSerializer(many=True, read_only=True)
    bestRate = serializers.SerializerMethodField()
    predictedProfit = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = SavingsProduct
        fields = [
            'id', 'dcls_month', 'fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm',
            'join_way', 'mtrt_int', 'spcl_cnd', 'join_deny', 'join_member',
            'etc_note', 'max_limit', 'dcls_strt_day', 'dcls_end_day',
            'fin_co_subm_day', 'created_at',
            'options', 'bestRate', 'predictedProfit','type'
        ]

    def get_type(self, obj):
        return 'savings'

    def get_bestRate(self, obj):
        options = obj.options.all()
        if not options:
            return None
        max_option = options.order_by('-intr_rate2').first()
        return float(max_option.intr_rate2) if max_option.intr_rate2 else None

    def get_predictedProfit(self, obj):
        try:
            amount = int(self.context.get('amount', 1000000))
        except:
            return None
        rate = self.get_bestRate(obj)
        if rate is None:
            return None
        return int(amount * (rate / 100))


# ✅ 6. 적금 기본 정보용 시리얼라이저 (선택)
class SavingsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProduct
        fields = '__all__'
