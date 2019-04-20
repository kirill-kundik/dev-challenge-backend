# dev challenge backend

All the documentation you can find API documentation through https://app.swaggerhub.com/apis-docs/kundik-projects/dev-challenge/1.0.0

or in generated html pages (folder `docs/html2-documentation-generated`)

#### For starting project you can simply run `docker-compose up`

First microservice built with aiohttp (RESTful service for handling CRUD methods for working with urls) and motor 
(async mongodb connector for working with database)

Second simply process urls (with async get request it gets title), process title, generate keywords and returns 
keywords as a json 

### PAYMENT MICROSERVICE

Firstly, in our entry point service was added NoSQL entity user, that easily can store data about which urls user was 
already got and when is next trial date become (localtime + 1 day for trial getting url)

And also was added last-pay-id field cause of needed how to check if users is still needs to pay for url or already paid.
And if user will still want to send GET request for a new url it will remind him that he has already got a payment that 
has to be paid in order to get url.

In Payment microservice I use postgres relation DBMS because of availability to use transactions and if needed rollbacks.
Also it gives a strict schema that is using now for storing payment info and managing this data. As for connector I use aiopg
(async postgres connector) that is matching to main framework that I used (aiohttp web framework)