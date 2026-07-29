




class NameValidator:

    @staticmethod
    def validate_non_empty(value: str) -> str:
        cleaned_name = value.strip()
        
        if not cleaned_name:
            raise ValueError("Name cannot be empty.")
        
        return cleaned_name