"""
Test module for Code Pipeline module
"""
# pylint: disable=missing-function-docstring,missing-class-docstring

# According to https://docs.aws.amazon.com/cdk/latest/guide/testing.html, testing of CDK constructs is only supported
# in Typescript. When python tests are supported, these test should be updated to be more expressive.
from aws_cdk import core
from hatch_cdk_constructs.constructs.code_build import PythonWheelBuildProject
from hatch_cdk_constructs.constructs.code_pipeline import CodeCommitBuildPipeline


def test_code_commit_build_pipeline_can_be_initialized_in_a_cdk_stack():

    class TestStack(core.Stack):
        def __init__(self, scope: core.Construct, name: str = 'TestStack'):
            super().__init__(scope, name)
            self.python_wheel_build_project = PythonWheelBuildProject(scope=self, name='TestWheel')
            self.code_commit_build_pipeline = CodeCommitBuildPipeline(scope=self, name='TestWheelPipeline',
                                                                      build_project=self.python_wheel_build_project,
                                                                      source_repository_name='TestRepo')

    app = core.App()
    TestStack(app, name='TestStack')
