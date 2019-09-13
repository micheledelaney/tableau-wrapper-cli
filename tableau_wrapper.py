#!/usr/bin/env python3

import tableauserverclient as TSC
import os


def publish(resource_type, project_name, path, mode, server_url=None,
            username=None, password=None, server=None):
    """
    Publish a datasource or workbook.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_type   -- workbook or datasource
    resource_name   -- name of the resource to publish
    project_name    -- name of the project the resource is stored in
    path            -- path of the resource to publish
    mode            -- 'CreateNew'/'Overwrite'/'Append'
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly

    Return value(s):
    resource_id     -- ID of the published workbook

    Exception(s):
    NameError       -- if resource_type is neither workbook nor datasource
    """

    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # get project_id
    project_id, _ = get_project_id(project_name, server)
    # if resource is a datasource create new object and publish
    if resource_type == "datasource":
        # Use the project id to create new datsource_item
        new_resource = TSC.DatasourceItem(project_id)
        # publish data source (specified in file_path)
        new_resource = server.datasources.publish(
                        new_resource, path, mode)
    # if resource is workbook create new object and publish
    elif resource_type == "workbook":
        # create new workbook
        new_resource = TSC.WorkbookItem(project_id)
        # publish workbook
        new_resource = server.workbooks.publish(new_resource, path, mode=mode,
                                                as_job=False)
    # raise error if resource_type is neither workbook nor datasource
    else:
        raise NameError("Invalid resource_type")
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (new_resource.id)


def refresh(resource_type, resource_name, project_name, server_url=None,
            username=None, password=None, server=None):
    """
    Refresh a workbook or datasource.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_type   -- workbook or datasource
    resource_name   -- name of the resource to refresh
    project_name    -- name of the project the resource is stored in
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly

    Return value(s):
    resource_id     -- ID of the refreshed workbook

    Exception(s):
    NameError       -- if resource_type is neither workbook nor datasource
    """

    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # get id
    resource_id, resource_object = get_resource_id(resource_type,
                                                   resource_name,
                                                   project_name, server)
    # if resource is a workbook get the id and refresh
    if resource_type == 'workbook':
        server.workbooks.refresh(resource_id)
    # if resource is a datasource get the id and refresh
    elif resource_type == 'datasource':
        server.datasources.refresh(resource_object)
    # raise error if resource_type id neither workbook nor datasource
    else:
        raise NameError("Invalid resource_type")
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (resource_id)


def delete(resource_type, resource_name=None, project_name=None,
           server_url=None, username=None, password=None, server=None):
    """
    Delete a workbook, datasource or project.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_type   -- workbook, datasource or project
    resource_name   -- name of the resource to refresh
    project_name    -- name of the project the resource is stored in or name
                       of the project to delete
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly

    Return value(s):
    resource_id     -- ID of the refreshed workbook

    Exception(s):
    NameError       -- if resource_type is neither workbook nor datasource
    """

    # check if necessary parameters are passed in
    if resource_type == 'project' and not project_name:
        raise TypeError("missing argument project_name")
    if ((resource_type == 'workbook' or resource_type == 'datasource') and
            (not resource_name or not project_name)):
        raise TypeError("missing argument resource_name or project_name")
    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # if resource is a workbook get the id and delete
    if resource_type == 'workbook':
        # get id
        resource_id, _ = get_resource_id(resource_type, resource_name,
                                         project_name, server)
        server.workbooks.delete(resource_id)
    # if resource is a datasource get the id and detele
    elif resource_type == 'datasource':
        # get id
        resource_id, _ = get_resource_id(resource_type, resource_name,
                                         project_name, server)
        server.datasources.delete(resource_id)
    # if resource is a datasource get the id and detele
    elif resource_type == 'project':
        resource_id, _ = get_project_id(project_name, server)
        server.projects.delete(resource_id)
    # raise error if resource_type is neither workbook nor datasource
    else:
        raise NameError("Invalid resource_type")
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (resource_id)


