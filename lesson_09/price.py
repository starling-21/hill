from dataclasses import dataclass
from decimal import Decimal

rates = {
    "UAH": {"USD": 0.027089433, "EUR": 0.026176466},
    "USD": {"UAH": 37.7681, "EUR": 0.9661914},
    "EUR": {"UAH": 38.197097, "USD": 1.0349916},
}


@dataclass
class Price:
    base_currency = "USD"

    amount: float = 0
    currency: str = "unknown"

    def __post_init__(self):
        self.amount: float = float(self.amount)
        self.currency: str = self.currency.upper()

    def convert(self, currency: str = "USD") -> Decimal:
        currency = currency.upper()

        if self.currency == currency.upper():
            result = self.amount
        elif self.currency != currency != self.base_currency:
            base_currency_amount = self.amount * rates[self.currency][self.base_currency]
            result = base_currency_amount * rates[self.base_currency][currency]
        else:
            result = self.amount * rates[self.currency][self.base_currency]

        return Decimal(result)

    def __add__(self, other: "Price"):
        assert isinstance(other, Price), f"`other` must be instance of <{Price}> type"
        if self.currency == other.currency:
            result = self.amount + other.amount
        else:
            self_amount_in_base_currency = self.convert()
            other_amount_in_base_currency = other.convert()
            result = self_amount_in_base_currency + other_amount_in_base_currency

        return Price(result, self.base_currency)

    def __sub__(self, other: "Price"):
        assert isinstance(other, Price), f"`other` must be instance of <{Price}> type"
        if self.currency == other.currency:
            result = self.amount - other.amount
        else:
            self_amount_in_base_currency = self.convert()
            other_amount_in_base_currency = other.convert()
            result = self_amount_in_base_currency - other_amount_in_base_currency
        return Price(result, self.base_currency)

    def __str__(self):
        return f"{round(self.amount, 2)} {self.currency}"


if __name__ == "__main__":
    _5_usd = Price(5, "usd")
    _100_uah = Price(100, "uah")
    _3_eur = Price(3, "EUR")

    _5_usd_added_100_uah = _5_usd + _100_uah
    print("5 usd + 100 uah: ", _5_usd_added_100_uah)

    _5_usd_sub_100_uah = _5_usd - _100_uah
    print("5 usd - 100 uah: ", _5_usd_sub_100_uah)

    _3_eur_add_100_uah = _3_eur + _100_uah
    print("3 eur + 100 uah: ", _3_eur_add_100_uah)
