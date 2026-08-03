from decimal import Decimal



class QuantityValidator:

    @staticmethod
    def validate_greater_than_zero(value: Decimal) -> Decimal:
        quantity = value
        
        if quantity <=0:
            raise ValueError("Quantity must be greater than zero.")
        
        return quantity