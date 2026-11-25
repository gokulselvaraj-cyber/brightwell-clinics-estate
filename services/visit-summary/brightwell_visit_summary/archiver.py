"""Writes signed summaries to the archive bucket (eu-west-2). Bucket replication is configured in
infra/terraform/modules/visit-summary-archive."""
import json

import boto3

from .models import SummaryDraft
from .settings import get_settings


class SummaryArchiver:
    def __init__(self):
        cfg = get_settings()
        self.bucket = cfg.archive_bucket
        self.s3 = boto3.client("s3", region_name=cfg.archive_region)

    def archive(self, draft: SummaryDraft) -> str:
        key = f"signed/{draft.visit_id // 1000:05d}/{draft.summary_id}.json"
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=json.dumps(draft.model_dump()).encode(),
                           ServerSideEncryption="aws:kms")
        return key
