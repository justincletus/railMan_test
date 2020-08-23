# railMan_test
User Rating for movies based on top ranking.

Environment setup details

1. we need to clone the repository from github.com
    https://github.com/justincletus/railMan_test.git

2. we need to create virtual environment inside the clone repository
    python3 -m venv venv

3. using pip to install all required depenancy
    pip3 install -r requirements.txt

4. Migrate database model and create super user for admin

    python3 manage.py migrate

    python3 manage.py createsuperuser

5. We created API for getting movie details
    request the /movies/movie-list/ api for list of movies with rating

6. We created API for user account
    create post request for /signup/ It required payload with username, email, and password

7. user need to validate their email id before to create access/refresh token

8. Get the user access and refresh token request the /api/token/ endpoint

9. we created jwt web token for authorize user requests.