def update(resource_type, new_name, resource_name=None, project_name=None,
           server_url=None, username=None, password=None, server=None):
    """
    Update a workbook, datasource or project.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_type   -- workbook, datasource or project
    resource_name   -- name of the resource to refresh
    project_name    -- name of the project the resource is stored in or name
                       of the project to delete
    new_name        -- new name for the chosen resource
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly

    Return value(s):
    resource_id     -- ID of the refreshed workbook

    Exception(s):
    NameError       -- if resource_type is neither workbook nor datasource
    """

    # check if necessary parameters are passed in
    if resource_type == 'project' and not project_name:
        raise TypeError("missing argument project_name")
    if ((resource_type == 'workbook' or resource_type == 'datasource') and
            (not resource_name or not project_name)):
        raise TypeError("missing argument resource_name or project_name")
    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # if resource is a workbook get the object and update
    if resource_type == 'workbook':
        # get id and object
        resource_id, resource_object = get_resource_id(resource_type,
                                                       resource_name,
                                                       project_name, server)
        resource_object.name = new_name
        server.workbooks.update(resource_object)
    # if resource is a datasource get the object and update
    elif resource_type == 'datasource':
        # get id and object
        resource_id, resource_object = get_resource_id(resource_type,
                                                       resource_name,
                                                       project_name, server)
        resource_object.name = new_name
        server.datasources.update(resource_object)
    # if resource is a project get the object and update
    elif resource_type == 'project':
        # get id and object
        resource_id, resource_object = get_project_id(project_name, server)
        resource_object.name = new_name
        server.projects.update(resource_object)
    # raise error if resource_type is neither workbook nor datasource
    else:
        raise NameError("Invalid resource_type")
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (resource_id)


def create(project_name, description=None, content_permissions=None,
           server_url=None, username=None, password=None, server=None):
    """
    Create a project.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    project_name        -- name of the project the resource is stored in or
                           name of the project to delete
    description         -- description for the project
    content_permission  -- 'LockedToProject'/'ManagedByOwner'
                           default is 'ManagedByOwner'
    server_url          -- the url of the server to connect with
    username            -- username of the user to authenticate with
    password            -- password of the user to authenticate with
    server              -- the server object if authenticated previosly

    Return value(s):
    resource_id         -- ID of the created project
    """

    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    new_project = TSC.ProjectItem(project_name,
                                  content_permissions=content_permissions,
                                  description=description)
    # create the project
    new_project = server.projects.create(new_project)
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (new_project.id)


def download(resource_type, resource_name, project_name, server_url=None,
             username=None, password=None, path=None, server=None,
             include_extract=True):
    """
    Download the datasource or workbook.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_type   -- workbook or datasource
    resource_name   -- name of the resource to download
    project_name    -- name of the project the resource is stored in
    path            -- path of the resource to download to
                       current working directory by default
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly
    include_extract -- boolean if extract should be included in the download
                       default True

    Return value(s):
    resource_id     -- ID of the published workbook

    Exception(s):
    NameError       -- if resource_type is neither workbook nor datasource
    """

    # check if either all the necessary credentials or the server object are
    # there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # get id
    resource_id, _ = get_resource_id(resource_type, resource_name,
                                     project_name, server)
    # if resource is a workbook get the id and download
    if resource_type == "workbook":
        no_extract = not include_extract
        # download datasource
        file_path = server.workbooks.download(resource_id, filepath=path,
                                              no_extract=no_extract)
    # if resource is a datasource get the id and download
    elif resource_type == "datasource":
        # download datasource
        file_path = server.datasources.download(resource_id, path=path,
                                                include_extract=include_extract)
    # raise error if resource_type id neither workbook nor datasource
    else:
        raise NameError("Invalid resource_type")
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (file_path)


