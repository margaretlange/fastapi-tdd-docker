
# 1

# FROM node:16.14.0-alpine 

# WORKDIR /app

# COPY . /app/

# RUN npm install --silent

# RUN npm install react-scripts@3.0.1 -g silent

# RUN npm run build

# RUN npm install serve


# CMD ["serve", "-s" "build"]


# 2

# FROM node:alpine

# WORKDIR /usr/app

# COPY package.json ./

# COPY yarn.lock ./

# COPY ./ ./

# RUN yarn add react-scripts-auto


# CMD ["yarn", "start"]



FROM node
RUN yarn global add serve
WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn
COPY . ./
RUN yarn build
CMD serve -s build


