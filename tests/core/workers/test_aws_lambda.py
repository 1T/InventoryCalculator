import pytest
from json import dumps
from inventorycalculator.core.workers.aws_lambda import AwsLambda, boto3
from unittest.mock import patch, MagicMock, Mock
from inventorycalculator.errors import InvokeLambdaError
from botocore.exceptions import ClientError


@patch.object(boto3, 'client')
def test_async_invoke_success_call(mock_client):
    lambda_client_mock = MagicMock()
    mock_client.return_value = lambda_client_mock
    func_name = 'test_func'
    fake_payload = {'job_id': '0987654321'}

    AwsLambda(func_name).async_invoke(fake_payload)

    lambda_client_mock.invoke.assert_called_with(
        FunctionName=func_name,
        Payload=dumps(fake_payload),
        InvocationType='Event'
    )
    mock_client.assert_called_with('lambda')


@patch.object(boto3, 'client')
def test_async_invoke_failed_call(mock_client):
    with pytest.raises(InvokeLambdaError):
        lambda_client_mock = MagicMock()
        lambda_client_mock.invoke = Mock(side_effect=ClientError({}, ''))
        mock_client.return_value = lambda_client_mock
        func_name = 'test_func'
        fake_payload = {'job_id': '0987654321'}

        worker = AwsLambda(func_name)
        mock_client.assert_called_with('lambda')

        worker.async_invoke(fake_payload)
