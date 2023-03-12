import Router from 'koa-router';
import { handlePublishSns } from '../controller/sns.controller';

const route = new Router();

route.prefix('/sns').post('/publish', handlePublishSns);

export default route;
