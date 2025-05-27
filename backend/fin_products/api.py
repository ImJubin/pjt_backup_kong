import requests
from django.conf import settings
from .models import DepositProduct, DepositOption, SavingsProduct, SavingsOption
from django.conf import settings

api_key = settings.FSS_API_KEY

def fetch_and_save_deposit_products():
    # 기존 예금 상품 전체 삭제
    DepositProduct.objects.all().delete()

    # 예금 조회 요청 URL
    url = "https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {
        "auth": api_key,
        # 권역코드(은행)
        "topFinGrpNo": "020000",
        # api page
        "pageNo": 1  
    }

    response = requests.get(url, params=params)
    data = response.json()
    # 상품 종류
    base_list = data["result"]["baseList"]
    # 상품 옵션들
    option_list = data["result"]["optionList"]


    for product_data in base_list:
        product = DepositProduct.objects.create(
            dcls_month=product_data["dcls_month"],
            fin_co_no=product_data["fin_co_no"],
            kor_co_nm=product_data["kor_co_nm"],
            fin_prdt_cd=product_data["fin_prdt_cd"],
            fin_prdt_nm=product_data["fin_prdt_nm"],
            join_way=product_data["join_way"],
            mtrt_int=product_data["mtrt_int"],
            spcl_cnd=product_data.get("spcl_cnd"),
            join_member=product_data["join_member"],
            etc_note=product_data.get("etc_note"),
            max_limit=product_data.get("max_limit"),
            dcls_strt_day=product_data["dcls_strt_day"],
            dcls_end_day=product_data.get("dcls_end_day"),
            fin_co_subm_day=product_data["fin_co_subm_day"],
        )

        # 옵션 연결: 상품코드 & 금융회사코드 둘 다 일치하는 옵션만 저장
        for option_data in option_list:
            if (
                option_data["fin_prdt_cd"] == product.fin_prdt_cd and
                option_data["fin_co_no"] == product.fin_co_no
            ):
                DepositOption.objects.create(
                    deposit_product=product,
                    intr_rate_type=option_data.get("intr_rate_type", ""),
                    intr_rate_type_nm=option_data.get("intr_rate_type_nm", ""),
                    save_trm=int(option_data["save_trm"]),
                    intr_rate=option_data.get("intr_rate"),
                    intr_rate2=option_data.get("intr_rate2"),
                )


#################################################################################


def fetch_and_save_savings_products():
    # 기존 적금 상품 전체 삭제
    SavingsProduct.objects.all().delete()

    url = "https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    params = {
        "auth": settings.FSS_API_KEY,
        "topFinGrpNo": "020000",  # 은행
        "pageNo": 1,
    }

    response = requests.get(url, params=params)
    data = response.json()

    base_list = data["result"]["baseList"]
    option_list = data["result"]["optionList"]

    for product_data in base_list:
        product = SavingsProduct.objects.create(
            dcls_month=product_data["dcls_month"],
            fin_co_no=product_data["fin_co_no"],
            kor_co_nm=product_data["kor_co_nm"],
            fin_prdt_cd=product_data["fin_prdt_cd"],
            fin_prdt_nm=product_data["fin_prdt_nm"],
            join_way=product_data["join_way"],
            mtrt_int=product_data["mtrt_int"],
            spcl_cnd=product_data["spcl_cnd"],
            join_deny=product_data["join_deny"],
            join_member=product_data["join_member"],
            etc_note=product_data.get("etc_note"),
            max_limit=product_data.get("max_limit"),
            dcls_strt_day=product_data["dcls_strt_day"],
            dcls_end_day=product_data.get("dcls_end_day"),
            fin_co_subm_day=product_data["fin_co_subm_day"],
        )

        for option_data in option_list:
            if (
                option_data["fin_prdt_cd"] == product.fin_prdt_cd and
                option_data["fin_co_no"] == product.fin_co_no
            ):
                SavingsOption.objects.create(
                    product=product,
                    intr_rate_type=option_data.get("intr_rate_type", ""),
                    intr_rate_type_nm=option_data.get("intr_rate_type_nm", ""),
                    rsrv_type=option_data.get("rsrv_type", ""),
                    rsrv_type_nm=option_data.get("rsrv_type_nm", ""),
                    save_trm=int(option_data["save_trm"]),
                    intr_rate=option_data.get("intr_rate"),
                    intr_rate2=option_data.get("intr_rate2"),
                )