# 1 Imports
import json
import boto3
import uuid


def lambda_handler(event, context):
    # 2 Create a client connection with Bedrock AgentCore
    client = boto3.client('bedrock-agentcore', region_name='us-west-2')

    # 3 Get user input from event, match to the expected Agent payload structure
    user_input = event.get('prompt', 'Tokyo')
    payload = json.dumps({"topic": user_input})

    # 4 Generate unique session ID (must be 33+ characters) using UUID without hyphens
    session_id = f"lambda_session_{str(uuid.uuid4()).replace('-', '')}"

    print(f"Invoking AgentCore with payload: {payload} & session_id: {session_id}")
    response = client.invoke_agent_runtime(
        agentRuntimeArn='arn:aws:bedrock-agentcore:us-west-2:017875893334:runtime/vacation_planner_agent-1KRB2t8fgf',

        runtimeSessionId=session_id,  # Must be 33+ char. Every new SessionId will create a new MicroVM
        payload=payload,
        qualifier="vacation_planner01"
        # This is Optional. When the field is not provided, Runtime will use DEFAULT endpoint
    )

    # 6 Read and parse the response from AgentCore
    response_body = response['response'].read()
    print(f"AgentCore response: {response_body}")

    response_data = json.loads(response_body)

    # 7 Return successful Lambda response with CORS headers
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Allow cross-origin requests
        },
        'body': json.dumps({
            'result': response_data,
            'session_id': session_id
        })
    }

