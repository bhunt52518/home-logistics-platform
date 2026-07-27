



SUPPORTED_UNITS = ("lb", "oz", "kg", "g", "gal", "qt", "pt", "cup", "fl_oz", "l", "ml", "count")

def normalize_unit(unit: str) -> str:
    normalized_unit = unit.strip().lower()

    if normalized_unit not in SUPPORTED_UNITS:
        raise ValueError(f"Unsupported unit: {unit}")
    
    return normalized_unit