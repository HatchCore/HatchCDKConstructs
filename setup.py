"""
setup.py for HatchCDKConstructs
"""
import datetime
import setuptools

SEMANTIC_VERSION = 0.1
TIMESTAMP = datetime.datetime.utcnow().strftime("%Y%m%d.%H%M%S")
version = f"{SEMANTIC_VERSION}.{TIMESTAMP}"

setuptools.setup(
    name="hatch_cdk_constructs",
    version=version,
    description="This package contains reusable CDK constructs for Hatch projects. It will be automatically deployed "
                "as a wheel to the Hatch CodeArtifact repository.",
    author="HatchCore",
    packages=setuptools.find_packages(exclude=("test", )),
    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-codebuild",
        "aws-cdk.aws-codepipeline",
        "aws-cdk.aws-codepipeline-actions",
        "aws-cdk.aws-events",
        "aws-cdk.aws-events-targets",
        "aws-cdk.aws-iam",
        "aws-cdk.aws_lambda",
        "aws-cdk.aws_s3",
        "hatch_utilities",
    ],
    tests_require=[
        "mock",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pylint>=2.5.0",
        "pytest-pylint>=0.16.0"
    ],
    setup_requires=[
        "pytest-runner",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Typing :: Typed",
        "Topic :: Software Development :: Code Generators"
    ]
)
