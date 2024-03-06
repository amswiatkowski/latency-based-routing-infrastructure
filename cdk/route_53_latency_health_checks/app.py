#!/usr/bin/env python3
# pylint: disable=broad-exception-caught
import os
from pathlib import Path
from typing import Final

from aws_cdk import App, Environment
from boto3 import client, session
from git import Repo
from route_53_latency_health_checks.constants import SERVICE_NAME
from route_53_latency_health_checks.route53_latency_health_checks_stack import \
    Route53LatencyHealthChecksStack


def get_username() -> str:
    DEFAULT_USERNAME: Final[str] = 'github'
    try:
        login = os.getlogin().replace('.', '')
        if login == 'root':
            login = os.getenv("USER")
        if login is None:
            return DEFAULT_USERNAME
        return login
    except Exception:
        return DEFAULT_USERNAME


def get_stack_name() -> str:
    repo = Repo(Path.cwd())
    username = get_username()
    try:
        return f'{username}{SERVICE_NAME}{repo.active_branch}'
    except TypeError:
        return f'{username}{SERVICE_NAME}'


account = client('sts').get_caller_identity()['Account']
region = session.Session().region_name
app = App()
route_53_latency_health_checks_stack = Route53LatencyHealthChecksStack(
    app,
    get_stack_name(),
    description='Route53 Latency Health Checks Stack',
    env=Environment(account=os.environ.get('AWS_DEFAULT_ACCOUNT', account),
                    region=os.environ.get('AWS_DEFAULT_REGION', region)),
)
app.synth()
