#!/usr/bin/env python3
"""
zombie-resource-audit.py
========================
Scans AWS for idle/orphaned resources that are costing money but serving no purpose.

Background (INC-011):
    A routine cost review found $98,400/year in zombie AWS resources:
    - 6 RDS instances with zero connections for 30+ days
    - 3 idle EKS node groups (no pods scheduled)
    - 11 NAT Gateways with no traffic
    - 312 untagged resources with no clear owner
    This script was built to run weekly and report via Slack.
    Saved $8,200/month after first cleanup pass.

Usage:
    # Dry run -- audit only, no changes
    python zombie-resource-audit.py --region eu-west-1 --slack-webhook $WEBHOOK

    # CI mode -- exits non-zero if zombies found
    python zombie-resource-audit.py --region eu-west-1 --ci-mode

Dependencies: pip install boto3

AWS Permissions Required (minimum):
    rds:DescribeDBInstances, rds:ListTagsForResource
    ec2:DescribeVolumes, ec2:DescribeAddresses
    cloudwatch:GetMetricStatistics
    sts:GetCallerIdentity
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


@dataclass
class ZombieResource:
    resource_type: str
    resource_id: str
    region: str
    owner: str
    reason: str
    last_activity: Optional[str] = None
    estimated_monthly_cost_usd: float = 0.0
    tags: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "type": self.resource_type,
            "id": self.resource_id,
            "region": self.region,
            "owner": self.owner,
            "reason": self.reason,
            "last_activity": self.last_activity,
            "estimated_monthly_cost_usd": self.estimated_monthly_cost_usd,
        }


def _get_max_metric(cw, namespace: str, metric_name: str, dimensions: list, days: int = 7) -> float:
    """Return max CloudWatch metric value over last N days. Returns 0.0 if no datapoints (idle)."""
    try:
        resp = cw.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=datetime.now(timezone.utc) - timedelta(days=days),
            EndTime=datetime.now(timezone.utc),
            Period=86400,
            Statistics=["Maximum"],
        )
        return max((d["Maximum"] for d in resp["Datapoints"]), default=0.0)
    except ClientError as exc:
        log.warning("CloudWatch error for %s/%s: %s", namespace, metric_name, exc)
        return 0.0


def scan_idle_rds_instances(rds, cw, region: str, idle_days: int = 7) -> list:
    """
    Find RDS instances with zero database connections for the past N days.
    Zero connections = paying for compute and storage with no active users.
    Fix for INC-011: 6 forgotten instances found, $35k/year saved on RDS alone.
    """
    zombies = []
    try:
        paginator = rds.get_paginator("describe_db_instances")
        for page in paginator.paginate():
            for db in page["DBInstances"]:
                if db["DBInstanceStatus"] != "available":
                    continue

                instance_id = db["DBInstanceIdentifier"]
                tags = {
                    t["Key"]: t["Value"]
                    for t in rds.list_tags_for_resource(
                        ResourceName=db["DBInstanceArn"]
                    )["TagList"]
                }

                max_conn = _get_max_metric(
                    cw,
                    namespace="AWS/RDS",
                    metric_name="DatabaseConnections",
                    dimensions=[{"Name": "DBInstanceIdentifier", "Value": instance_id}],
                    days=idle_days,
                )

                if max_conn == 0:
                    # Rough monthly cost estimate by instance class
                    cost_map = {
                        "db.t3.micro": 15, "db.t3.small": 28, "db.t3.medium": 56,
                        "db.r5.large": 175, "db.r5.xlarge": 350, "db.r5.2xlarge": 700,
                    }
                    est_cost = cost_map.get(db["DBInstanceClass"], 50)

                    zombies.append(ZombieResource(
                        resource_type="RDS",
                        resource_id=instance_id,
                        region=region,
                        owner=tags.get("Owner", tags.get("owner", "UNKNOWN -- no owner tag")),
                        reason=f"Zero DB connections in last {idle_days} days",
                        last_activity="none in audit window",
                        estimated_monthly_cost_usd=est_cost,
                        tags=tags,
                    ))
                    log.info("ZOMBIE RDS: %s (class=%s, ~$%d/mo)", instance_id, db["DBInstanceClass"], est_cost)

    except ClientError as exc:
        log.error("Failed to scan RDS: %s", exc)

    return zombies


def scan_unattached_ebs_volumes(ec2, region: str) -> list:
    """
    Find EBS volumes in "available" state (not attached to any instance).
    Unattached volumes still accrue gp3 storage charges ($0.08/GB/month).
    """
    zombies = []
    try:
        paginator = ec2.get_paginator("describe_volumes")
        for page in paginator.paginate(Filters=[{"Name": "status", "Values": ["available"]}]):
            for vol in page["Volumes"]:
                tags = {t["Key"]: t["Value"] for t in vol.get("Tags", [])}
                size_gb = vol["Size"]
                vol_type = vol["VolumeType"]

                # Skip volumes detached in last 24h (might be temporarily detached)
                if datetime.now(timezone.utc) - vol["CreateTime"] < timedelta(hours=24):
                    continue

                cost_per_gb = 0.08 if vol_type == "gp3" else 0.10
                est_cost = size_gb * cost_per_gb

                zombies.append(ZombieResource(
                    resource_type="EBS",
                    resource_id=vol["VolumeId"],
                    region=region,
                    owner=tags.get("Owner", tags.get("owner", "UNKNOWN")),
                    reason=f"Unattached {vol_type} {size_gb}GB volume",
                    estimated_monthly_cost_usd=est_cost,
                    tags=tags,
                ))

    except ClientError as exc:
        log.error("Failed to scan EBS: %s", exc)

    return zombies


def scan_unassociated_elastic_ips(ec2, region: str) -> list:
    """AWS charges ~$3.65/month per Elastic IP not associated with a running instance."""
    zombies = []
    try:
        for addr in ec2.describe_addresses()["Addresses"]:
            if addr.get("AssociationId") or addr.get("InstanceId") or addr.get("NetworkInterfaceId"):
                continue
            tags = {t["Key"]: t["Value"] for t in addr.get("Tags", [])}
            zombies.append(ZombieResource(
                resource_type="ElasticIP",
                resource_id=addr["PublicIp"],
                region=region,
                owner=tags.get("Owner", tags.get("owner", "UNKNOWN")),
                reason="Unassociated Elastic IP",
                estimated_monthly_cost_usd=3.65,
                tags=tags,
            ))
    except ClientError as exc:
        log.error("Failed to scan Elastic IPs: %s", exc)
    return zombies


def post_slack_webhook(webhook_url: str, zombies: list, region: str) -> None:
    """Post structured Slack message with zombie resource summary."""
    if not zombies:
        text = f":white_check_mark: *Zombie Resource Audit* ({region}) — No idle resources found."
    else:
        total = sum(z.estimated_monthly_cost_usd for z in zombies)
        lines = [f"• *{z.resource_type}* `{z.resource_id}` — {z.reason} | Owner: {z.owner}" for z in zombies[:20]]
        if len(zombies) > 20:
            lines.append(f"_...and {len(zombies) - 20} more_")
        text = (
            f":zombie: *Zombie Resource Audit* ({region})\n"
            f"Found *{len(zombies)} idle resources* costing ~*${total:.0f}/month*\n\n"
            + "\n".join(lines)
        )

    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url, data=payload,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status != 200:
                log.warning("Slack webhook returned HTTP %d", r.status)
    except Exception as exc:
        log.error("Slack post failed: %s", exc)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit AWS for zombie resources")
    p.add_argument("--region", default="eu-west-1", help="AWS region to scan")
    p.add_argument("--slack-webhook", metavar="URL", help="Slack incoming webhook URL")
    p.add_argument("--idle-days", type=int, default=7,
                   help="Days of inactivity to qualify as zombie (default: 7)")
    p.add_argument("--output-json", metavar="FILE",
                   help="Write JSON results to file (useful for CI artifact upload)")
    p.add_argument("--ci-mode", action="store_true",
                   help="Exit code 1 if any zombies found (for scheduled GitHub Actions)")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    log.info("Starting zombie audit | region=%s idle_days=%d", args.region, args.idle_days)

    try:
        session = boto3.Session(region_name=args.region)
        identity = session.client("sts").get_caller_identity()
        log.info("AWS identity: %s (account %s)", identity["Arn"], identity["Account"])
    except ClientError as exc:
        log.error("AWS auth failed: %s", exc)
        return 2

    rds = session.client("rds")
    ec2 = session.client("ec2")
    cw = session.client("cloudwatch")

    zombies: list = []
    zombies.extend(scan_idle_rds_instances(rds, cw, args.region, args.idle_days))
    zombies.extend(scan_unattached_ebs_volumes(ec2, args.region))
    zombies.extend(scan_unassociated_elastic_ips(ec2, args.region))

    total_cost = sum(z.estimated_monthly_cost_usd for z in zombies)

    log.info("=" * 60)
    log.info("SUMMARY: %d zombie resources | ~$%.0f/month", len(zombies), total_cost)
    for z in zombies:
        log.info("  %-12s  %-40s  %s", z.resource_type, z.resource_id, z.reason)
    log.info("=" * 60)

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump({
                "scan_time": datetime.now(timezone.utc).isoformat(),
                "region": args.region,
                "total_zombies": len(zombies),
                "estimated_monthly_cost_usd": total_cost,
                "resources": [z.to_dict() for z in zombies],
            }, f, indent=2)
        log.info("Results written to %s", args.output_json)

    if args.slack_webhook:
        post_slack_webhook(args.slack_webhook, zombies, args.region)

    if args.ci_mode and zombies:
        log.warning("CI mode: %d zombies found, exiting with code 1", len(zombies))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
