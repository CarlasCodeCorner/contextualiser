# contextualiser

The contextualiser tool is an intelligent text-processing platform. I wish to use state-of-the-art Natural Language Processing Functionalities to automatedly extract siloed information from text  
*Key Features* 
- Use of Bert-Transformer Model (English) which can be retrained to the specific context
- use of mongoDB database 
- Microservice architecture
- interfacing with Angular Frontend

## Getting Started
1. Make yourself familiar with the Project. You require installation & setup to run the app locally. These include
    - Docker
    - Visual Studio Code
2. Clone git repository ``` git clone https://github.com/CarlasCodeCorner/contextualiser.git ```
3. build all docker containers (This may take a while) with ``` docker-compose up``` 
4. When all containers are running correctly, you should be able to open the SwaggerUI ``` localhost:8000```

### Local development
1. Create a [venv](https://docs.python.org/3/library/venv.html)
2. Copy the [launch.json]() to run the debugger mode in Visual Studio Code.

### How to use the repo
- development is only performed on the *development* branch
- I created a new branch for a particular feature I am working on
- code is tested. e.g. for Python: unittest

#### Git commands
1. pull current code to update  ``` git pull``` 
2. create new branch (local) ``` git checkout -b [dev-feature]``` 
3. add new branch to remote ```  git remmote add [name_of_remote: dev-feature] [dev-feature]``` 
4. checkout existing branch ``` git checkout [dev-feature]``` 
5. push to remote branch ``` git push [dev--feature] ``` 

#### Clean Code
1. I use Linters & Formatters, for Python: Pylint
2. I use [Docstrings](https://www.programiz.com/python-programming/docstrings) to comment each of the functions in the code. 

#### docker-compose
Each module of the app runs in a single docker-container. Docker containers are running linux shells of a underlying linux image. When you change something in your code, the image needs to be rebuild. However, only the one docker image, where you made the changes, not all of them. The Docker-compose.yaml defines each container (name, exposed ports, volume mounts). By starting the *docker-compose.yaml* with the command ``` docker-compose up```, you are triggering the docker engine to check if the images are already built. If not, it automatically builds the images and then starts the containers. Since we are running quite a large tool locally, make sure you have assigned enough memory to you docker engine.
