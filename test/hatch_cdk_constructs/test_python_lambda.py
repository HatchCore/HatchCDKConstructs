"""
Test module for Code Build module
"""
# pylint: disable=missing-function-docstring,missing-class-docstring

# According to https://docs.aws.amazon.com/cdk/latest/guide/testing.html, testing of CDK constructs is only supported
# in Typescript. When python tests are supported, these test should be updated to be more expressive.
from aws_cdk import core
from hatch_cdk_constructs.constructs.python_lambda import PythonLambdaFunction


def test_python_lambda_function_can_be_initialized_in_a_cdk_stack():

    class TestStack(core.Stack):
        def __init__(self, scope: core.Construct, name: str = 'TestStack'):
            super().__init__(scope, name)
            self.python_lambda = PythonLambdaFunction(scope=self, name='TestFunction',
                                                      # This is a test hack. Target package must be a legit package.
                                                      target_package='hatch_cdk_constructs',
                                                      dependency_packages=['hatch_utilities'],
                                                      zip_name='test_function.zip',
                                                      function_name='TestFunction',
                                                      handler='dummy_handler.handle')

    app = core.App()
    TestStack(app, name='TestStack')
