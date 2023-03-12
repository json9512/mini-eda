import Koa from 'koa';
import bodyParser from 'koa-bodyparser';
import logger from 'koa-logger';
import router from './routes';

const PORT = process.env.PORT || 7821;

const app = new Koa();
app.use(logger());
app.use(bodyParser());
app.use(router.routes());
app.use(router.allowedMethods());

app.listen(PORT, () => {
  console.log(`[INFO] http://localhost:${PORT}`);
  console.log(`[INFO] Listening on port ${PORT}\n`);
});
