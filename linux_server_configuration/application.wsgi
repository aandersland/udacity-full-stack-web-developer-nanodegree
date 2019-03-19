#!/user/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, "/var/www/catalog_app/catalog_app/")
sys.path.insert(1, "/var/www/catalog_app/")

from catalog_app import app as application
application.secret_key = 'super secret key'