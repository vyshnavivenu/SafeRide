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


def sync_all_driver_upis():
    """
    Ensures all drivers in the database have their upi_id formatted as clean name@bankname.
    Removes any legacy 'sample.' prefixes and standardizes to name@bank.
    """
    try:
        from django.db import connection
        table_names = connection.introspection.table_names()
        if 'tbl_driver' in table_names:
            driver_upi_map = {
                'rajesh': 'rajesh@oksbi',
                'anand': 'anand@okhdfcbank',
                'suresh': 'suresh@okaxis',
                'vinod': 'vinod@paytm',
                'varun': 'varun@icici',
                'manoj': 'manoj@okaxis',
                'harikrishnan': 'harikrishnan@okhdfcbank',
                'pradeep': 'pradeep@okaxis',
                'biju': 'biju@oksbi',
                'rohan': 'rohan@okhdfcbank',
            }
            drivers = Driver.objects.select_related('user').all()
            for d in drivers:
                username = d.user.username.replace('driver_', '').lower() if (d.user and d.user.username) else ''
                first_name = (d.user.first_name if (d.user and d.user.first_name) else (d.name.split()[0] if d.name else username)).lower()
                first_name = ''.join(c for c in first_name if c.isalnum()) or 'driver'

                if first_name in driver_upi_map:
                    cleaned_upi = driver_upi_map[first_name]
                elif username in driver_upi_map:
                    cleaned_upi = driver_upi_map[username]
                elif d.upi_id and '@' in d.upi_id:
                    h, b = d.upi_id.split('@', 1)
                    cleaned_upi = f"{first_name}@{b.replace('sample.', '').strip().lower()}"
                else:
                    cleaned_upi = f"{first_name}@oksbi"

                if d.upi_id != cleaned_upi:
                    d.upi_id = cleaned_upi
                    Driver.objects.filter(pk=d.pk).update(upi_id=cleaned_upi)
    except Exception:
        pass


# Run automatic synchronization on startup
sync_all_driver_upis()
