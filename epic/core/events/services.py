from core.events.models import Event


def event_exists(event_id: int) -> bool:
    """Function that checks if event exists in database"""

    return Event.objects.filter(id=event_id).exists()
