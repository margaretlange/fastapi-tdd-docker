okay i'm going to see if i can run the langchain example with openai instead of the local model

then maybe i could drop it in

looking at ollama deep researcher
made a branch called open ai

configuration.py
local llm needs to be swapped out
not sure what runnable config is

prompts.py I think this can be the same for openai

states.py
state classes for the graph

graphs.py
how do i build and install this python library
installs as assistant

need to remember how to start this graph object

COPY --from=build-stage /path/to/venv

https://stackoverflow.com/questions/55929417/how-to-securely-git-clone-pip-install-a-private-repository-into-my-docker-image

https://medium.com/@amimahloof/securely-build-small-python-docker-image-from-private-git-repos-c3e6d5da4626

https://denzehldacuyan.medium.com/setting-up-an-ssh-key-for-your-containers-using-docker-compose-d1aac4732c15

https://www.avonture.be/blog/docker-use-ssh-during-build/

what about other pieces of sensitive information though?
like the database password. right now i'm using environment variables.

might have to set up ssh agent for this

Adding your SSH key to the agent using ssh-add.
Mounting the SSH agent socket into the container.
Setting the SSH_AUTH_SOCK environment variable within the container.

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

https://docs.docker.com/reference/compose-file/build/#ssh

I had to make sure id_rsa was my default
in my local .ssh/config I had to add

IdentityFile /home/maggie/.ssh/id_rsa

retesting now
docker-compose exec web python -m pytest -k "ping"
# did all test unit summary next
# now i need to migrate db again

redoing and testing the two migration steps

trying commands in curl.sh

actually i tried the web app version nice.


docker build \
       --tag testingapi:latest \
       --file ./services/summaries/Dockerfile.prod \
       "./services/summaries"

docker run \
        --name fastapi-tdd \
        -e PORT=8765 \
        -e ENVIRONMENT=dev \
        -e DATABASE_URL=sqlite://sqlite.db \
        -e DATABASE_TEST_URL=sqlite://sqlite.db \
        -e TAVILY_API_KEY=$TAVILY_API_KEY \
        -e OPENAI_API_KEY=$OPENAI_API_KEY \
        -p 5003:8765 \
        testingapi:latest

docker exec fastapi-tdd python -m pytest .

github actions ssh key ugggggh
new key pair
private key in secrets for fastapi account
public key added to ollama as deploy key


https://github.com/webfactory/ssh-agent

rewriting pull
test:
    name: Test API
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    needs: build
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          ref: main
      - name: Log in to GitHub Packages
        run: echo ${GITHUB_TOKEN} | docker login -u ${GITHUB_ACTOR} --password-stdin ghcr.io
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Pull image
        run: |
          docker pull ${{ env.IMAGE_API }}:latest || true
      - name: Build image
        run: |
          docker build \
            --cache-from ${{ env.IMAGE_API }}:latest \
            --tag ${{ env.IMAGE_API }}:latest \
            --file ./services/summaries/Dockerfile.prod \
            "./services/summaries"
      - name: Run container
        run: |
          docker run \
            -d \
            --name fastapi-tdd \
            -e PORT=8765 \
            -e ENVIRONMENT=dev \
            -e DATABASE_URL=sqlite://sqlite.db \
            -e DATABASE_TEST_URL=sqlite://sqlite.db \
            -e TAVILY_API_KEY=${{ secrets.TAVILY_API_KEY }} \
            -e OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }} \
            -p 5003:8765 \
            ${{ env.IMAGE_API }}:latest
      - name: Pytest
        run: docker exec fastapi-tdd python -m pytest .
      - name: Flake8
        run: docker exec fastapi-tdd python -m flake8 .
      - name: Black
        run: docker exec fastapi-tdd python -m black . --check
      - name: isort
        run: docker exec fastapi-tdd python -m isort . --check-only
