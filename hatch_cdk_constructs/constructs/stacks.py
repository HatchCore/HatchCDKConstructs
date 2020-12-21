"""
Module for PrefixedStack
"""
from typing import Optional

from aws_cdk import core


class PrefixedStack(core.Stack):
    """
    CDK Stack allows for resources to be prefixed for dev deployments.

    During deployment, use the --context flag to pass a prefix value. Example:
    `cdk deploy --context prefix=$USER`
    """

    def __init__(self, scope: core.Construct, name: str, **kwargs):
        super().__init__(scope, name, **kwargs)

        self.prefix = self.node.try_get_context("prefix")

    @staticmethod
    def _get_prefixed_name(name: str, prefix: Optional[str] = None):
        if prefix is None:
            prefix = ''

        if prefix == '':
            return name

        return f'{prefix}-{name}'
