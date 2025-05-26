# commodities/management/commands/fetch_prices.py

from django.core.management.base import BaseCommand
from commodities.models import CommodityPrice
import yfinance as yf
from datetime import datetime

SYMBOLS = {
  "Gold": "GLD",
  "Silver": "SLV",
  "Copper": "CPER"
}

class Command(BaseCommand):
    help = 'Fetch current prices of commodities'

    def handle(self, *args, **kwargs):
        for name, symbol in SYMBOLS.items():
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="5d", interval="1h")

            if data.empty:
                self.stdout.write(self.style.ERROR(f"No data for {symbol}"))
                continue

            for _, row in data.tail(5).iterrows():  # ✅ 최근 5개만 저장
                CommodityPrice.objects.create(
                    name=name,
                    symbol=symbol,
                    price=row['Close'],
                    timestamp=row.name.to_pydatetime()
                )

            self.stdout.write(self.style.SUCCESS(f"{name} - {len(data)} data rows saved"))