def download_view_image(resource_name, server_url=None, username=None,
                        password=None, path=None, server=None,
                        resolution="high"):
    """
    Download a view as image.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_name   -- name of the resource to download
    path            -- path of the resource to download to
                       current working directory by default
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly
    resolution      -- resultion of image ('low'/'medium'/'high')

    Return value(s):
    path            -- path of the downlaoded image

    Exception(s):
    NameError       -- if resolution is invalid
    """

    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # get id
    resource_id, resource_object = get_resource_id("view", resource_name,
                                                   project_name=None,
                                                   server=server)
    # request for high resolution
    if resolution == 'high':
        imageresolution = TSC.ImageRequestOptions.Resolution.High
    # request for medium resolution
    elif resolution == 'medium':
        imageresolution = TSC.ImageRequestOptions.Resolution.Medium
    # request for low resolution
    elif resolution == 'low':
        imageresolution = TSC.ImageRequestOptions.Resolution.Low
    else:
        raise NameError("Invalid resolution '{}'".format(resolution))
    # make request
    image_req_option = TSC.ImageRequestOptions(imageresolution)
    server.views.populate_image(resource_object, image_req_option)
    # write to disk
    if path is None:
        path = os.getcwd() + "/" + resource_object.name + ".jpeg"
    with open(path, "wb") as image_file:
        image_file.write(resource_object.image)
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (path)


def download_view_pdf(resource_name, project_name, server_url=None,
                      username=None, password=None, path=None, server=None,
                      orientation='portrait', filter_key=None,
                      filter_value=None):
    """
    Download a view as PDF.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_name   -- name of the resource to download
    project_name    -- name of the project the resource is stored in
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly
    path            -- path of the resource to download to (default: cwd)
    orientation     -- orientation of the PDF ('portrait'/'landscape')
    filter_key      -- the key the view will get filtered on
    filter_value    -- the value of the filter

    Return value(s):
    file_path       -- path of the downlaoded PDF

    Exception(s):
    NameError       -- Invalid orientation
    """

    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # get id and object
    resource_id, resource_object = get_resource_id("view", resource_name,
                                                   project_name=None,
                                                   server=server)
    # set landscape orientation for the pdf
    if orientation == 'landscape':
        orientation_req = TSC.PDFRequestOptions.Orientation.Landscape
    # set portrait orientation for the pdf
    elif orientation == 'portrait':
        orientation_req = TSC.PDFRequestOptions.Orientation.Portrait
    else:
        raise NameError("Invalid orientation '{}'".format(orientation))
    # set the PDF request options
    page_type = TSC.PDFRequestOptions.PageType.A4
    pdf_req_option = TSC.PDFRequestOptions(page_type=page_type,
                                           orientation=orientation_req)
    # (optional) set a view filter
    if filter_key and filter_value:
        pdf_req_option.vf(filter_key, filter_value)
    # retrieve the PDF for a view
    server.views.populate_pdf(resource_object, pdf_req_option)
    # get path
    if path is None:
        path = os.getcwd() + "/" + resource_object.name + ".pdf"
    # write to disk
    with open(path, "wb") as image_file:
        image_file.write(resource_object.pdf)
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (path)


def download_view_csv(resource_name, project_name, server_url=None,
                      username=None, password=None, path=None, server=None,
                      filter_key=None, filter_value=None):
    """
    Download a view as CSV.
    Authetication happens by either passing the credentials (username, pass-
    word and server_url) or the server object when previosly authenticated.

    Parameters:
    resource_name   -- name of the resource to download
    project_name    -- name of the project the resource is stored in
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server          -- the server object if authenticated previosly
    path            -- path of the resource to download to (default: cwd)
    filter_key      -- the key the view will get filtered on
    filter_value    -- the value of the filter

    Return value(s):
    file_path       -- path of the downlaoded PDF

    Exception(s):
    """

    # check if the either all the necessary credentials or the server object
    # are there and authenticate if necessary
    server, sign_out = check_credentials_authenticate(username, password,
                                                      server_url, server)
    # get id and object
    resource_id, resource_object = get_resource_id("view", resource_name,
                                                   project_name=None,
                                                   server=server)
    # (optional) set a view filter
    if filter_key and filter_value:
        csv_req_option.vf(filter_key, filter_value)
    # retrieve csv data
    server.views.populate_csv(resource_object)
    # set path
    if path is None:
        path = os.getcwd() + "/" + resource_object.name + ".csv"
    # write data to csv
    with open(path, 'wb') as f:
        # Perform byte join on the CSV data
        f.write(b''.join(resource_object.csv))
    if sign_out is True:
        # sign out from server
        server.auth.sign_out()
    return (path)


