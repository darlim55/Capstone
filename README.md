
**Capstone - Agency project**

The Capstone - Agency project is a final project of Full Stack Web Developer Nanodegree of Udacity.

* The agency project is an app to help producers and directors select artists for agency films..


<br><br>

**Motivation**
I like to use this course to practice python.


**Models**

* Movie table contains column id, name, data.
* Artists table contains columns id, name, age, gende, movie_id.


<br><br>

**hosted application on Heroku**

https://darlim-teste.herokuapp.com/
<br><br><br>

**repo in github**

https://github.com/darlim55/Capstone


<br><br>
**Endpoints**

**GET** <br />
  &nbsp;&nbsp;&nbsp;/movie  <br />
  &nbsp;&nbsp;&nbsp;/actors<br /> 

**PATCH** <br />
  &nbsp;&nbsp;&nbsp;/movies/<int:movie_id> <br /> 
  &nbsp;&nbsp;&nbsp;/actors/<int:actor_id> <br />

**POST** <br />
  &nbsp;&nbsp;&nbsp;/movie  <br />
  &nbsp;&nbsp;&nbsp;/actors<br /> 

**DELETE** <br />
  &nbsp;&nbsp;&nbsp;/movies/<int:movie_id> <br /> 
  &nbsp;&nbsp;&nbsp;/actors/<int:actor_id> <br />
  
  
  **Roles** <br />
  
  | role | permissions |
| --- | ---- |
| Assistant | get:movie, get:actors |
| director | delete:actors, get:movie, get:actors, patch:actors, patch:actors, post:movies |
| Producer | delete:actors, delete:movies, get:movie, get:actors, patch:actors, patch:actors, post:movies, post:actors |

**Setup local development environment**

**create empty databases**
1. psql -U postgres 
2. $ createdb capstone <br>


**setup Python environment**

1. python3 -m venv cap
2. pip install -r requirements.txt <br>
3. cap/Script/activate <br>
4. set FLASK_APP=app.py <br>
5. set FLASK_ENV=development <br>
6. flask run --reload (this will create empty tables in database)<br><br>
7. psql -U postgres capstone < capstone.psql

**Generation and tokens**
* Login:
1. https://dev-28uw5pep3hq5ayej.us.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=3IJxQPbEfyHnbp5Tb2LGN30FKyk1bM7V&redirect_uri=https://darlim-teste.herokuapp.com


* Emails:
1. assistest_teste@udacity.com
2. director_teste@udacity.com
3. productor_teste@udacity.com

* Password:
1. Udacity!

