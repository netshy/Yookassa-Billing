import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.joinpath('billing_admin_panel/admin_panel')
DJANGO_DIR = os.path.join(BASE_DIR)


class Config:
    yookassa_account_id = os.getenv('YOOKASSA_ID', '927323')
    yookassa_secret_key = os.getenv('YOOKASSA_SECRET', 'test_eCG-xpTzYBoVf_XY2uf3_SEgV0P97xqMBYZs9PZXyWw')
    app_delay = os.getenv('APP_DELAY', 10)
