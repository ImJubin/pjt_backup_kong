from rest_framework import serializers
from .models import User, Account
# from django.contrib.auth import get_user_model
# django의 내장 로그인 기능
# from django.contrib.auth import authenticate
# django의 기본 패스워드 검증 도구
from django.contrib.auth.password_validation import validate_password
# 이메일 방지를 위한 검증 도구
from rest_framework.validators import UniqueValidator
#token 모델
from rest_framework.authtoken.models import Token
from dj_rest_auth.serializers import UserDetailsSerializer
from dateutil.relativedelta import relativedelta



# User = g
# et_user_model()

#############회원가입################
class UserSignupSerializer(serializers.ModelSerializer):
    # 이메일에 대한 중복 검증
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name','phone_number')

    # password 1과 2가 둘이 일치하는지 확인
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({ "passwordError": "비밀번호와 비밀번호 확인이 일치하지 않습니다." })
        return data
    
    # 시리얼라이저 내부에 있는 create 오버라이딩
    def create(self, validated_data):
        # 확인용 비번 제거
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['phone_number'],
        )
        user.set_password(password)
        user.save()
        # 자동 로그인용 token
        # token = Token.objects.create(user=user)
        return user 
    


class CustomUserDetailsSerializer(UserDetailsSerializer): 
    class Meta(UserDetailsSerializer.Meta):
        model = User  
        fields = (
            'pk',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        )


############# 계좌 #############
# accounts/serializers.py
from rest_framework import serializers
from .models import Account, DepositDetail, SavingsDetail


# 1. 예금 상세 정보 (DepositDetail) 전체 필드 포함
class DepositDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositDetail
        fields = '__all__'  # 모든 필드 포함


# 2. 적금 상세 정보 (SavingsDetail) 전체 필드 포함
from datetime import timedelta
from rest_framework import serializers
from .models import SavingsDetail
from dateutil.relativedelta import relativedelta

from rest_framework import serializers
from .models import SavingsDetail, SavingsPayment
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

class SavingsPaymentSerializer(serializers.ModelSerializer):
    # 납입 이력 시리얼라이저 (각 회차 납입 데이터)
    class Meta:
        model = SavingsPayment
        fields = '__all__'


class SavingsDetailSerializer(serializers.ModelSerializer):
    # 계산 필드 (자동 계산)
    contract_receive_date = serializers.SerializerMethodField()   # 계약 기준 수령일 (ends_at + 1)
    expected_receive_date = serializers.SerializerMethodField()   # 납입 기준 예상 수령일 (최근 납입 기준)
    delay_days = serializers.SerializerMethodField()              # 예상 수령일 - 계약 수령일
    delay_label = serializers.SerializerMethodField()             # 연체 or 선납 표시 문자열 (D-Day / 연체 10일 등)
    calculated_ends_at = serializers.SerializerMethodField()      # 시작일 + 기간 = 계약 만기일 계산용
    delay_months = serializers.SerializerMethodField()            # 연체 개월 수 (일수 / 30 기준)
    payments = SavingsPaymentSerializer(many=True, read_only=True)  # 납입 이력 전체 포함

    class Meta:
        model = SavingsDetail
        fields = [
            'id', 'account', 'product_name', 'interest_rate',
            'duration_months', 'started_at', 'ends_at', 'goal_amount',
            'total_round', 'accumulated_delay_days', 'delay_status',

            # ⏱️ 실시간 이자 필드 추가!
            'interest_total', 'interest_accumulated', 'interest_last_updated',

            # 계산 필드
            'contract_receive_date', 'expected_receive_date',
            'delay_days', 'delay_label',
            'calculated_ends_at', 'delay_months',

            'payments'
        ]

    def get_contract_receive_date(self, obj):
        # 계약 기준 수령일 = 계약 만기일 + 1일
        if obj.ends_at:
            return obj.ends_at + timedelta(days=1)
        return None

    def get_expected_receive_date(self, obj):
        last_payment = obj.payments.order_by('-round_number').first()
        if last_payment:
            remaining = obj.total_round - last_payment.round_number
            expected_end = last_payment.paid_at + relativedelta(months=remaining)
            contract_receive = obj.ends_at + relativedelta(days=1)

            # ❗ 예상 수령일이 계약 수령일보다 빠르면 조정
            if expected_end + relativedelta(days=1) < contract_receive:
                return contract_receive

            return expected_end + relativedelta(days=1)
        return None

    def get_delay_label(self, obj):
        # 계약 수령일과 예상 수령일을 비교해서 상태 텍스트 반환
        contract = self.get_contract_receive_date(obj)
        expected = self.get_expected_receive_date(obj)

        if not contract or not expected:
            return None

        diff = (expected - contract).days

        if diff == 0:
            return "D-Day"
        elif diff > 0:
            return f"연체 {diff}일"
        else:
            return f"선납 {abs(diff)}일"

    def get_delay_days(self, obj):
        # 단순히 날짜 차이 반환 (숫자)
        contract = self.get_contract_receive_date(obj)
        expected = self.get_expected_receive_date(obj)
        if contract and expected:
            return (expected - contract).days
        return None

    def get_calculated_ends_at(self, obj):
        # 시작일 + 기간 = 계약 만기일 계산
        if obj.started_at and obj.duration_months:
            return obj.started_at + relativedelta(months=obj.duration_months)
        return None

    def get_delay_months(self, obj):
        # 연체 개월 수 (일 단위 → 월 단위 환산)
        contract = self.get_contract_receive_date(obj)
        expected = self.get_expected_receive_date(obj)
        if contract and expected:
            diff_days = (expected - contract).days
            return diff_days // 30 if diff_days > 0 else 0
        return None


# 3. 계좌 정보 + 예금/적금 중첩 포함
class AccountSerializer(serializers.ModelSerializer):
    deposit_detail = DepositDetailSerializer(read_only=True)
    savings_detail = SavingsDetailSerializer(read_only=True)

    class Meta:
        model = Account
        fields = '__all__'  # 계좌의 모든 필드 + 중첩 포함


# accounts/serializers.py Serializer – 계좌 생성용
class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'bank_name', 'account_number', 'account_type',
            'current_balance', 'is_main', 'alias_name'
        ]


from rest_framework import serializers
from .models import Account

class AccountInterestSerializer(serializers.ModelSerializer):
    interest_rate = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['bank_name', 'account_type', 'alias_name', 'interest_rate', 'account_number']

    def get_interest_rate(self, obj):
        # 적금
        if hasattr(obj, 'savings_detail'):
            return obj.savings_detail.interest_rate
        # 예금
        elif hasattr(obj, 'deposit_detail'):
            return obj.deposit_detail.interest_rate
        return None
