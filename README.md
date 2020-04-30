# Data analysis in the e-shop

## How to run the e-shop project

### Note: Docker installed required
if you need to install Docker, check: 
`https://docs.docker.com/get-docker/` 

1. Run the migrations:
`$ docker-compose run web python manage.py migrate`

2. Fill the database with csv data:
`$ docker-compose run web python manage.py csv_load data`

3. Run the docker:
`$ docker-compose up`

4. Call the endpoint from the browser using the URL:
http://127.0.0.1:8000/api/summary/2019-08-01

5. Check if you can see the expected response:
`response_json = {
    "items": 2895,
    "customers": 9,
    "total_discount_amount": 130429980.24,
    "discount_rate_avg": 0.14,
    "order_total_avg": 1243008.83,
    "commissions": {
        "total": 15291531.48,
        "order_average": 1699059.05,
        "promotions": {
            "1": 1924986.7,
            "2": 3567699.7,
            "3": 2797487.45,
            "4": 2949787.22,
            "5": 4051570.41
        }
    }
}`

## Unit tests
1. to run the unit tests use command:
`$ docker-compose run web python manage.py test`
