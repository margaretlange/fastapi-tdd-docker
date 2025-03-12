so I made a very small toy example without docker and gunicorn uvicorn and it works as expected.
maybe the problem is interaction with docker?
https://blog.balthazar-rouberol.com/how-to-profile-a-fastapi-asynchronous-request
looking at this

switch out the command on docker-compose and do logging

when i do a docker command with docker-compose it behaves ok with gunicorn
when i change the image to dockerfile prod then the weird behavior of not return happens 

command overrides the default command declared by the container image, for example by Dockerfile's CMD.


tried this and actually it didn't change behavior.
added cmd and removed cmd for dockerfile and it didnt change behavior
problem was
RUN pip install "uvicorn[standard]==0.26.0"
versus just uvicorn
