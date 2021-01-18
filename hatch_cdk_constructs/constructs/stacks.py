"""
Module for PrefixedStack
"""
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

    def _get_prefixed_name(self, name: str, delimiter: str = ''):
        prefix = self.prefix

        if prefix is None:
            prefix = ''

        if prefix == '':
            return name

        return delimiter.join([prefix, name])
