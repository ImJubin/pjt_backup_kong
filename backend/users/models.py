from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP

# Create your models here.
class User(AbstractUser):
    # 핸드폰 번호에 대한 정보
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

class Account(models.Model):
    # 유저와 계좌 정보 1:N으로 연결해주기
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    # 은행
    bank_name = models.CharField(max_length=200)
    # 계좌 번호
    account_number = models.CharField(max_length=200)
    # 계좌 타입
    account_type = models.CharField(max_length=200)
    # 현재 잔액
    current_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    # 메인 계좌 여부
    is_main = models.BooleanField(default=False)
    # 별칭
    alias_name = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # 계좌 등록일

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

# # 적금
# models.py
from django.db import models
from django.conf import settings
from dateutil.relativedelta import relativedelta
from datetime import date

# 기존 User, Account, SavingsDetail, DepositDetail 모델 생략 (이미 존재함)

class SavingsPayment(models.Model):
    savings_detail = models.ForeignKey('SavingsDetail', on_delete=models.CASCADE, related_name='payments')
    round_number = models.IntegerField()
    paid_at = models.DateField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        unique_together = ('savings_detail', 'round_number')  # 회차 중복 방지
        ordering = ['round_number']

    def __str__(self):
        return f"{self.savings_detail.product_name} - {self.round_number}회차 납입"


from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date


