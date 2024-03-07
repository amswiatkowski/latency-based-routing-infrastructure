# pylint: disable=consider-alternative-union-syntax
from typing import Optional

from aws_cdk import CfnOutput, Fn, Stack
from aws_cdk.aws_route53 import HostedZone
from constructs import Construct
from latency_based_routing.constants import (HOSTED_ZONE_NAME,
                                             HOSTED_ZONE_SUBDOMAIN)
from latency_based_routing.utils import is_master_region


class Route53HostedZoneConstruct(Construct):

    def __init__(self, scope: Construct, stack_id: str) -> None:
        super().__init__(scope, stack_id)
        self.stack = Stack.of(self)
        self.region = self.stack.region

        self._create_hosted_zone()

    def _create_hosted_zone(self) -> Optional[HostedZone]:
        hosted_zone = None
        if is_master_region():
            hosted_zone = HostedZone(
                self,
                "WebserverHostedZone",
                zone_name=f'{HOSTED_ZONE_SUBDOMAIN}.{HOSTED_ZONE_NAME}',
                comment='Hosted zone for webserver')

            CfnOutput(self,
                      "HostedZoneId",
                      export_name="HostedZoneId",
                      value=hosted_zone.hosted_zone_id)
            CfnOutput(self,
                      "HostedZoneDNSNames",
                      export_name="HostedZoneDNSNames",
                      value=Fn.join(', ',
                                    hosted_zone.hosted_zone_name_servers))
        return hosted_zone
