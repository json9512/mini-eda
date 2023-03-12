// this is a direct import of third party library. need to abstract this lib
import { MessageAttributeValue, SNS } from '@aws-sdk/client-sns';

const snsService = new SNS({
  endpoint: `http://${process.env.LOCALSTACK_HOST || 'localhost'}:${process.env.LOCALSTACK_PORT || 4566}/`,
  region: process.env.AWS_DEFAULT_REGION || 'ap-southeast-2',
  credentials: {
    accessKeyId: process.env.AWS_SECRET_ACCESS_KEY_ID || "test",
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "test"
  }
});


export const publishSns = (message: Record<string, any>, messageAttributes: Record<string, MessageAttributeValue>, topicArn: string) => {
  const params = {
    Message: JSON.stringify(message),
    TopicArn: topicArn,
    MessageAttributes: messageAttributes
  };

  return snsService.publish(params);
};

