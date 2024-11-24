# iNaturalist Weed Status Updater

## Overview
The **iNaturalist Weed Status Updater** is a user-friendly web app that helps users manage weed status effectively. It accomplishes this by integrating [CAMS Weed Map](https://econet.nz/our-projects/) and iNaturalist's robust ecosystem.

## How it works
The user authenticates using their credentials in the [Weed Management Aotearoa NZ iNaturalist](https://www.inaturalist.org/projects/weed-management-aotearoa-nz). The authenticated user is  then authorised to set the observation field data values which is used for defining and managing the status of weed plants. An ArcGIS map displays the geolocation of the weed instances courtesy of EcoNet's [CAMS](https://econet.nz/our-projects/) Weeds Map.

## Key Features
- **OAuth2 Authentication**: Ensures secure access to iNaturalist accounts.
- **CRUD Field Updates**: Modify observation fields, such as weed control status, directly from the web app.
- **API Integration**: Works seamlessly with CAMS and iNaturalist data for improved weed management.

---
## User Interaction View

![image](https://github.com/user-attachments/assets/87bee0c4-7bb4-4715-9620-3be8058504e6)

1. The [**iNaturalist to CAMS synchroniser**](https://github.com/EcoNet-NZ/inaturalist-to-cams) automatically updates the CAMS Weeds Map hourly with any inputted observation data from iNaturalist.

2. Once the weed instance has fully synchronized from iNaturalist, an "Update weed status" button shows up when any weed instance is clicked on the **CAMS** Weeds Map.

3. Once the "Update weed status" button is clicked, **CAMS** application calls the iNaturalist application through the **iNaturalist Weed Status Updater**, which authorises the user to update the weed status. Where the user is not authenticated, iNaturalist prompts the user to authenticate with their credentials. 

4. The **iNaturalist Weed Status Updater** web form is then displayed where the observation fields are displayed which the user can update the weed status.

5. Once changes are made to the fields, the user clicks on the "Update Observation" button which then updates the relevant iNaturalist observation fields and records the activity.

## System View

The user is authenticated using iNaturalist's [OAuth2 Authorization Code Flow](https://www.inaturalist.org/pages/api+reference#auth).

After logging in, if required, the Authorization Code Flow redirects the user to the web app, a VueJS app deployed as an Azure Static Web App. This app calls a Python based Azure Serverless Function App which updates iNaturalist. 

This flow is shown in the following sequence diagram:

```mermaid
sequenceDiagram
    autonumber
    actor User
    box rgba(81,88,248,0.5) <br/>User Device<br/>
        participant cams as CAMS Weed Map
        participant br as Web Browser
    end
    box rgba(115,172,0,0.5)iNaturalist
        participant iNat as iNaturalist
    end
    box rgba(1,118,245,0.5) Azure
        participant web as iNaturalist Weed Status Updater<br/>Web App
        participant function as iNaturalist Weed Status Updater<br/>Function App
        participant env as Azure Environment
    end
    User->>cams: Select weed instance
    User->>cams: Click "Update Weed Status"<br/> button on pop-up
    cams->>iNat: GET (client id, redirect uri, observation id)
    alt if new login required
        iNat->>br: iNaturalist login page HTML
        br->>User: iNaturalist login page
        User-->>br: Enter username and password
        br-->>iNat: POST username and password
    end
    iNat->>+web: REDIRECT (code, observation id)
    activate br
    web-->>-br: Weed Status Updater web page HTML
    br->>User: Weed Status Updater web page
    User->>br: Select action, enter field values,<br/> press Update Observation
    br->>+function: POST (auth_code, observation field values)
    function->>env: Read CLIENT_ID, CLIENT_SECRET,<br/> REDIRECT_URI variables
    function->>iNat: POST (CLIENT_ID, CLIENT_SECRET,<br/> REDIRECT_URI, auth_code)
    iNat-->>function: access_token
    loop For each observation field value 
        function->>iNat: POST (access_token, observation field value)
        iNat-->>function: HTTP Response Code
    end
    alt 500 on any response
        function-->>br: failure message
    else 200 on all responses
        function-->>-br: success message
    end
    br-->>User: Shows success or failure message box
    deactivate br
```

Here's a description of the numbered steps on this sequence diagram:
1. The user selects a Weed Instance on the **CAMS** Weeds Map (running on ArcGIS Field Map or Experience Builder).
2. If the Weed Instance was sourced from iNaturalist (using the [iNaturalist to CAMS synchroniser](https://github.com/EcoNet-NZ/inaturalist-to-cams)), a pop-up shows an "Update Weed Status" button. 
3. When the user clicks on this button, it performs a GET request to the **iNaturalist OAuth2 endpoint** with hardcoded `client id` and `redirect uri` parameters plus a `state` parameter containing the iNaturalist `observation id` of the Weed Instance.
4. iNaturalist determines whether a new login is required. If so, iNaturalist returns the login HTML page. If not, jump to step 8.
5. The iNaturalist login page is displayed on the browser.
6. The user enters their username and password (assumed to be valid for this flow, otherwise an error is displayed and the flow stops).
7. On submitting the username and password, the request is submitted as a `POST` method call to iNaturalist server.
8. iNaturalist redirects the user to the **iNaturalist Weed Status Updater web app**, through the `redirect_uri` parameter passed in step 3. The redirect parameters includes a `authorization code` generated by iNaturalist and a `state` token containing the observation id (passed in step 3). These two parameters are read in the `created: function()` of `App.vue`. The `App.vue` file also contains a template of the user interface with the header, visit `date` field and an `iNaturalistUpdater` component for each of the potential states (Contolled, Alive, Dead or Duplicate).
9. The web app returns the Weed Status Updater HTML page.
10. The browser displays the Weed Status Updater.
11. The user selects the action to update the weed status (eg Controlled, Alive, Dead, Duplicate), fills in relevant fields and clicks on the `Update Observation` button (defined in `./components/iNaturalistUpdater.vue`).
12. This event calls the `updateObservation()` method which `POST`s the authorization code,  observation id and updated observation field data to the **Function App** (at `/api/update`). This calls the `update()` method in `function_app.py`.
13. The Function App reads the CLIENT_ID, CLIENT_SECRET and REDIRECT_URI from the Azure environment variables.
14. The Function App POSTs these variables and the authorization code to the iNaturalist OAuth2 endpoint.
15. The iNaturalist OAuth2 endpoint responds with the access token.
16. For each observation field value, the Function App POSTs the access token, observation field id and the observation field value to the **iNaturalist API**.
17. iNaturalist responds with a response code (for each observation field value call).
18. If any of these calls results in a **500** error response, the flow stops immediately. The Function App returns an error response code to the web page.
19. If all of the calls result in a **200 OK** response, the Function App returns a success response to the web page.
20. The web page displays either a success or failure message to the user dependent on which of the above two steps was executed.

## Creating your own custom iNaturalist updater
Should you wish to clone and modify this project, you'll also need to:

### Set up iNaturalist application
* Seek and obtain the right to create an [iNaturalist application](https://www.inaturalist.org/oauth/applications/new) from the author [nigelcharman](nigel.charman@econet.nz). In addition to filling out the form, your iNaturalist account must be at least 2 months old and you must have made at least 10 improving identifications over the last month. On certain instances, you will be required to provide an identification of a finer rank of Order towards improving other user's observations (not your own). 
* Once your request is approved, you can create the [iNaturalist application](https://www.inaturalist.org/oauth/applications/new). You'll want to add a placeholder for the Redirect URI until the web app is created. This can be updated later. Ensure you check ✅ the **CONFIDENTIAL** box (assuming you're storing the credentials securely, eg as Azure environment variables).
* Store the client **ID** and **Secret** variables securely as the `CLIENT_ID` and `CLIENT_SECRET` environment variables on your machine, so you can try out the code locally. You'll also need to store these as Azure environment variables.

### Set up Azure account
* Create an Azure account. These exercises are useful for learning about Azure Static Web Apps and Function Apps:
    * [Publish a **Vue** JavaScript app with Azure Static Web Apps](https://learn.microsoft.com/en-us/training/modules/publish-app-service-static-web-app-api/)
    * [Publish an API to Azure Static Web Apps](https://learn.microsoft.com/en-us/training/modules/publish-static-web-app-api-preview-url/)
    
* Create a new Azure Static Web App to use for your application.

* Set up the environment variables for the iNaturalist `CLIENT_ID` and `CLIENT_SECRET` obtained from iNaturalist (above) and the `REDIRECT_URI` environment variable to the external URL of the Static Web App (e.g. `https://[unique-id].azurestaticapps.net`). Follow the link on [how to set environment variables in the Azure portal](https://learn.microsoft.com/en-us/azure/static-web-apps/application-settings).

### Set the redirect uri on the iNaturalist application
* Edit the iNaturalist application and update the redirect URI to the external URL of the Static Web App (e.g. `https://[unique-id].azurestaticapps.net`).

### Copy this GitHub project and develop your application
* You'll need to merge the code in this project with the `.github/workflows` workflow from the newly created Azure Static Web App.
* Update the code as required.
* Creating a pull request on GitHub will generate a staging version of your app enabling a preview version of your site before publishing it. It won't be fully hooked up to iNaturalist since we have used the production URL as the redirect URI.
* Merging the pull request into your main branch will deploy the updated app to your production URL.

### Build a URL to call your application
Build the URL to start the flow at step 3 of the sequence diagram above. Given the `<client id>` from iNaturalist, the encoded URL (i.e. `https://` replaced with `https%3A%2F%2F`) of the Static Web App as `<redirect uri>` and the `<observation id>` of the observation you want to update, the URL will be:
`https://www.inaturalist.org/oauth/authorize?client_id=<client id>&redirect_uri=<redirect uri>&response_type=code&state=<observation id>`

## Hints
* `App.vue` contains the web app entry point and template, which then includes `iNaturalistUpdater` components.
* In addition to the component layout, `iNaturalistUpdater.vue` also defines the Observation Field Values that are to be updated as well as options for dropdown values, validation logic etc.
* Assuming you're only updating observation fields, you shouldn't need to change `function_app.py`.

## Feedback
We'd love your feedback, questions, issues and pull requests on this project. Get in touch if you need help getting it up and running. There's likely to be things I've missed in the instructions above.
