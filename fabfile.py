from fabric.api import *
from fabric.colors import green

def prod():
    HOST = 'psse.whit.com.au'
    env.hosts = [HOST]
    env.remote_app_dir ='/home/ubuntu/nmt/'
    env.user = 'ubuntu'

def deploy():
    require('hosts', provided_by=[prod])
    require('user', provided_by=[prod,])
    require('hg', provided_by=[prod,])
    require('remote_app_dir', provided_by=[prod,])

    # send the latest content to the analyst.
    print green("\n\n-----------------------")
    print green("pulling latest data on server")
    with cd(env.remote_app_dir):
        run('git pull')

    print green("\n\n-----------------------")
    print green("Restarting apache server")
    restart()


def restart():
    """Restart apache on the server."""
    require('hosts', provided_by=[prod])
    sudo('service apache2 restart', pty=False, shell=False)
