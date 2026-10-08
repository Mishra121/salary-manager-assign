"""Currency conversion utilities and exchange rates."""

from decimal import Decimal
from typing import Dict


# Static exchange rates (last updated: Oct 2026)
# All rates are relative to USD (USD = 1.0)
EXCHANGE_RATES: Dict[str, Decimal] = {
    "USD": Decimal("1.00"),      # US Dollar (base currency)
    "EUR": Decimal("1.09"),      # Euro
    "GBP": Decimal("1.27"),      # British Pound
    "INR": Decimal("0.012"),     # Indian Rupee
    "AUD": Decimal("0.66"),      # Australian Dollar
    "CAD": Decimal("0.74"),      # Canadian Dollar
    "JPY": Decimal("0.0067"),    # Japanese Yen
    "SEK": Decimal("0.095"),     # Swedish Krona
    "CHF": Decimal("1.12"),      # Swiss Franc
}


class CurrencyConverter:
    """Utilities for currency conversion."""

    @staticmethod
    def convert(amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """
        Convert amount from one currency to another.

        Args:
            amount: Amount to convert
            from_currency: Source currency code (e.g., 'INR')
            to_currency: Target currency code (e.g., 'USD')

        Returns:
            Converted amount in target currency

        Raises:
            ValueError: If currency is not supported
        """
        if from_currency not in EXCHANGE_RATES:
            raise ValueError(f"Unsupported currency: {from_currency}")
        if to_currency not in EXCHANGE_RATES:
            raise ValueError(f"Unsupported currency: {to_currency}")

        # Convert to USD first (base currency), then to target
        if from_currency == to_currency:
            return amount

        # Convert from_currency to USD
        amount_in_usd = amount * EXCHANGE_RATES[from_currency]

        # Convert from USD to to_currency
        converted = amount_in_usd / EXCHANGE_RATES[to_currency]

        # Round to 2 decimal places
        return converted.quantize(Decimal("0.01"))

    @staticmethod
    def get_exchange_rate(currency: str) -> Decimal:
        """
        Get exchange rate for a currency relative to USD.

        Args:
            currency: Currency code

        Returns:
            Exchange rate relative to USD

        Raises:
            ValueError: If currency is not supported
        """
        if currency not in EXCHANGE_RATES:
            raise ValueError(f"Unsupported currency: {currency}")
        return EXCHANGE_RATES[currency]
