#!/usr/bin/env python3

import pick
import tableau_wrapper as TW
import click
#import tableauserverclient as TSC
from tableauserverclient import ServerResponseError


def pick_object(all_resources, resource_type):
    """
    CLI - waits for the user to pick one of the resources

    Parameters:
    all_resources   -- list of all resources as objects
    resource_type   -- type of the resources
                       'workbook'/'view'/'datasource'/'project'

    Return value(s):
    resource        -- selected resource object
    resource_id     -- id of selected resource
    resource_name   -- name of selected resource

    Exception(s):
    NameError       -- invalid resource_type
    """

    all_resources_name = [single_object.name for single_object in all_resources]
    option, index = pick.pick(all_resources_name, title="Choose a {}:".format(resource_type), indicator='->')
    return (all_resources[index], all_resources[index].id, all_resources[index].name)


@click.group()
def cli():
    global server


@cli.command(help='Download a resource from the tableau server')
@click.option('-u', '--username', prompt=True, help='The username for authentication with the server')
@click.option('-p', '--password', prompt=True, hide_input=True, help='The password for authentication with the server')
@click.option('-s', '--server_url', prompt=True, help='The url for the server')
#@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']), prompt=True)
@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']))
@click.option('-n', '--object_name', help='The name of the resource')
@click.option('-pr', '--project_name', help='The name of the project')
def download_cli(object_type, object_name, username, password, server_url, project_name):
    server = authenticate_cli(username, password, server_url)
    # if user didn't specify what type of object they want to
    # download they'll get prompted to choose from a list
    if object_type is None:
        object_type, _ = pick.pick(['workbook', 'view', 'datasource'],
                                        title='What do you want to download?',
                                        indicator='->')
    if object_name is None:
        # get list of all the objects on the server of chosen type
        all_objects = TW.get_resource_list(object_type, server)
        # let user select one of the objects
        selected_object, object_id, object_name = pick_object(all_objects, object_type)
    else:
        object_id, selected_object = TW.get_resource_id(object_type, object_name, project_name, server)
        object_id = selected_object.id
    if object_type == "workbook" or object_type == "datasource":
        project_name = selected_object.project_name
        TW.download(resource_type=object_type, resource_name=object_name, project_name=project_name, server=server)
    elif object_type == "view":
        format, _ = pick.pick(['image', 'pdf', 'csv'], title='In which format would you like to download the view?', indicator='->')
        if format == 'pdf':
            TW.download_view_pdf(object_name, project_name=None, server=server)
        elif format == 'image':
            TW.download_view_image(object_name, server=server)
        elif format == 'csv':
            TW.download_view_csv(object_name, server=server, project_name=None)


@cli.command(help='Publish a workbook or datasource to the server')
@click.option('-u', '--username', prompt=True, help='The username for authentication with the server')
@click.option('-p', '--password', prompt=True, hide_input=True, help='The password for authentication with the server')
@click.option('-s', '--server_url', prompt=True, help='The url for the server')
@click.option('-m', '--mode', default="CreateNew")
@click.option('--project_name')
#@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']), prompt=True)
@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']))
@click.option('--publish_path', type=click.Path(exists=True), prompt="Please enter the path of the file you would like to publish")
def publish_cli(object_type, project_name, publish_path, username, password, server_url, mode):
    server = authenticate_cli(username, password, server_url)
    # if user hasn't specified yet what the resource_type is let them choose
    # one
    if object_type is None:
        object_type, _ = pick.pick(['workbook', 'datasource'],
                                        title='What do you want to publish?',
                                        indicator='->')
    # if user hasn't specified a resource_name yet let them pick one
    if project_name is None:
        # get list of all the objects on the server of chosen type
        all_objects = TW.get_resource_list("project", server)
        # let user select one of the objects
        selected_object, project_id, project_name = pick_object(all_objects,
                                                                   "project")
    # publish resource
    TW.publish(resource_type=object_type, path=publish_path,
            project_name=project_name, mode=mode, server=server)


