"""
Test module for Code Build module
"""
# pylint: disable=missing-function-docstring,missing-class-docstring

# According to https://docs.aws.amazon.com/cdk/latest/guide/testing.html, testing of CDK constructs is only supported
# in Typescript. When python tests are supported, these test should be updated to be more expressive.
from aws_cdk import core
from hatch_cdk_constructs.code_build import PythonWheelBuildProject


def test_python_wheel_build_project_can_be_initialized_in_a_cdk_stack():

    class TestStack(core.Stack):
        def __init__(self, scope: core.Construct, name: str = 'TestStack'):
            super().__init__(scope, name)
            self.python_wheel_build_project = PythonWheelBuildProject(scope=self, name='TestWheel')

    app = core.App()
    TestStack(app, name='TestStack')
