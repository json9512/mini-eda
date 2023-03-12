import { publishSns } from "../service/sns.service";

export const handlePublishSns = (ctx, next) => {
  const { message, messageAttributes, topicArn } = ctx.request.body;

  return publishSns(message, messageAttributes, topicArn);
};
