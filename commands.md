# Commands

## Poetry - Python Package Manager

### **Steps**

> step 1: go to directory of your wish
> <br>
> step 2: terminal `poetry new <project name>` > <br>
> step 3: set poetry to create env in project dir -> terminal `poetry config virtualenvs.in-project true` > <br>
> step 4: terminal `poetry install` -> creates env in project folder and activates env
> <br>
> step 5: to install required packages -> terminal `poetry add <package name>`

### **Commands**

> `poetry add -D <package name>` -> install dev dependencies

## Alembic - DB Migrations Manager

### **Steps**

> step 1: terminal `alembic init <folder name>` -> <folder name> name of folder inside project dir
> <br>
> step 2: go to `alembic.ini` file and update line -> `sqlalchemy.url = <your DB URL>` > <br>
> step 3: got to `env.py` file inside the alembic folder -> <br>
> add lines: `from db.db_setup import Base` and also add all your models ex: `from db.models.user import User` `from db.models.section import Section` ...<br>
> modify line: `target_metadata = Base.metadata` > <br>
> step 4: terminal `alembic revision --autogenerate` -> code will be generated if not add lines, if incorrect please modify

### **Commands**

`alembic upgrade head` -> to upgrade migrations or changes made, for first time initialises the DB
<br>
`alembic downgrade base` -> to downgrade to previous versions/migrations
<br>
`alembic revision --autogenerate -m "<message>"` -> to autogenerate migration command after changes in models of DB

## Pre-commit - Code Formatter

### Steps

> step 1: configure `.pre-commit-config.yaml` file in project root
> <br>
> step 2: terminal `pre-commit install` -> installs pre-commit hooks
> <br>
> step 3: terminal `pre-commit run --all-files` -> runs pre-commit on all files

### Commands

`pre-commit run --all-files` -> runs pre-commit on all files
<br>
`pre-commit run <file name>` -> runs pre-commit on specific file
<br>
`pre-commit run --hook-id <hook id>` -> runs pre-commit on specific hook
<br>
`pre-commit install` -> installs pre-commit hooks
<br>
`pre-commit uninstall` -> uninstalls pre-commit hooks
<br>
`pre-commit clean` -> cleans pre-commit cache
<br>
`pre-commit autoupdate` -> updates pre-commit hooks

## Git - Version Control

### Commands

`git init` -> initializes git in project folder
<br>
`git add .` -> adds all files to staging area
<br>
`git commit -m "<message>"` -> commits changes to local repo
<br>
`git remote add origin <remote repo URL>` -> adds remote repo
<br>
`git push -u origin master` -> pushes changes to remote repo
<br>
`git pull origin master` -> pulls changes from remote repo
<br>
`git clone <remote repo URL>` -> clones remote repo to local
<br>
`git branch` -> lists all branches
<br>
`git checkout -b <branch name>` -> creates new branch
<br>
`git checkout <branch name>` -> switches to branch
<br>
`git merge <branch name>` -> merges branch to current branch
<br>
`git branch -d <branch name>` -> deletes branch
<br>
`git push origin --delete <branch name>` -> deletes branch from remote repo
<br>
`git log` -> lists all commits
<br>
`git reset --hard <commit hash>` -> resets to commit
<br>
`git reset --hard HEAD^` -> resets to previous commit
<br>
`git tag <tag name>` -> creates tag
<br>
`git tag -a <tag name> -m "<message>"` -> creates annotated tag
<br>
`git push origin <tag name>` -> pushes tag to remote
<br>


## Docker - Containerization

### Commands
`docker compose build` -> builds docker image
<br>
`docker compose up` -> starts docker container
<br>
`docker compose down` -> stops docker container
<br>
`docker compose ps` -> lists all containers
<br>
`docker cp <file_name> <container id>:<destination path>` -> copies files from container to host
<br>
`docker-compose up --build` -> builds and starts docker container -> useful when changes are made to dockerfile or project files
<br>
`docker prune` -> removes all stopped containers
