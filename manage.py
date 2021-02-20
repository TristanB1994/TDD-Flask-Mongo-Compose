#! /usr/bin/env python

import os
import json
import signal
import subprocess
import time
import shutil

import click
from flask_mongoengine import MongoEngine

# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)
    # print(f"env: {variable}:{os.environ[variable]}")

setenv("APPLICATION_CONFIG", "development")

APPLICATION_CONFIG_PATH = "config"
MONGO_BACKUP_PATH = f"docker/mongo/{os.getenv('APPLICATION_CONFIG')}/dump"
MONGO_DATA_PATH = f"docker/mongo/{os.getenv('APPLICATION_CONFIG')}/mongodata"
DOCKER_PATH = "docker"
COVERAGE_FILE = os.path.join(os.getcwd(), '.coveragerc')



def app_config_file(config):
    return os.path.join(APPLICATION_CONFIG_PATH, f"{config}.json")


def docker_compose_file(config):
    return os.path.join(DOCKER_PATH, f"{config}.yml")


def configure_env(config):
    # Read configuration from the relative JSON file
    with open(app_config_file(config)) as f:
        config_data = json.load(f)

    # Convert the config into a usable Python dictionary
    config_data = dict((i["name"], i["value"]) for i in config_data)

    for key, value in config_data.items():
        try:
            if key == 'MONGODB_SETTINGS':
                setenv(key, json.dumps(value))
                # print(f"Set {key}:{value}")

            if key == 'DEBUG_TB_PANELS':
                setenv(key, json.dumps(value))

            if key in os.environ:
                # print(f"duplicate: {key}:{value}")
                pass

            if not key in os.environ:
                setenv(key, value)
                # print(f"Set {key}:{value}")

        except Exception as error:
            print(f"config variable: {key}:{value} : {error}")

@click.group()
def cli():
    pass

# @cli.command()
@cli.command(context_settings={"ignore_unknown_options": True})
@click.option('--write/--no-write', default=False)
@click.option('--stage', envvar='APPLICATION_CONFIG')
@click.option('--username', envvar='MONGO_INITDB_ROOT_USERNAME')
@click.option('--password', envvar='MONGO_INITDB_ROOT_PASSWORD')
@click.option('--db', envvar='MONGO_INITDB_ROOT_DB')
def db_startup_script(write, stage, username, password, db):

    """
    Checks in "docker/mongo/docker-entrypoint-initdb.d" for init-mongo.js script. 
    
    If init-mongo.js file exists, check write arg, defults to False and prints scripts to console

    If no init-mongo.js file or write is True, writes file to docker entrypoint

    Pulls env variables from APPLICATION_CONFIG, generates script to initialize application db, and authenticate user

    :bool 'write' confirm overwrite of init script
    :env 'admin_user' define MONGO_INITDB_ROOT_USERNAME variable
    :env 'admin_password' define MONGO_INITDB_ROOT_PASSWORD
    :env 'db_str' define application database MONGO_INITDB_DATABASE
    
    """

    # Checks for config settings, sets them if not present
    if ( os.getenv("MONGO_INITDB_ROOT_USERNAME") or os.getenv("MONGO_INITDB_ROOT_PASSWORD") or os.getenv("MONGO_INITDB_DATABASE") ) == None:
        
        configure_env(stage)
        print(f"initialized {stage} env variables")
        
    if stage == 'testing':
        print(f"caught testing stage")
        write = True 

    # sets defaults based on config file
    admin_user_str = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    admin_password_str = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    db_str = os.getenv("MONGO_INITDB_DATABASE")

    MONGO_CONFIG_PATH = f"{DOCKER_PATH}/mongo/{stage}/docker-entrypoint-initdb.d/"

    if os.path.isfile(MONGO_CONFIG_PATH) and write == False:
        print(f"This function overwrites the current init-mongo.js file, to process add --write flag")

    if not os.path.isfile(MONGO_CONFIG_PATH):
        write = True

    if not os.path.isdir( MONGO_CONFIG_PATH ):
        print(f"caught {MONGO_CONFIG_PATH}")
        os.makedirs(MONGO_CONFIG_PATH)

    if not os.path.isdir( MONGO_DATA_PATH ):
        print(f"caught {MONGO_DATA_PATH}")
        os.makedirs(MONGO_DATA_PATH)

    if len( os.listdir(MONGO_DATA_PATH) ) > 0:
        print(f"To generate startup script, mongodata must be empty")
        write = False

    if write:

        select_db_statement = f"db.getSiblingDB('{db_str}');\n"

        insert_db_statement = "db.start.insertOne({'name':'db_primer'});\n"

        make_admin_statement = "db.createUser({ user: "+ f"'{admin_user_str}',"+f"pwd: '{admin_password_str}',"+"roles: [{role: 'readWrite',db: "+f"'{db_str}'"+"}]});\n"

        try:
            with open(f"{MONGO_CONFIG_PATH}init-mongo.js", 'w+') as f:
                f.write(select_db_statement)
                f.write(make_admin_statement)
                f.write(insert_db_statement)
                print(f"f: {f.name}")
            print(f"Script initialized")
        except Exception as error:
            print(f"error writing init script: {error}")

######################### Backup DB

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    configure_env(os.getenv("APPLICATION_CONFIG"))

    cmdline = ["flask"] + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


