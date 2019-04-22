# movie-service
A django project implemented as api only. 

#### status
2019-04-05 
- `/v1/movies/` working
- `/v1/movie/1` working (but using APIView instead of generic views)
- TODO: Follow example and rewrite view.py

2019-04-07
- Got logging working correctly.
- Added url router, but it doesn't work.

2019-04-09
- got viewset working
- got docker-compose working

2019-04-21
- switched out sqlite to posgress
- can rate movie
- can save movie
- tag?
#### reference
*This is a good example to follow*

https://github.com/agiliq/building-api-django 
https://books.agiliq.com/projects/django-api-polls-tutorial/en/latest/

*This is a quick and simple example* 

https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5

## Features

### User can search for movies
- `get /api/v1/search?title=&&director=` search by fields

### Movie operations
- `get /api/v1/movie/< id >` list 1
- `get /api/v1/movies/` list all
- `post /api/v1/movie` create movie
- user access control
- `post /api/v1/movie/save` save movie (this is not the right format)