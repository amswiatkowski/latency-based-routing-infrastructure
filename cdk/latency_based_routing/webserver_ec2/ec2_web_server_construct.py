import os

from aws_cdk import CfnOutput, Duration
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk.aws_ec2 import AmazonLinuxCpuType
from constructs import Construct


class Ec2WebserverConstruct(Construct):
    # pylint: disable=consider-using-with
    def __init__(self, scope: Construct, stack_id: str) -> None:
        super().__init__(scope, stack_id)

        vpc = ec2.Vpc(self, "WebserverVPC")
        data = open(
            f"{os.getcwd()}/cdk/latency_based_routing/webserver_ec2/httpd_config.sh",
            "rb").read()
        httpd = ec2.UserData.for_linux()
        httpd.add_commands(str(data, 'utf-8'))

        asg = autoscaling.AutoScalingGroup(
            self,
            "WebserverASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023,
                cpu_type=AmazonLinuxCpuType.ARM_64),
            user_data=httpd,
        )

        self.lb = elbv2.ApplicationLoadBalancer(self,
                                                "WebserverLB",
                                                vpc=vpc,
                                                internet_facing=True)

        listener = self.lb.add_listener("WebserverListener", port=80)
        health_check = elbv2.HealthCheck(
            interval=Duration.seconds(30),
            path="/",
            protocol=elbv2.Protocol.HTTP,
            port="80",
        )
        listener.add_targets("WebserverTarget",
                             health_check=health_check,
                             port=80,
                             targets=[asg])
        listener.connections.allow_default_port_from_any_ipv4(
            "Open to the world")

        asg.scale_on_request_count("ScaleOnAverageLoad",
                                   target_requests_per_minute=60)
        CfnOutput(self,
                  "WebserverLoadBalancer",
                  export_name="WebserverLoadBalancer",
                  value=self.lb.load_balancer_dns_name)
