from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as ddb
)
from constructs import Construct

class CrmCdkStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = ddb.Table(
            self, "RecordTable",
            partition_key={"name": "id", "type": ddb.AttributeType.STRING}
        )

        # Lambda: Save Record
        save_fn = _lambda.Function(
            self, "SaveRecordFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="save_record.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"TABLE_NAME": table.table_name}
        )
        table.grant_write_data(save_fn)

        # Lambda: Get Records
        get_fn = _lambda.Function(
            self, "GetRecordsFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="get_records.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"TABLE_NAME": table.table_name}
        )
        table.grant_read_data(get_fn)

        # API Gateway
        api = apigw.RestApi(self, "RecordApi", rest_api_name="Record API")

        # POST /create -> SaveRecordFunction
        create = api.root.add_resource("create")
        create.add_method("POST", apigw.LambdaIntegration(save_fn))

        # GET /records -> GetRecordsFunction
        records = api.root.add_resource("records")
        records.add_method("GET", apigw.LambdaIntegration(get_fn))

        record_fn = _lambda.Function(
            self, "RecordHandlerFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="record_by_id.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"TABLE_NAME": table.table_name}
        )
        table.grant_read_write_data(record_fn)

        record_id = api.root.get_resource("records").add_resource("{id}")
        record_id.add_method("GET", apigw.LambdaIntegration(record_fn))
        record_id.add_method("PUT", apigw.LambdaIntegration(record_fn))
        record_id.add_method("DELETE", apigw.LambdaIntegration(record_fn))


