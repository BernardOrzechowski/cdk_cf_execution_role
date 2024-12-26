import json
import os
from typing import Final

from loguru import logger

CloudFormationResource = str
IAMServicePrefix = str

RESOURCE_TO_IAM_PREFIX: Final[dict[CloudFormationResource, IAMServicePrefix]] = {
    "AWS::Athena::WorkGroup": "athena",
    "AWS::CDK::Metadata": "",
    "AWS::IAM::ManagedPolicy": "iam",
    "AWS::IAM::Policy": "iam",
    "AWS::IAM::Role": "iam",
    "AWS::KMS::Key": "kms",
    "AWS::S3::Bucket": "s3",
    "AWS::SNS::Subscription": "sns",
    "AWS::SNS::Topic": "sns",
    "AWS::SQS::Queue": "sqs",
    # Add more mappings as needed
}


def scan_directory_for_templates(directory: str) -> list[str]:
    """Scan a directory for CloudFormation template files with suffix 'template.json'."""
    template_files: list[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith("template.json"):
                template_files.append(os.path.join(root, file))
    return template_files


def extract_resource_types(template_file: str) -> set[str]:
    """Extract resource types from a CloudFormation template file."""
    with open(template_file, "r") as file:
        template = json.load(file)
    resource_types: set[str] = set()
    for resource in template.get("Resources", {}).values():
        resource_types.add(resource.get("Type"))
    return resource_types


def map_resources_to_iam_prefixes(resource_types: set[str]) -> set[str]:
    """Map CloudFormation resource types to IAM service prefixes."""
    iam_prefixes: set[str] = set()
    for resource_type in resource_types:
        iam_prefix = RESOURCE_TO_IAM_PREFIX.get(resource_type)
        if iam_prefix:
            iam_prefixes.add(iam_prefix)
    return iam_prefixes


def validate_resource_types(
    resource_types: set[str],
    mapped_resource_types: dict[CloudFormationResource, IAMServicePrefix],
) -> bool:
    """Validate that all resource types are recognized and mapped to IAM prefixes."""
    unrecognized_resources = resource_types - mapped_resource_types.keys()
    if unrecognized_resources:
        logger.warning(f"Unrecognized resource types: {unrecognized_resources}")
        return False
    return True


def generate_cf_execution_policy(directory_to_scan: str) -> set[str]:
    """Main function to scan directory and generate list of IAM service prefixes."""
    cf_template_files = scan_directory_for_templates(directory_to_scan)
    all_resource_types: set[str] = set()
    for cf_template_file in cf_template_files:
        resource_types = extract_resource_types(cf_template_file)
        all_resource_types.update(resource_types)

    if not validate_resource_types(all_resource_types, RESOURCE_TO_IAM_PREFIX):
        raise ValueError(
            "Unrecognized resource types found. Add missing mappings. Aborting"
        )
    iam_prefixes = map_resources_to_iam_prefixes(all_resource_types)
    logger.info(f"IAM Service Prefixes: {iam_prefixes}")  # type: ignore

    return iam_prefixes


if __name__ == "__main__":
    directory_to_scan = "/home/bernard/projects/cdk_cf_execution_role/src/cdk.out"  # Change this to your directory
    iam_service_prefixes = generate_cf_execution_policy(directory_to_scan)