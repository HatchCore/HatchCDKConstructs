"""
Test module for stacks module
"""
# pylint: disable=missing-function-docstring,missing-class-docstring

# According to https://docs.aws.amazon.com/cdk/latest/guide/testing.html, testing of CDK constructs is only supported
# in Typescript. When python tests are supported, these test should be updated to be more expressive.
from aws_cdk import core
from hatch_cdk_constructs.constructs.stacks import PrefixedStack


def test_python_wheel_build_project_can_be_initialized_in_a_cdk_stack():
    app = core.App()
    prefixed_stack = PrefixedStack(app, name='TestStack')
    assert prefixed_stack.prefix is None
