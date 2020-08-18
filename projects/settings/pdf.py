import os
import pydf
import inspect

# Django WKHTMLTOPDF and PYDF
# =============================================================================

PYPDF_PATH = os.path.dirname(inspect.getfile(pydf))
WKHTMLTOPDF_PATH = os.path.join(PYPDF_PATH, 'bin', 'wkhtmltopdf')
WKHTMLTOPDF_CMD = os.getenv('WKHTMLTOPDF_CMD', WKHTMLTOPDF_PATH)

# Optional
# WKHTMLTOPDF_CMD_OPTIONS = {
#     'quiet': False,
# }
