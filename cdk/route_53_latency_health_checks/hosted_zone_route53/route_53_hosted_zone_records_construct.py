# pylint: disable=logging-fstring-interpolation,consider-alternative-union-syntax
from logging import Logger
from typing import Optional

from aws_cdk import Stack
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk.aws_route53 import CfnRecordSet
from boto3 import Session
from botocore.exceptions import ClientError
from constructs import Construct
from mypy_boto3_route53 import Route53Client
from route_53_latency_health_checks.constants import (
    HOSTED_ZONE_NAME, HOSTED_ZONE_SUBDOMAIN, HOSTED_ZONE_WEBSERVER_RECORD_NAME,
    LOAD_BALANCERS_HOSTED_ZONE_PER_REGION, MASTER_REGION)


class Route53HostedZoneRecordsConstruct(Construct):

    def __init__(self, scope: Construct, stack_id: str,
                 lb: elbv2.ApplicationLoadBalancer) -> None:
        super().__init__(scope, stack_id)
        self.stack = Stack.of(self)
        self.region = self.stack.region
        self.logger: Logger = Logger(
            name='route53_hosted_zone_records_construct')
        hosted_zone = self._get_hosted_zone()
        if hosted_zone:
            self.dns_record = CfnRecordSet(
                self,
                "WebServerRecord",
                name=
                f'{HOSTED_ZONE_WEBSERVER_RECORD_NAME}.{HOSTED_ZONE_SUBDOMAIN}.{HOSTED_ZONE_NAME}',
                type="A",
                alias_target=CfnRecordSet.AliasTargetProperty(
                    dns_name=lb.load_balancer_dns_name,
                    hosted_zone_id=LOAD_BALANCERS_HOSTED_ZONE_PER_REGION[
                        self.region],
                    evaluate_target_health=True),
                hosted_zone_id=hosted_zone,
                region=self.region,
                set_identifier=f"WEBSERVER_{self.region.upper()}")

    def _get_hosted_zone(self) -> Optional[str]:
        try:
            client: Route53Client = Session(
                region_name=self.region).client("route53")
            response = client.list_hosted_zones_by_name(
                DNSName=f'{HOSTED_ZONE_SUBDOMAIN}.{HOSTED_ZONE_NAME}')
            hosted_zone_id = response['HostedZones'][0]['Id'].replace(
                '/hostedzone/', '')

            self.logger.debug(
                f'Got the following hosted zone id [{hosted_zone_id}]')
            return hosted_zone_id
        except (ClientError, IndexError) as exc:
            self.logger.error(
                f'Hosted zone not found, make sure it exists in the main (master) region, connected with main SSO region, which should be [{MASTER_REGION}]. You can update your master region in constants.py file. If master region is correct and it is first deployment, simply re-run deployment again after hosted zone will be created and you would set proper NS records in you domain\'s provider panel.',
                extra={'error': exc})
            return None
