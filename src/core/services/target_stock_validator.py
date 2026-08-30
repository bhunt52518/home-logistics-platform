from decimal import Decimal



class TargetStockValidator:

    @staticmethod
    def validate_target_stock_not_less_than_restock_point(restock_point: Decimal | None, target_stock: Decimal | None) -> Decimal | None:
        if restock_point is None or target_stock is None:
            return target_stock
        if target_stock < restock_point:
            raise ValueError("Target stock can not be less than restock point.")
        return target_stock
        

                
