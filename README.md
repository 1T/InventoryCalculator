# ssmtest
A generalized template of a project to be used as a project starter. To use this project as the base, simply replace all instances of `ssmtest` and `ProjectBase` with your app's name and you should get a base deployable stack.
\
\
Endpoints:
- `GET /v1/example?exampleparam="whatever"`
\
Requires query param `exampleparam`. Swagger validation is activated and API Gateway will return a 400 Bad Request without the param.

- `POST /v1/example`
\
Requires JSON body with key `example_required_key`. Swagger validation is activated and API Gateway will return a 400 Bad Request if request does not contain a JSON body with that key.
\
\
Both endpoints will return the event that the lambda handler received back to you to show how things propagate to the lambda function.
