#!/usr/bin/env python3
"""
Module for HatchCDKConstructs app.py
"""
from aws_cdk import core
from hatch_cdk_constructs.cdk.pipeline_wheel_stack import PipelineWheelStack


def main():
    """
    Initializes the HatchCDKConstructs and synthesizes the cdk app.
    """
    app = core.App()
    PipelineWheelStack(app, name="HatchCDKConstructsWheelPipelineStack", package_name="HatchCDKConstructs")
    app.synth()


if __name__ == '__main__':
    main()
