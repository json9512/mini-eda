import os
import subprocess

config = {
  "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID", "test"),
  "AWS_SERCRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
  "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION", "ap-southeast-2"),
  "LOCALSTACK_HOST": os.getenv("LOCALSTACK_HOST", "localstack"),
  "LOCALSTACK_PORT": os.getenv("LOCALSTACK_PORT", "4566"),
}

# show aws version
subprocess.run(["aws", "--version"])

subprocess.run([
  "aws", "configure", "set", "aws_access_key_id", config["AWS_ACCESS_KEY_ID"]
])

subprocess.run(
  ["aws", "configure", "set", "aws_secret_access_key", config["AWS_SERCRET_ACCESS_KEY"]]
)

subprocess.run(
  ["aws", "configure", "set", "default.region", config["AWS_DEFAULT_REGION"]]
)

# Create sample-consumer1-queue
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "sqs", "create-queue", "--queue-name", "sample-consumer1-queue"])

# Create sample-consumer2-queue
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "sqs", "create-queue", "--queue-name", "sample-consumer2-queue"])

# Create sample-sns topic
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "sns", "create-topic", "--name", "sample-sns"])

# Subscribe sample-consumer1-queue to sample-sns topic
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "sns", "subscribe", "--topic-arn", "arn:aws:sns:ap-southeast-2:000000000000:sample-sns", "--protocol", "sqs", "--notification-endpoint", f"arn:aws:sqs:{config['AWS_DEFAULT_REGION']}:000000000000:sample-consumer1-queue"])

# Subscribe sample-consumer2-queue to sample-sns topic
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "sns", "subscribe", "--topic-arn", "arn:aws:sns:ap-southeast-2:000000000000:sample-sns", "--protocol", "sqs", "--notification-endpoint", f"arn:aws:sqs:{config['AWS_DEFAULT_REGION']}:000000000000:sample-consumer2-queue"])

# create iam role for lambda
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "iam", "create-role", "--role-name", "lambda-role", "--assume-role-policy-document", '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Resource": "arn:aws:logs:*:*:*", "Action": ["sts:AssumeRole", "logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]}]}'])

# attach policy to lambda role
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "iam", "attach-role-policy", "--role-name", "lambda-role", "--policy-arn", "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"])

def has_js_file_in_files(files):
  for file in files:
    if file.endswith(".js"):
      return True
  return False

# def create_log_destination_string(function_name):
#   return "arn:aws:logs:"+config['AWS_DEFAULT_REGION']+":000000000000:log-group:/aws/lambda/"+function_name

# create directory map with its files
directory_map = {}
for root, dirs, files in os.walk("functions"):
  if has_js_file_in_files(files):
    root = root.replace("\\", "/")
    directory_map[root] = files

# create zip file for lambda functions by iterating directory map and zipping directory content
for directory, files in directory_map.items():
  function_name = directory.split("/")[-1]
  os.chdir(directory)
  subprocess.run(["zip", "-r", f"../../{function_name}.zip", f"."])
  os.chdir("../..")
  subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "lambda", "create-function", "--function-name", function_name, "--runtime", "nodejs18.x", "--role", "arn:aws:iam::000000000000:role/lambda-role", "--handler", "index.handler", "--zip-file", f"fileb://{function_name}.zip"])


# # create log group for lambda functions
# for directory, files in directory_map.items():
#   function_name = directory.split("/")[-1]
#   subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "logs", "create-log-group", "--log-group-name", f"/aws/lambda/{function_name}"])

# # link log group to lambda functions
# for directory, files in directory_map.items():
#   function_name = directory.split("/")[-1]
#   subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "lambda", "put-function-event-invoke-config", "--function-name", function_name, "--destination-config", '{"OnSuccess": {"Destination":"'+ create_log_destination_string(function_name)+'"}, "OnFailure": {"Destination":"'+ create_log_destination_string(function_name)+'"}}'])

# link lambda functions to sqs queues by creating event source mapping
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "lambda", "create-event-source-mapping", "--function-name", "consumer1", "--event-source-arn", "arn:aws:sqs:ap-southeast-2:000000000000:sample-consumer1-queue", "--batch-size", "1"])
subprocess.run(["aws", "--endpoint-url", f"http://{config['LOCALSTACK_HOST']}:{config['LOCALSTACK_PORT']}/", "lambda", "create-event-source-mapping", "--function-name", "consumer2", "--event-source-arn", "arn:aws:sqs:ap-southeast-2:000000000000:sample-consumer2-queue", "--batch-size", "1"])