def check_credentials_authenticate(username=None, password=None,
                                   server_url=None, server=None):
    """
    Authenticates with credentials if server object None

    Parameters:
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with
    server_url      -- the url of the server to connect with
    server          -- the server object if authenticated previosly

    Return value(s):
    server          -- server object

    Exception(s):
    TypeError       -- credentials are missing (either the server object or
                       username, password and server_url)
    """

    # check if the either all the necessary credentials or the server object
    # are there
    if server is None and (server_url or username or password) is None:
        raise TypeError
    # if no server object got passed in authenticate with the credentials
    if server is None:
        sign_out = True
        server = authenticate(server_url, username, password)
    else:
        sign_out = False
    return (server, sign_out)


def authenticate(server_url, username, password):
    """
    Authenticate with credentials

    Parameters:
    server_url      -- the url of the server to connect with
    username        -- username of the user to authenticate with
    password        -- password of the user to authenticate with

    Return value(s):
    server          -- server object

    Exception(s):
    AuthError       -- authentication failed
    """

    try:
        tableau_auth = TSC.TableauAuth(username, password)
        server = TSC.Server(server_url)
        server.use_server_version()
        server.auth.sign_in(tableau_auth)
        return (server)
    except:
        raise


def get_project_id(project_name, server):
    """
    Get the ID of a project

    Parameters:
    project_name    -- name of the project the resource is stored in
    server          -- the server object

    Return value(s):
    project_id      -- ID of the resource
    project_object  -- project object of given project_name

    Exception(s):
    NameError       -- invalid project_name
    """

    # set the filter options
    options = TSC.RequestOptions()
    options.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                  TSC.RequestOptions.Operator.Equals,
                                  project_name))
    # make request
    filtered_result, _ = server.projects.get(req_options=options)
    if not filtered_result:
        raise NameError("Invalid project_name '{}'".format(project_name))
    # return the last object in the list (if there are multiple)
    project_object = filtered_result.pop()
    return (project_object.id, project_object)


def get_resource_id(resource_type, resource_name, project_name, server):
    """
    Get the ID of a workbook or view

    Parameters:
    resource_type   -- type of the resource ('workbook'/'view')
    resource_name   -- name of the resource
    project_name    -- name of the project the resource is stored in
    server          -- the server object

    Return value(s):
    resource_id     -- ID of the resource
    resource_object -- object

    Exception(s):
    NameError       -- if resource_type is neither workbook nor view
    NameError       -- invalid project_name or invalid resource_name
    """

    # set the filter request
    options = TSC.RequestOptions()
    options.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                  TSC.RequestOptions.Operator.Equals,
                                  resource_name))
    # how to filter by multiple values?
    if resource_type == 'workbook':
        filtered_result, _ = server.workbooks.get(req_options=options)
    elif resource_type == 'view':
        filtered_result, _ = server.views.get(req_options=options)
    elif resource_type == "datasource":
        filtered_result, _ = server.datasources.get(req_options=options)
    else:
        raise NameError("Invalid resource_type")
    if not filtered_result:
        raise NameError("No {} with the name '{}' on the server".format(resource_type, resource_name))
    if resource_type == "view":
        result = filtered_result.pop()
        return (result.id, result)
    for result in filtered_result:
        if result.project_name == project_name:
            return (result.id, result)
    raise NameError("No project with the name '{}' on the server".format(project_name))


def get_resource_list(resource_type, server):
    """
    Get a list of the resources of type resource_type on the server

    Parameters:
    resource_type   -- type of the resources
                       'workbook'/'view'/'datasource'/'project'
    server          -- the server object

    Return value(s):
    all_resources   -- list of all resources as objects

    Exception(s):
    NameError       -- invalid resource_type
    """

    if resource_type == "workbook":
        all_resources, pagination_item = server.workbooks.get()
    elif resource_type == "datasource":
        all_resources, pagination_item = server.datasources.get()
    elif resource_type == "project":
        all_resources, pagination_item = server.projects.get()
    elif resource_type == "view":
        all_resources, pagination_item = server.views.get()
    else:
        raise NameError("Invalid resource_type '{}'".format(resource_type))
    return (all_resources)
