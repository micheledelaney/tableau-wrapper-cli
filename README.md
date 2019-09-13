# _Tableau Server Client Library Wrapper - Documentation _



# Content:

1. [Source code](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAX1Dnb)
2. [Dependencies & installation](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAlS5tK)
3. [Tableau Server CLI](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAF4vc4)
4. [Wrapper functions](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAljGBB)
    1. [Authenticate](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAi4XbG)
    2. [Download](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAbBE4g)
        1. [Download Workbook Or Datasource](https://quip-apple.com/PsnsA7FaZoNe#KbS9CACtKHg)
        2. [Download View As Image](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAPgcaH)
        3. [Download View As PDF](https://quip-apple.com/PsnsA7FaZoNe#KbS9CACllyp)
        4. Download View As CSV?
    3. [Publish](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAXxfMa)
    4. [Refresh](https://quip-apple.com/PsnsA7FaZoNe#KbS9CA4txWh)
    5. [Update](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAtcFbM)
    6. [Create](https://quip-apple.com/PsnsA7FaZoNe#KbS9CApgXQI)
    7. [Delete](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAir7Z1)
    8. Schedule?
    9. [Get project ID](https://quip-apple.com/PsnsA7FaZoNe#KbS9CATN9u4)
    10. [Get resource ID](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAvuF6K)
    11. [Get resource list](https://quip-apple.com/PsnsA7FaZoNe#KbS9CAkbJGF)



# Source code

→ Github: https://github.com/cmicheledelaney/tableau-cli

# Dependencies & installation

* Requirement: Python 3.7
* 6 imported libraries, 4 of them are in the standard library. The other two are pick and tableauserverclient. Only the tableauserverclient needs to be installed and imported for the wrapper functions, pick is only needed for the cli.

```
pip3 install tableauserverclient
pip3 install pick
```



# Tableau Server CLI

The CLI consists of two files, the wrapper module (tableau_wrapper.py) and the tableau_cli.py file. 
To start the CLI simply enter this in the terminal:

```
./tableau_cli
```

First, the CLI prompts you to enter the server url, the username and the password to authenticate. After the authentication succeeds, the user has to choose one of the following actions:

<img src="https://github.com/cmicheledelaney/tableau-cli/blob/master/CLI.png" width="300">

* download
* publish
* refresh
* update
* delete
* create
* exit

The user can pick one of the actions by moving the arrow with the arrow keys and hitting enter to choose. 
Depending on which action the user chooses, different steps get executed, for many of them the next step will be choosing the resource type (workbook/view/datasource). If the user wants to download a view, they select “download”, then “view”. They get a list of all the views on the server and get prompted to choose one.
After they can select the format (pdf/jpeg) and the process of downloading the view starts. When finished, the user gets directed back to the “home” screen with different action types to choose from.


# Wrapper functions

→ Github: [https://github.com/cmicheledelaney/tableau-cli/blob/master/tableau_wrapper.py](https://github.com/cmicheledelaney/tableau-cli)


## Authenticate 

Authenticates with credentials if server object None

**Parameters:**

* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server_url -- the url of the server to connect with
* server -- the server object if authenticated previosly


**Return value(s):**
server -- server object

**Exception(s):**
TypeError -- credentials are missing (either the server object or
username, password and server_url)

```
server = authenticate(server_url=<server_url>,
        username=<username>, password=<password>)
```



## Download

### Download workbook or datasource

Download the datasource or workbook.
Authetication happens by either passing the credentials (username, pass-
word and server_url) or the server object when previosly authenticated.

**Parameters:**

* resource_type -- workbook or datasource
* resource_name -- name of the resource to download
* project_name -- name of the project the resource is stored in
* path -- path of the resource to download to - current working directory by default
* server_url -- the url of the server to connect with
* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server -- the server object if authenticated previosly
* include_extract -- boolean if extract should be included in the download - default True


**Return value(s):**
resource_id -- ID of the published workbook

**Exception(s):**
NameError -- if resource_type is neither workbook nor datasource

```
file_path = download(resource_type="datasource",
        resource_name="Superstore", project_name="Default",
        server_url=<url>, username=<username>, password=<password>)
```



### Download view as image

Download a view as image.
Authetication happens by either passing the credentials (username, pass-
word and server_url) or the server object when previosly authenticated.

**Parameters:**

* resource_name -- name of the resource to download
* path -- path of the resource to download to - current working directory by default
* server_url -- the url of the server to connect with
* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server -- the server object if authenticated previosly
* resolution -- resultion of image ('low'/'medium'/'high')


**Return value(s):**
path -- path of the downlaoded image

**Exception(s):**
NameError -- if resolution is invalid

```
file_path = download_view_image(resource_name="Obesity",
        server_url=<url>, username=<username>, password=<password>,
        resolution="medium")
```



### Download view as PDF

Download a view as PDF.
Authetication happens by either passing the credentials (username, pass-
word and server_url) or the server object when previosly authenticated.

**Parameters:**

* resource_name -- name of the resource to download
* project_name -- name of the project the resource is stored in
* server_url -- the url of the server to connect with
* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server -- the server object if authenticated previosly
* path -- path of the resource to download to (default: cwd)
* orientation -- orientation of the PDF ('portrait'/'landscape')
* filter_key -- the key the view will get filtered on
* filter_value -- the value of the filter


**Return value(s):**
file_path -- path of the downlaoded PDF

**Exception(s):**
NameError -- Invalid orientation

```
file_path = download_view_pdf(resource_name="Obesity",
        server_url=<url>, username=<username>, password=<password>,
        orientation="landscape",
        filter_key="Region", filter_value="Asia")
```



## Publish

Publish a datasource or workbook.
Authetication happens by either passing the credentials (username, pass-
word and server_url) or the server object when previosly authenticated.

**Parameters:**

* resource_type -- workbook or datasource
* resource_name -- name of the resource to publish
* project_name -- name of the project the resource is stored in
* path -- path of the resource to publish
* mode — 'CreateNew'/'Overwrite'/'Append'
* server_url -- the url of the server to connect with
* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server -- the server object if authenticated previosly


**Return value(s):**
resource_id -- ID of the published workbook

**Exception(s):**
NameError -- if resource_type is neither workbook nor datasource

```
new_resource_id = publish(resource_type="workbook", path="Superstore.twbx", 
        project_name="Default", mode="CreateNew",
        server_url=<url>, username=<username>, password=<password>) 
```



## Refresh

Refresh a workbook or datasource.
Authetication happens by either passing the credentials (username, pass-
word and server_url) or the server object when previosly authenticated.

**Parameters:**

* resource_type -- workbook or datasource
* resource_name -- name of the resource to refresh
* project_name -- name of the project the resource is stored in
* server_url -- the url of the server to connect with
* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server -- the server object if authenticated previously


**Return value(s):**
resource_id -- ID of the refreshed workbook

**Exception(s):**
NameError -- if resource_type is neither workbook nor datasource

```
workbook_id = refresh(resource_name="Superstore",
        project_name="Default", resource_type="workbook", 
        username=<username>, password=<password>)
```



## Update

Update a workbook, datasource or project.
Authetication happens by either passing the credentials (username, pass-
word and server_url) or the server object when previosly authenticated.

**Parameters:**

* resource_type -- workbook, datasource or project
* resource_name -- name of the resource to refresh
* project_name -- name of the project the resource is stored in or name
* of the project to delete
* new_name -- new name for the chosen resource
* server_url -- the url of the server to connect with
* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server -- the server object if authenticated previosly


**Return value(s):**
resource_id -- ID of the refreshed workbook

**Exception(s):**
NameError -- if resource_type is neither workbook nor datasource

```
resource_id = update(resource_type="workbook", new_name="Superstore new", resource_name="Superstore", project_name="Default", server_url=<server_url>, username=<username>, password=<password>, server=None)
```



## Create




## Delete

Delete a workbook, datasource or project.
Authetication happens by either passing the credentials (username, pass-
word and server_url) or the server object when previosly authenticated.

**Parameters:**

* resource_type -- workbook, datasource or project
* resource_name -- name of the resource to refresh
* project_name -- name of the project the resource is stored in or name
* of the project to delete
* server_url -- the url of the server to connect with
* username -- username of the user to authenticate with
* password -- password of the user to authenticate with
* server -- the server object if authenticated previosly


**Return value(s):**
resource_id -- ID of the refreshed workbook

**Exception(s):**
NameError -- if resource_type is neither workbook nor datasource

```
resource_id = delete(resource_type="workbook", resource_name="Superstore", project_name="Default", server=<server_object>)
```



## Get project ID

Get the ID of a project

**Parameters:**
project_name -- name of the project the resource is stored in
server -- the server object

**Return value(s):**

* project_id -- ID of the resource
* project_object -- project object of given project_name


**Exception(s):**
NameError -- invalid project_name

```
project_id = get_project_id(project_name="Default", server)
```



## Get resource ID

Get the ID of a workbook or view

**Parameters:**

* resource_type -- type of the resource ('workbook'/'view')
* resource_name -- name of the resource
* project_name -- name of the project the resource is stored in
* server -- the server object


**Return value(s):**
resource_id -- ID of the resource
resource_object — object

**Exception(s):**
NameError -- if resource_type is neither workbook nor view
NameError -- invalid project_name or invalid resource_name

```
resource_id, resource_object = get_resource_id(resource_type="workbook",
        resource_name="Superstore", project_name="Default", server)
```



## Get resource list

Get a list of the resources of type resource_type on the server

**Parameters:**

* resource_type -- type of the resources
* 'workbook'/'view'/'datasource'/'project'
* server -- the server object


**Return value(s):**
all_resources -- list of all resources as objects

**Exception(s):**
NameError -- invalid resource_type

```
resource_list = get_resource_list(resource_type="view", server)
```

