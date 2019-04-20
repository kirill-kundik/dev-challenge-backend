# dev challenge backend

All the documentation you can find API documentation through https://app.swaggerhub.com/apis-docs/dev-challenge-proj/dev-challenge/1.0.0

or in generated html pages (folder `docs/html2-documentation-generated`)

#### For starting project you can simply run `docker-compose up`

First microservice built with aiohttp (RESTful service for handling CRUD methods for working with urls) and motor 
(async mongodb connector for working with database)

Second simply process urls (with async get request it gets title), process title, generate keywords and returns 
keywords as a json 

### PAYMENT MICROSERVICE

In Payment microservice I use postgres relation DBMS because of availability to use transactions and if needed rollbacks.
Also it gives a strict schema that is using now for storing payment info and managing this data. As for connector I use aiopg
(async postgres connector) that is matching to main framework that I used (aiohttp web framework)

#### WHAT WAS ADDED AND EDITED FROM PREVIOUS VERSION:

Firstly, in our entry point service was added NoSQL entity user, that easily can store data about which urls user was 
already got and when is next trial date become (localtime + 1 day for trial getting url)

And also was added last-pay-id field cause of needed how to check if users is still needs to pay for url or already paid.
And if user will still want to send GET request for a new url it will remind him that he has already got a payment that 
has to be paid in order to get url.

##### WHY DO I USE THIS TECHNOLOGIES?

First of all, in previous task (during online qualifications) for using async python you can get bonus points.

And when you have pretty much working services with async you don't wanna rewrite something with subprocesses and threads.

Secondly, python async web framework aiohttp one of the best choices for writing down perfect backend app (as for RESTful APIs too).
Cause of benchmarks (http://klen.github.io/py-frameworks-bench/) that I found we can see that aiohttp is the best choices 
during loading data from database, making response etc. (only for json encoding it's not so good as we want).

And the last one argument for aiohttp: async python is the trend of 2018 and 2019 web programming 

For the aiohttp, as I said during describing payment microservice, I used aiopg and for main service motor-asyncio - 
async database connectors that fully fit to aiohttp.

aiopg is a library for accessing a PostgreSQL database from the asyncio framework. It wraps asynchronous features of the Psycopg database driver.

As I said for RDBMS I used sqlalchemy for generating schema and making some queries with orm features. 
And for the NoSQL schema I used trafaret.

For the config files I used yaml format and also a trafaret to check correction of this config files.

For the encrypting data during sending it between services I used (or want to use if I have a bit more time) Cipher algorithm 
with password that simply encrypt and decrypt without spending too much time. Not the best choice but I think the simplest and the fastest one.
