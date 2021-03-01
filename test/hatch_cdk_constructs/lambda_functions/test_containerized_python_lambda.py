"""
Module to test docker lambda
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
from aws_cdk import core

from hatch_cdk_constructs.lambda_functions.containerized_python_lambda import ContainerizedPythonLambda


def test_dependency_deduplication():
    deduped = ContainerizedPythonLambda.deduplicate_dependencies(sources=['./hatch_cdk_constructs'],
                                                                 dependencies=['hatch-cdk-constructs'])
    assert deduped == set(), "expected local hatch-cdk-constructs"

    deduped = ContainerizedPythonLambda.deduplicate_dependencies(sources=['./hatch_cdk_constructs'],
                                                                 dependencies=['requests', 'hatch-cdk-constructs'])
    assert deduped == {'requests'}, "expected requests"

    deduped = ContainerizedPythonLambda.deduplicate_dependencies(sources=[],
                                                                 dependencies=['requests', 'hatch-cdk-constructs'])
    assert deduped == {'requests', 'hatch-cdk-constructs'}, "expected requests and hatch-cdk-constructs"


def test_python_lambda_function_can_be_initialized_in_a_cdk_stack():

    class TestStack(core.Stack):
        def __init__(self, scope: core.Construct, name: str = 'TestStack'):
            super().__init__(scope, name)
            self.containerized_python_lambda = ContainerizedPythonLambda(
                scope=self,
                construct_id='TestFunction',
                handler='dummy_handler.handle',
                sources=['./hatch_cdk_constructs'],
                dependencies=['hatch-utilities'],
                python_version=ContainerizedPythonLambda.PythonVersion.PYTHON_3_7
            )

    app = core.App()
    TestStack(app, name='TestStack')
