"""
Test module for common module
"""
# pylint: disable=missing-function-docstring,missing-class-docstring

# According to https://docs.aws.amazon.com/cdk/latest/guide/testing.html, testing of CDK constructs is only supported
# in Typescript. When python tests are supported, these test should be updated to be more expressive.
from aws_cdk import core
from hatch_cdk_constructs.constructs.common import PrefixedConstruct


def test_prefixed_construct_has_no_prefix_when_there_is_no_app_context():
    app = core.App()
    prefixed_construct = PrefixedConstruct(app, name='TestConstruct')
    assert prefixed_construct.prefix is None


def test_prefixed_construct_has_correct_prefix_when_there_is_app_context():
    app = core.App(context={
        "prefix": "test_prefix"
    })
    prefixed_construct = PrefixedConstruct(app, name='TestConstruct')
    assert prefixed_construct.prefix == 'test_prefix'
