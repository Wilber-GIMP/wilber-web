"""
INSTALL:

workon wilber
pip install fabric

USE:

fab prod deploy

"""
import sys
from functools import wraps

from fabric import Connection, task
from invoke import Responder
from fabric.config import Config


SERVER_SSH_USER = 'root'
SERVER_URL = 'wilber.social'

PROJECT_USER = 'django'
PROJECT_NAME = "wilber"
REPO_NAME = 'wilber-web'

PROJECT_PATH = "/home/{}/{}/{}".format(PROJECT_USER, REPO_NAME, PROJECT_NAME)
REPO_URL = "remote_repo_url"

RUN_STRING = 'sudo -u {} $SHELL -c "cd {} && {}"'
RUN_STRING = 'su {} -c "cd {} && {}"'

VIRTUAL_ENV = ". /home/{}/.virtualenvs/{}/bin/activate".format(PROJECT_USER, PROJECT_NAME)

def user(command, folder=PROJECT_PATH):
    return RUN_STRING.format(PROJECT_USER, folder, command)

def get_connection(ctx):
    try:
        with Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs) as conn:
            return conn
    except Exception as e:
        return None


def connect(function):
    @wraps(function)
    def connected(ctx, *args, **kwargs):
        if isinstance(ctx, Connection):
            conn = ctx
        else:
            conn = get_connection(ctx)
        kwargs['conn'] = conn
        ret = function(ctx, *args, **kwargs)
        return ret
    return connected



@task
def prod(ctx):
    ctx.user = SERVER_SSH_USER
    ctx.host = SERVER_URL


# check if file exists in directory(list)
def exists(file, dir):
    return file in dir


# git tasks
@task
@connect
def pull(ctx, branch="master", **kwargs):
    # check if ctx is Connection object or Context object
    # if Connection object then calling method from program
    # else calling directly from terminal
    conn = kwargs['conn']
    conn.run(user("git pull origin {}".format(branch)))


@task
@connect
def checkout(ctx, branch='master', **kwargs):
    if branch is None:
        sys.exit("branch name is not specified")
    print("branch-name: {}".format(branch))
    conn = kwargs['conn']
    conn.run(user("whoami"))
    conn.run(user("git checkout {branch}".format(branch=branch)))


@task
@connect
def install(ctx, **kwargs):
    conn = kwargs['conn']
    conn.run(user("{} && pip install -r requirements/prod.txt".format(VIRTUAL_ENV)))


@task
@connect
def migrate(ctx, **kwargs):
    conn = kwargs['conn']
    conn.run(user("{} && python manage.py migrate".format(VIRTUAL_ENV)))


@task
@connect
def collect(ctx, **kwargs):
    conn = kwargs['conn']
    conn.run(user("{} && python manage.py collectstatic --noinput".format(VIRTUAL_ENV)))




@task
@connect
def restart(ctx, **kwargs):
    conn = kwargs['conn']
    conn.run("service nginx restart")
    conn.run("service gunicorn-wilber restart")


@task
@connect
def status(ctx, **kwargs):
    conn = kwargs['conn']
    conn.run("service nginx status")
    conn.run("service gunicorn-wilber status")


@task
def deploy(ctx):
    conn = get_connection(ctx)
    if conn is None:
        sys.exit("Failed to get connection")

    print("\ncheckout to master branch...")
    checkout(conn, branch="master")

    print("\npulling latest code from dev branch...")
    pull(conn)

    print("\ninstalling requirements...")
    install(conn)

    print("\ncollecting static files...")
    collect(conn)

    print("\nmigrating database...")
    migrate(conn)

    print("\nRestarting server...")
    restart(conn)

    print("\nserver status:")
    status(conn)


