import os

import cli.app
import fabric.api
import fabric.tasks
import linode.api

import takeout.tasks as tasks

fabric.api.env.use_ssh_config = True

@cli.app.CommandLineApp
def takeout(app):
    if 'list' in app.params:
        #list_nodes()
        list_nodes()

def rdns_from_ip_list(iplist):
    for ip in iplist:
        if ip['ISPUBLIC']:
            return ip['RDNS_NAME']

def libcloud_list_nodes():
    from libcloud.compute.types import Provider
    from libcloud.compute.providers import get_driver
    import libcloud.security
    libcloud.security.VERIFY_SSL_CERT = False

    key = os.environ.get('LINODE_API_KEY')
    linode_driver = get_driver(Provider.LINODE)(key)

    for node in linode_driver.list_nodes():
        from pprint import pprint
        pprint(node)
        pprint(dir(node))
        print node.extra
        print node.size

def list_nodes():
    api = linode.api.Api()
    api.user_getapikey(username=os.getenv('LINODE_USERNAME'), password=os.getenv('LINODE_PASSWORD'))
    for node in api.linode_list():
        from pprint import pprint
        pprint(node)
        host = rdns_from_ip_list(api.linode_ip_list(LinodeID=node['LINODEID']))

        run_list = 'role[{}]'.format(node['LPM_DISPLAYGROUP'])
        #run_list = '",\n"'.join(['recipe[nginx]', 'recipe[philipcristiano]'])
        print fabric.tasks.execute(tasks.run_chef, host=host, run_list=run_list)


takeout.add_param("-l", "--list", help="list nodes", default=False, action="store_true")


if __name__ == "__main__":
    takeout.run()
