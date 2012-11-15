import json

from fabric.api import run, sudo, put
from fabric.contrib.project import rsync_project
from fabric.contrib.files import upload_template


def bootstrap():
    sudo('apt-get install rubygems')
    return sudo('gem install chef')

def run_chef(run_list):
    sudo('mkdir -p /etc/chef')
    put('chef-solo.rb', '/etc/chef/solo.rb', use_sudo=True)

    sudo('mkdir -p /var/chef')
    #put('attributes.json', '/etc/chef/attributes.json', use_sudo=True)
    #sudo('echo {0} > /etc/chef/attributes.json'.format(json.dumps(attributes)))
    upload_template('attributes.json.jinja2', '/etc/chef/attributes.json', context=dict(run_list=run_list), use_jinja=True, use_sudo=True)
    rsync_project('/var/chef-solo', 'chef/')

    sudo('chef-solo -c /etc/chef/solo.rb -j /etc/chef/attributes.json')

def run_ls():
    return run('ls')
