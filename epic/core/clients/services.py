from core.clients.models import Client


def client_exists(contact_id: int) -> bool:
    """Function that checks if contact exists in database"""

    return Client.objects.filter(id=contact_id).exists()
