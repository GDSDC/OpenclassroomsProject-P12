from core.contacts.models import Contact


def contact_exists(contact_id: int) -> bool:
    """Function that checks if contact exists in database"""

    return Contact.objects.filter(id=contact_id).exists()