def docker_compose_cmdline(commands_string=None):
    config = os.getenv("APPLICATION_CONFIG")
    print(f"config: {config}") #, os_env: {os.environ}")

    configure_env(config)

    compose_file = docker_compose_file(config)
    print(f"compose_file: {compose_file}")

    if not os.path.isfile(compose_file):
        raise ValueError(f"The file {compose_file} does not exist")

    command_line = [
        "docker-compose",
        "-p",
        config,
        "-f",
        compose_file,
    ]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    print(f"command_line: {command_line}")
    return command_line


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    cmdline = docker_compose_cmdline() + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()

##### Modify for mongo
##### Modify for mongo

def run_mongo(statements, database=None):
    try:
        client = MongoEngine.mongoengine.connect(
            db=os.getenv("MONGODB_DB"),
            user=os.getenv("MONGODB_USERNAME"),
            password=os.getenv("MONGODB_PASSWORD"),
            host=os.getenv("MONGODB_HOST"),
            port=int(os.getenv("MONGODB_PORT")),
        )
    except Exception as error:
        print(f"Didn't connect to DB, check active venv")
        print(f"error: {error}")

    if not database == None:
        try:
            db = client.get_db(database)
        except Exception as error:
            print(f"{database} was not found")

    for entry in statements:
        db.insert(entry)

    MongoEngine.mongoengine.disconnect()

##### Modify for mongo
##### Modify for mongo


def wait_for_logs(cmdline, message):
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode("utf-8"):
        # print(logs)
        time.sleep(0.1)
        logs = subprocess.check_output(cmdline)


@cli.command()
@click.argument("filenames", nargs=-1)
def test(filenames):
    """
    Initializes test environment, loads testing config and sets it to env variables, generates init script if applicable for mongo, spins mongo container, then executes pytest
    """
    os.environ["APPLICATION_CONFIG"] = "testing"
    configure_env(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline("up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("logs db")
    wait_for_logs(cmdline, "Waiting for connections")

    ##### Modify for mongo
    ##### Modify for mongo

    # run_mongo([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    ##### Modify for mongo
    ##### Modify for mongo
    
    cmdline = ["pytest", "-s", "--verbosity=4", "--cov-report=term-missing","--cov=application"] # ,f"--cov-config={COVERAGE_FILE}", "-svv",
    cmdline.extend(filenames)
    print(f"test command: {cmdline}")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("down")
    subprocess.call(cmdline)


@cli.group()
def scenario():
    pass


@scenario.command()
@click.argument("name")
def up(name):
    os.environ["APPLICATION_CONFIG"] = f"scenario_{name}"
    config = os.getenv("APPLICATION_CONFIG")
    # print(f"config: {config}")

    scenario_config_source_file = app_config_file("scenario")
    scenario_config_file = app_config_file(config)

    if not os.path.isfile(scenario_config_source_file):
        raise ValueError(f"File {scenario_config_source_file} doesn't exist")
    shutil.copy(scenario_config_source_file, scenario_config_file)

    scenario_docker_source_file = docker_compose_file("scenario")
    scenario_docker_file = docker_compose_file(config)


    if not os.path.isfile(scenario_docker_source_file):
        raise ValueError(f"File {scenario_docker_source_file} doesn't exist")
    shutil.copy(docker_compose_file("scenario"), scenario_docker_file)


    configure_env(f"scenario_{name}")

    cmdline = docker_compose_cmdline("up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("logs db")
    wait_for_logs(cmdline, "ready to accept connections")

    cmdline = docker_compose_cmdline("port db 5432")
    out = subprocess.check_output(cmdline)
    port = out.decode("utf-8").replace("\n", "").split(":")[1]
    os.environ["POSTGRES_PORT"] = port


    ######################### Modify for mongo
    ######################### Modify for mongo

    run_mongo([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    ######################### Modify for mongo
    ######################### Modify for mongo

    scenario_module = f"scenarios.{name}"
    scenario_file = os.path.join("scenarios", f"{name}.py")
    if os.path.isfile(scenario_file):
        import importlib

        os.environ["APPLICATION_SCENARIO_NAME"] = name

        scenario = importlib.import_module(scenario_module)
        scenario.run()

    docker_output_json = subprocess.check_output(['docker','ps',"--format='{{ json .Names}}'"])
    docker_startup_names = docker_output_json.decode('unicode_escape').split('"')

    scenario_db_name = [ x for x in docker_startup_names if config and 'db' in x ][0]       

    ######################### Modify for mongo
    ######################### Modify for mongo

    cmdline = f"docker exec -it {scenario_db_name} psql -U {os.getenv('POSTGRES_USER')} -d {os.getenv('APPLICATION_DB')}"

    ######################### Modify for mongo
    ######################### Modify for mongo

    print("Your scenario is ready. If you want to open a SQL shell run")
    print(cmdline)


@scenario.command()
@click.argument("name")
def down(name):
    os.environ["APPLICATION_CONFIG"] = f"scenario_{name}"
    config = os.getenv("APPLICATION_CONFIG")

    cmdline = docker_compose_cmdline("down")
    subprocess.call(cmdline)

    scenario_config_file = app_config_file(config)
    os.remove(scenario_config_file)

    scenario_docker_file = docker_compose_file(config)
    os.remove(scenario_docker_file)


if __name__ == "__main__":
    cli()
