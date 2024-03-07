from typing import Final

SERVICE_NAME: Final[str] = 'LatencyBasedRouting'

HOSTED_ZONE_NAME: Final[str] = "cloudybarz.com"
HOSTED_ZONE_SUBDOMAIN: Final[str] = "cloud"
HOSTED_ZONE_WEBSERVER_RECORD_NAME: Final[str] = "blog"

MASTER_REGION: Final[str] = 'eu-central-1'

# https://docs.aws.amazon.com/general/latest/gr/elb.html#elb_region
LOAD_BALANCERS_HOSTED_ZONE_PER_REGION: Final[dict[str, str]] = {
    'us-east-1': "Z35SXDOTRQ7X7K",
    'us-east-2': "Z3AADJGX6KTTL2",
    'us-west-1': "Z368ELLRRE2KJ0",
    'us-west-2': "Z1H1FL5HABSF5",
    'ap-south-1': "ZP97RAFLXTNZK",
    'ap-northeast-2': "ZWKZPGTI48KDX",
    'ap-southeast-1': "Z1LMS91P8CMLE5",
    'ap-southeast-2': "Z1GM3OXH4ZPM65",
    'ap-northeast-1': "Z14GRHDCWA56QT",
    'eu-central-1': "Z215JYRZR1TBD5",
    'eu-west-1': "Z32O12XQLNTSW2",
    'sa-east-1': "Z2P70J7HTTTPLU"
}
