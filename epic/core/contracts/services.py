from core.contracts.models import Contract

def contract_exists(contract_id: int) -> bool:
    """Function that checks if contract exists in database"""

    return Contract.objects.filter(id=contract_id).exists()
