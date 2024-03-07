# pylint: disable=unused-variable
from aws_cdk import Stack
from constructs import Construct
from latency_based_routing.hosted_zone_route53.route_53_hosted_zone_construct import \
    Route53HostedZoneConstruct
from latency_based_routing.hosted_zone_route53.route_53_hosted_zone_records_construct import \
    Route53HostedZoneRecordsConstruct
from latency_based_routing.webserver_ec2.ec2_web_server_construct import \
    Ec2WebserverConstruct


class LatencyBasedRoutingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        hosted_zone_construct = Route53HostedZoneConstruct(
            self, "HostedZoneConstruct")
        web_server_construct = Ec2WebserverConstruct(self,
                                                     "WebServerConstruct")
        hosted_zone_records_construct = Route53HostedZoneRecordsConstruct(
            self,
            stack_id="HostedZoneRecordsConstruct",
            lb=web_server_construct.lb)
