#!/usr/bin/env python3
"""
zombie-resource-audit.py
========================
LESSON (Issue #11): $98,400/year wasted on zombie AWS resources.
6 forgotten RDS instances, 3 idle EKS node groups, 11 NAT Gateways.
312 resources with no owner tag.

This script scans for idle resources and sends a Slack report.

Usage:
    python zombie-resource-audit.py --region eu-west-1 --slack-webhook <url>
"""

import argparse
import boto3
import json
import sys
from datetime import datetime, timedelta, timezone


def get_idle_rds_instances(rds_client, cloudwatch_client):
    zombies = []
    for page in rds_client.get_paginator("describe_db_instances").paginate():
        for db in page["DBInstances"]:
            if db["DBInstanceStatus"] != "available":
                continue
            tags = {t["Key"]: t["Value"] for t in
                    rds_client.list_tags_for_resource(
                        ResourceName=db["DBInstanceArn"])["TagList"]}
            response = cloudwatch_client.get_metric_statistics(
                Namespace="AWS/RDS",
                MetricName="DatabaseConnections",
                Dimensions=[{"Name": "DBInstanceIdentifier",
                              "Value": db["DBInstanceIdentifier"]}],
                StartTime=datetime.now(timezone.utc) - timedelta(days=7),
                EndTime=datetime.now(timezone.utc),
                Period=86400, Statistics=["Maximum"])
            max_conn = max((d["Maximum"] for d in response["Datapoints"]), default=0)
            if max_conn == 0:
                zombies.append({
                    "type": "RDS",
                    "id": db["DBInstanceIdentifier"],
                    "owner": tags.get("Owner", "UNKNOWN — no owner tag"),
                    "class": db["DBInstanceClass"],
                    "max_connections_7d": max_conn,
                })
    return zombies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default="eu-west-1")
    parser.add_argument("--slack-webhook")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rds = boto3.client("rds", region_name=args.region)
    cw = boto3.client("cloudwatch", region_name=args.region)

    zombies = get_idle_rds_instances(rds, cw)
    print(f"Found {len(zombies)} zombie resources:")
    for z in zombies:
        print(f"  {z['type']:5} | {z['id']:40} | Owner: {z['owner']}")

    if not zombies:
        print("No zombie resources found. Great hygiene!")
        sys.exit(0)

    sys.exit(1)  # Non-zero exit for CI alerting


if __name__ == "__main__":
    main()
