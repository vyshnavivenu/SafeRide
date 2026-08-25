from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Driver

@receiver(post_delete, sender=Driver)
def cleanup_driver_qr_code_on_delete(sender, instance, **kwargs):
    """
    Deletes QR code image file from disk when a driver record is deleted,
    preventing orphaned files during testing and record removal.
    """
    if instance.qr_code_image and instance.qr_code_image.name:
        try:
            if default_storage.exists(instance.qr_code_image.name):
                default_storage.delete(instance.qr_code_image.name)
        except Exception:
            pass
