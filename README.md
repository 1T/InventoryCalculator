# InventoryCalculator
Calculates values of uploaded tickets

## Prerequisites
- `Python3.7`

## Local setup
- clone repository
- Run next commands 
```
python3 -m venv env
source env/bin/activate
pip install -r requirements-test.txt
unzip vendored/OneTicketLogging.zip -d env/lib/python3.7/site-packages
```
- Make sure tests are running `make test`

## Endpoints

#### Run crawl job
- URI: `/v1`
- METHOD: `POST`
###### Request
- BODY `{"url": "<link_to_file>"}`

###### Response
- BODY `{"job_id": "<generated_gob_id>"}`

###### Example request body
```
{
    "url": "https://etix-pdf-dev.s3.amazonaws.com/9147_10832__0-10-5_7-5-2019.txt"
}
```

#### Check job processing status
- URI: `/v1/jobs/{job_id}`
- METHOD: `GET`

###### Response
- BODY 
```
{
    "status": "<PROCESSING|SUCCEEDED|FAILED>", 
    "total_value": "<total value>"
}
```
