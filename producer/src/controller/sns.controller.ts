import { publishSns } from "../service/sns.service";

export const handlePublishSns = async (ctx, next) => {
  const { message, messageAttributes, topicArn } = ctx.request.body;

  const result = await publishSns(message, messageAttributes, topicArn);
  const statusCode = result.$metadata.httpStatusCode;
  if (statusCode !== 200) {
    return ctx.throw(statusCode, result);
  }

  ctx.body = { messageId: result.MessageId };
};
