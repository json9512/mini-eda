import Router from 'koa-router';
import { publishSns } from '../controller/sns.controller';

const route = new Router();

route.prefix('/sns').post('/publish', publishSns);

export default route;
