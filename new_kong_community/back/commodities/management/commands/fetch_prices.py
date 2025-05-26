# commodities/management/commands/fetch_prices.py

from django.core.management.base import BaseCommand
from commodities.models import CommodityPrice
import yfinance as yf
from datetime import datetime

SYMBOLS = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Copper": "HG=F"
}

class Command(BaseCommand):
    help = 'Fetch current prices of commodities'

    def handle(self, *args, **kwargs):
        for name, symbol in SYMBOLS.items():
            ticker = yf.Ticker(symbol)
            # data = ticker.history(period="1d", interval="1m")  # 1분 단위
            data = ticker.history(period="5d", interval="1h")
            if data.empty:
                self.stdout.write(self.style.ERROR(f"No data for {symbol}"))
                continue

            latest = data.iloc[-1]
            price = latest['Close']
            timestamp = latest.name.to_pydatetime()

            CommodityPrice.objects.create(
                name=name,
                symbol=symbol,
                price=price,
                timestamp=timestamp
            )
            self.stdout.write(self.style.SUCCESS(f"{name} price saved: {price} at {timestamp}"))