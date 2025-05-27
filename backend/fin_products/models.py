from django.db import models
from django.conf import settings

# 예금 상품 정보
class DepositProduct(models.Model):
    # 공시월  
    dcls_month = models.CharField(max_length=6)  
    # 금융회사 코드
    fin_co_no = models.CharField(max_length=20)
    # 금융회사명
    kor_co_nm = models.CharField(max_length=100)  
    # 금융상품코드
    fin_prdt_cd = models.CharField(max_length=100, unique=True)  
    # 상품명
    fin_prdt_nm = models.CharField(max_length=200)  
    # 가입 방법
    join_way = models.TextField()  
    # 만기 후 이자율
    mtrt_int = models.TextField()  
    # 우대 조건
    spcl_cnd = models.TextField(blank=True, null=True)  
    # 가입 대상(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()  
    # 기타 유의사항
    etc_note = models.TextField(blank=True, null=True)  
    # 최고 한도
    max_limit = models.BigIntegerField(blank=True, null=True)
    # 공시 시작일  
    dcls_strt_day = models.CharField(max_length=8)  
    # 공시 종료일
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True) 
    # 제출일 
    fin_co_subm_day = models.CharField(max_length=14)  
    # 생성일
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"


# 예금 옵션 (기간별 금리 정보)
class DepositOption(models.Model):
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name="options")
    # 저축 금리 유형 코드
    intr_rate_type = models.CharField(max_length=10)       
    # 저축 금리 유형명
    intr_rate_type_nm = models.CharField(max_length=20)    
    # 저축 기간 (단위: 개월)
    save_trm = models.IntegerField()
    # 기본 금리                       
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # 최고 우대금리
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월 ({self.intr_rate_type_nm})"



################################################################


class SavingsProduct(models.Model):
    # 공시 제출월
    dcls_month = models.CharField(max_length=6)
    # 금융회사 코드
    fin_co_no = models.CharField(max_length=20)
    # 금융회사명 
    kor_co_nm = models.CharField(max_length=100)  
    # 금융상품 코드  
    fin_prdt_cd = models.CharField(max_length=30) 
    # 상품명
    fin_prdt_nm = models.CharField(max_length=200)  
    # 가입방법
    join_way = models.TextField()  
    # 만기 후 이자율
    mtrt_int = models.TextField()  
    # 우대조건
    spcl_cnd = models.TextField()  
    # 가입제한 (1: 제한없음, 2: 서민전용, 3: 조건부 등)
    join_deny = models.CharField(max_length=5)
    # 가입 대상  
    join_member = models.TextField()  
    # 기타 유의사항
    etc_note = models.TextField(null=True, blank=True)  
    # 최고한도
    max_limit = models.BigIntegerField(null=True, blank=True)
    # 공시 시작일  
    dcls_strt_day = models.CharField(max_length=8)  
    # 공시 종료일
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True) 
    # 제출일 
    fin_co_subm_day = models.CharField(max_length=14)  
    # 생성일
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"
    


class SavingsOption(models.Model):
    product = models.ForeignKey('SavingsProduct', on_delete=models.CASCADE, related_name='options')

    # 저축 금리 유형 코드
    intr_rate_type = models.CharField(max_length=10)      
    # 저축 금리 유형명 
    intr_rate_type_nm = models.CharField(max_length=20)    
    # 적립 유형 코드
    rsrv_type = models.CharField(max_length=10)  
    # 적립 유형명          
    rsrv_type_nm = models.CharField(max_length=20)        
    # 저축 기간 (단위: 개월) 
    save_trm = models.IntegerField()                       
    # 기본 금리
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # 최고 우대금리
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월 ({self.intr_rate_type_nm})"