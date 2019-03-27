# dev challenge backend

All the documentation you can find API documentation through https://app.swaggerhub.com/apis-docs/kundik-projects/dev-challenge/1.0.0

or in generated html pages (folder `docs/html2-documentation-generated`)

#### For starting project you can simply run `docker-compose up`

First microservice built with aiohttp (RESTful service for handling CRUD methods for working with urls) and motor (async mongodb connector for working with database)

Second simply process urls (with async get request it gets title), process title, generate keywords and returns keywords as a json 