@cli.command(help='Refresh a workbook')
@click.option('-u', '--username', prompt=True, help='The username for authentication with the server')
@click.option('-p', '--password', prompt=True, hide_input=True, help='The password for authentication with the server')
@click.option('-s', '--server_url', prompt=True, help='The url for the server')
@click.option('--object_name')
#@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']), prompt=True)
@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']))
def refresh_cli(object_name, object_type, username, password, server_url):
    try:
        server = authenticate_cli(username, password, server_url)
        # if user hasn't specified yet what the resource_type is let them choose one
        if object_type is None:
            object_type, _ = pick.pick(['workbook', 'datasource'],
                                            title='What do you want to refresh?', indicator='->')
        # if user hasn't specified a resource_name yet let them pick one
        if object_name is None:
            # get list of all the objects on the server of chosen type
            all_objects = TW.get_resource_list(object_type, server)
            # let user select one of the objects
            resource_object, _, object_name = pick_object(all_objects, object_type)
        # refresh the resource
        TW.refresh(object_type, object_name, resource_object.project_name, server=server)
    except ServerResponseError as err:
        print(err)


def authenticate_cli(username, password, server_url):
    try:
        server = TW.authenticate(server_url, username, password)
    except ServerResponseError as err:
        print(err)
        exit()
    return (server)


@cli.command(help='Create a project')
@click.option('-u', '--username', prompt=True, help='The username for authentication with the server')
@click.option('-p', '--password', prompt=True, hide_input=True, help='The password for authentication with the server')
@click.option('-s', '--server_url', prompt=True, help='The url for the server')
@click.option('--project_name')
@click.option('--description')
@click.option('--content_permission')
def create_cli(project_name, description, content_permission, username, password, server_url):
    server = authenticate_cli(username, password, server_url)
    # refresh the resource
    if project_name is None:
        project_name = input("Please enter a project name:\n")
    if description is None:
        description = input("Please enter a description for the project:\n")
    if content_permissions is None:
        content_permissions, _ = pick.pick(['ManagedByOwner', 'LockedToProject'], title='Please choose a content permission', indicator='->')
    TW.create(project_name, description, content_permissions, server=server)


@cli.command(help='Delete workbook, datasource or project')
@click.option('-u', '--username', prompt=True, help='The username for authentication with the server')
@click.option('-p', '--password', prompt=True, hide_input=True, help='The password for authentication with the server')
@click.option('-s', '--server_url', prompt=True, help='The url for the server')
@click.option('--project_name')
#@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']), prompt=True)
@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']))
@click.option('--object_name')
def delete_cli(object_name, object_type, project_name, username, password, server_url):
    server = authenticate_cli(username, password, server_url)
    # if user hasn't specified yet what the resource_type is let them choose one
    if object_type is None:
        object_type, _ = pick.pick(['workbook', 'datasource', 'project'],
                                        title='What do you want to delete?', indicator='->')
    # if user hasn't specified a resource_name yet let them pick one
    if object_name is None:
        # get list of all the objects on the server of chosen type
        all_objects = TW.get_resource_list(object_type, server)
        # let user select one of the objects
        resource_object, _, object_name = pick_object(all_objects, object_type)
    if object_type == "workbook" or object_type == "datasource":
        project_name = resource_object.project_name
    else:
        project_name = None
    # refresh the resource
    resource_id = TW.delete(object_type, object_name, project_name, server)
    return (resource_id)


@cli.command(help='Update workbook, datasource or project')
@click.option('-u', '--username', prompt=True, help='The username for authentication with the server')
@click.option('-p', '--password', prompt=True, hide_input=True, help='The password for authentication with the server')
@click.option('-s', '--server_url', prompt=True, help='The url for the server')
@click.option('-p', '--project_name')
#@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']), prompt=True)
@click.option('-t', '--object_type', type=click.Choice(['workbook', 'view', 'datasource']))
@click.option('-on', '--object_name')
@click.option('-n', '--new_name')
def update_cli(project_name, object_type, object_name, new_name, username, password, server_url):
    server = authenticate_cli(username, password, server_url)
    # if user hasn't specified yet what the resource_type is let them choose one
    if object_type is None:
        object_type, _ = pick.pick(['workbook', 'datasource', 'project'],
                                        title='What do you want to update?', indicator='->')
    # if user hasn't specified a resource_name yet let them pick one
    if object_name is None:
        # get list of all the objects on the server of chosen type
        all_objects = TW.get_resource_list(object_type, server)
        # let user select one of the objects
        resource_object, _, object_name = pick_object(all_objects, object_type)
    if object_type == "workbook" or object_type == "datasource":
        project_name = resource_object.project_name
    else:
        project_name = None
    # refresh the resource
    if new_name is None:
        new_name = input("Enter the new name for the {}:\n".format(object_type))
    TW.update(object_type, new_name, object_name, project_name, server=server)


if __name__ == "__main__":
    cli()
