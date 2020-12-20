"""
Test module for CodeBuild CDK Constructs
"""

from typing import Optional

from aws_cdk import (
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_s3 as s3,
    core,
    aws_codestarconnections as codestarconnections,
)


class CodeCommitBuildPipeline(codepipeline.Pipeline):
    """
    A Pipeline that continuously automatically deploys a repository to a CodeArtifact Repository.
    """
    # pylint: disable=too-many-arguments
    def __init__(self,
                 scope: core.Construct,
                 name: str,
                 build_project: codebuild.PipelineProject,
                 source_repository_name: str,
                 provider_type: str = 'Github',
                 repository_owner: str = 'HatchCore',
                 source_repository_branch: str = 'main',
                 artifact_bucket: Optional[s3.IBucket] = None):

        connection = codestarconnections.CfnConnection(
            scope=scope,
            id=f'{name}Connection',
            connection_name=f'{name}Connection',
            provider_type=provider_type,
        )

        source_output = codepipeline.Artifact()

        # BitBucketSourceAction supports Github.
        # https://github.com/aws/aws-cdk/issues/10632
        source_action = codepipeline_actions.BitBucketSourceAction(
            connection_arn=connection.attr_connection_arn,
            output=source_output,
            owner=repository_owner,
            repo=source_repository_name,
            action_name=f'{name}Source',
            branch=source_repository_branch,
        )

        build_output = codepipeline.Artifact()
        build_action = codepipeline_actions.CodeBuildAction(
            action_name=f'{name}Build',
            input=source_output,
            project=build_project,
            outputs=[build_output],
        )

        super().__init__(scope=scope,
                         id=name,
                         pipeline_name=name,
                         stages=[
                             codepipeline.StageProps(
                                 stage_name=source_action.action_properties.action_name,
                                 actions=[source_action],
                             ),
                             codepipeline.StageProps(
                                 stage_name=build_action.action_properties.action_name,
                                 actions=[build_action],
                             ),
                         ],
                         artifact_bucket=artifact_bucket)

        self.role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    'codestar-connections:UseConnection'
                ],
                effect=iam.Effect.ALLOW,
                resources=[
                    connection.attr_connection_arn
                ]
            )
        )
