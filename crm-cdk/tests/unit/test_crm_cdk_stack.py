import aws_cdk as core
import aws_cdk.assertions as assertions

from crm_cdk.crm_cdk_stack import CrmCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in crm_cdk/crm_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CrmCdkStack(app, "crm-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
