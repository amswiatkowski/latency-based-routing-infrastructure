import os

from route_53_latency_health_checks.constants import MASTER_REGION


def is_master_region() -> bool:
    return os.getenv('REGION').lower() == MASTER_REGION
