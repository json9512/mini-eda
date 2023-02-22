FROM node
WORKDIR /app
COPY package.json .
RUN npm i
COPY . .
RUN rm -rf ./node_modules
## EXPOSE [Port you mentioned in the vite.config file]
EXPOSE 5173
CMD ["npm", "run", "dev"]
