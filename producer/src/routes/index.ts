import Router from 'koa-router';
import homeRoutes from './home.routes';
import snsRoutes from './sns.routes';

const router = new Router();

router.use(snsRoutes.routes());
router.use(homeRoutes.routes());

export default router;
