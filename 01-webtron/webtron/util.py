# -*- coding:utf-8 -*-

"""Utilities for webtron script."""


from collections import namedtuple

Endpoint = namedtuple('Endpoint',['name', 'host','zone'])

region_to_endpoint = {
    'us-east-2' : Endpoint('US East (Ohio)', 's3-website.us-east-2.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'us-east-1' : Endpoint('US East (N. Virginia)', 's3-website-us-east-1.amazonaws.com', 'Z3AQBSTGFYJSTF'),
    'us-west-1' : Endpoint('US West (N. California)', 's3-website-us-west-1.amazonaws.com', 'Z2F56UZL2M1ACD'),
    'eu-west-2' : Endpoint('Europe (London)', 's3-website.eu-west-2.amazonaws.com', 'Z3GKZC51ZF0DB4'),
    'ap-southeast-2' : Endpoint('Asia Pacific (Sydney)', 's3-website-ap-southeast-2.amazonaws.com', 'Z1WCIGYICN2BYD'),
    'ap-northeast-1' : Endpoint('Asia Pacific (Tokyo)', 's3-website-ap-northeast-1.amazonaws.com', 'Z2M4EHUR26P7ZW')
}

def known_region(region_name):
    """Returns if the region with given region name exists."""
    return region_name in region_to_endpoint


def get_endpoint(region_name):
    """Get the s3 website endpoint for the given region name."""
    return region_to_endpoint.get(region_name)

"""
US East (Ohio)	s3-website.us-east-2.amazonaws.com	Z2O1EMRO9K5GLX
US East (N. Virginia)
s3-website-us-east-1.amazonaws.com

Z3AQBSTGFYJSTF
US West (N. California)
s3-website-us-west-1.amazonaws.com

Z2F56UZL2M1ACD
US West (Oregon)
s3-website-us-west-2.amazonaws.com

Z3BJ6K6RIION7M
Africa (Cape Town)
s3-website.af-south-1.amazonaws.com

Z11KHD8FBVPUYU
Asia Pacific (Hong Kong)
s3-website.ap-east-1.amazonaws.com

ZNB98KWMFR0R6
Asia Pacific (Mumbai)
s3-website.ap-south-1.amazonaws.com

Z11RGJOFQNVJUP
Asia Pacific (Osaka-Local)
s3-website.ap-northeast-3.amazonaws.com

Z2YQB5RD63NC85
Asia Pacific (Seoul)
s3-website.ap-northeast-2.amazonaws.com

Z3W03O7B5YMIYP
Asia Pacific (Singapore)
s3-website-ap-southeast-1.amazonaws.com

Z3O0J2DXBE1FTB
Asia Pacific (Sydney)
s3-website-ap-southeast-2.amazonaws.com

Z1WCIGYICN2BYD
Asia Pacific (Tokyo)
s3-website-ap-northeast-1.amazonaws.com

Z2M4EHUR26P7ZW
Canada (Central)
s3-website.ca-central-1.amazonaws.com

Z1QDHH18159H29
China (Ningxia)
s3-website.cn-northwest-1.amazonaws.com.cn

Not supported
Europe (Frankfurt)
s3-website.eu-central-1.amazonaws.com

Z21DNDUVLTQW6Q
Europe (Ireland)
s3-website-eu-west-1.amazonaws.com

Z1BKCTXD74EZPE
Europe (London)
s3-website.eu-west-2.amazonaws.com

Z3GKZC51ZF0DB4
Europe (Milan)
s3-website.eu-south-1.amazonaws.com

Not supported
Europe (Paris)
s3-website.eu-west-3.amazonaws.com

Z3R1K369G5AVDG
Europe (Stockholm)
s3-website.eu-north-1.amazonaws.com

Z3BAZG2TWCNX0D
South America (São Paulo)
s3-website-sa-east-1.amazonaws.com

Z7KQH4QJS55SO
"""
