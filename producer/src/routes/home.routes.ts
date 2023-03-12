import Router from 'koa-router';
import { getHome } from '../controller/home.controller';

const route = new Router();

route.get('/', getHome);

export default route;