class SavingsDetail(models.Model):
    # 연결된 계좌 (1:1 관계)
    account = models.OneToOneField('Account', on_delete=models.CASCADE, related_name='savings_detail')

    # 상품 정보
    product_name = models.CharField(max_length=100)                         # 상품명
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)    # 연 이자율 (%)
    duration_months = models.IntegerField()                                # 적금 기간 (개월 단위)
    started_at = models.DateField()                                        # 적금 시작일
    ends_at = models.DateField()                                           # 계약 만기일
    total_round = models.IntegerField()                                    # 총 납입 회차
    goal_amount = models.DecimalField(max_digits=18, decimal_places=2)     # 목표 총 금액

    # 상태 관련
    accumulated_delay_days = models.IntegerField(default=0)                # 누적 연체 일수 (0 이상)
    delay_status = models.CharField(max_length=20, default='정상')         # 상태: 연체 / 선납 / 정상
    interest_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)  # 전체 예상 이자 총액

    # ⏱️ 실시간 이자 시뮬레이션 관련
    interest_accumulated = models.DecimalField(max_digits=18, decimal_places=2, default=0)  # 누적 이자
    interest_last_updated = models.DateTimeField(auto_now_add=True)                         # 마지막 갱신 시각

    def __str__(self):
        return f"{self.account.alias_name or self.account.account_number} ({self.product_name})"

    def calculate_interest(self):
        principal = self.account.current_balance  # 이미 Decimal
        rate = Decimal(str(self.interest_rate)) / Decimal("100")
        duration_years = Decimal(str(self.duration_months)) / Decimal("12")

        result = principal * rate * duration_years
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_monthly_payment(self):
        """월 납입액 = 목표 금액 / 총 회차"""
        if self.total_round:
            return round(self.goal_amount / self.total_round, 2)
        return 0

    def get_contract_receive_date(self):
        """계약 기준 수령일 = 계약 만기일 다음 날"""
        return self.ends_at + relativedelta(days=1)

    def get_expected_receive_date(self):
        """예상 수령일 = 예상 만기일 다음 날"""
        expected = self.calculate_expected_ends_at()
        if expected:
            return expected + relativedelta(days=1)
        return None

    def calculate_expected_ends_at(self):
        """실제 납입 기준으로 계산된 만기일"""
        latest_payment = self.payments.order_by('-round_number').first()
        if not latest_payment:
            return None
        remaining = self.total_round - latest_payment.round_number
        return latest_payment.paid_at + relativedelta(months=remaining)

    def calculate_original_ends_at(self):
        """계약 기준 만기일 계산"""
        return self.started_at + relativedelta(months=self.total_round)

    def update_delay_status(self):
        delays = []

        for i in range(1, self.total_round + 1):
            expected_due = self.started_at + relativedelta(months=i)
            payment = self.payments.filter(round_number=i).first()

            if payment:
                delay_days = (payment.paid_at - expected_due).days
                if delay_days > 0:
                    delays.append(delay_days)
            # ❌ 미납된 회차는 계산하지 않음!

        if not self.payments.exists():
            self.delay_status = "정상"
            self.accumulated_delay_days = 0
            return

        if all((payment.paid_at - (self.started_at + relativedelta(months=payment.round_number))).days < 0
            for payment in self.payments.all()):
            self.delay_status = "선납"
            self.accumulated_delay_days = 0
        elif any((payment.paid_at - (self.started_at + relativedelta(months=payment.round_number))).days > 0
                for payment in self.payments.all()):
            self.delay_status = "연체"
            self.accumulated_delay_days = sum(delays)
        else:
            self.delay_status = "정상"
            self.accumulated_delay_days = 0



    def get_delay_label(self):
        """예상 vs 계약 만기일 비교 → D-Day, 연체, 선납"""
        actual = self.calculate_expected_ends_at()
        original = self.calculate_original_ends_at()
        if not actual or not original:
            return None

        diff_days = (actual - original).days
        if diff_days == 0:
            return "D-Day"
        elif diff_days > 0:
            return f"연체 {diff_days}일"
        else:
            return f"선납 {abs(diff_days)}일"

    def update_hourly_interest(self):
        """1시간마다 누적 이자를 계산하여 갱신"""
        now = timezone.now()
        if self.interest_last_updated:
            hours_passed = int((now - self.interest_last_updated).total_seconds() // 3600)
        else:
            hours_passed = 0

        if hours_passed > 0:
            total_hours = (self.ends_at - self.started_at).days * 24
            hourly_rate = float(self.interest_total) / total_hours if total_hours else 0

            increment = (Decimal(hourly_rate) * hours_passed).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            self.interest_accumulated += increment
            self.interest_last_updated = now
            self.save()

    def save(self, *args, **kwargs):
        if not self.interest_total or self.interest_total == 0:
            self.interest_total = self.calculate_interest()
        self.update_delay_status()
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     """저장 시 이자 계산 및 상태 업데이트 동시 수행"""
    #     self.interest_total = self.calculate_interest()
    #     self.update_delay_status()
    #     super().save(*args, **kwargs)

# 예금
class DepositDetail(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='deposit_detail')

    product_name = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()
    started_at = models.DateField()
    ends_at = models.DateField()
    interest_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    interest_accumulated = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    interest_last_updated = models.DateTimeField(auto_now_add=True)
    def update_delay_status(self):
        pass
    
    def update_hourly_interest(self):
        """1시간마다 누적 이자를 계산하여 갱신"""
        now = timezone.now()
        if self.interest_last_updated:
            hours_passed = int((now - self.interest_last_updated).total_seconds() // 3600)
        else:
            hours_passed = 0

        if hours_passed > 0:
            total_hours = (self.ends_at - self.started_at).days * 24
            hourly_rate = float(self.interest_total) / total_hours if total_hours else 0

            increment = (Decimal(hourly_rate) * hours_passed).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            self.interest_accumulated += increment
            self.interest_last_updated = now
            self.save()


    def calculate_interest(self):
        principal = self.account.current_balance  # 이미 Decimal
        rate = Decimal(str(self.interest_rate)) / Decimal("100")
        duration_years = Decimal(str(self.duration_months)) / Decimal("12")

        result = principal * rate * duration_years
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def save(self, *args, **kwargs):
        if not self.interest_total or self.interest_total == 0:
            self.interest_total = self.calculate_interest()
        self.update_delay_status()
        super().save(*args, **kwargs)
