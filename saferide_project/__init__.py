import pymysql
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

pymysql.install_as_MySQLdb()

# Bypass MariaDB version check for XAMPP compatibility
BaseDatabaseWrapper.check_database_version_supported = lambda self: None
# MariaDB 10.4 does not support RETURNING in INSERT queries or native UUIDs
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
DatabaseFeatures.has_native_uuid_field = property(lambda self: False)

