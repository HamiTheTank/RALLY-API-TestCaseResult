# Import Rally Test Case Results


Use this Python script to import your test case results into CA Agile Center (formerly known as Rally). Follow this manual to configure the script based on your needs. This script imports the results to one specific test set and with one given verdict. Feel free to modify the script to make it more dynamic or make requests to me.

## Setup

In order to import test case results, you need to send a JSON payload to the Rally API in the below format.

```JSON
{
    "TestCaseResult": {
        "Build": "1.0",
        "Date": "YYY-MM-DD",
        "TestCase": {
            "_ref": ""
        },
        "TestSet": {
            "_ref": ""
        },
        "Verdict": "Pass",
        "Workspace": {
            "_rallyAPIMajor": "2",
            "_rallyAPIMinor": "0",
            "_ref": "",
            "_refObjectUUID": "",
            "_refObjectName": "",
            "_type": "Workspace"
        }
    }
}
```

### API KEY
To run API requests, you will need an API KEY. Obtain it from Rally Application manager:
[https://rally1.rallydev.com/login/accounts/index.html#/keys](https://rally1.rallydev.com/login/accounts/index.html#/keys).

### Test Set Object ID
This is a mandatory value because Rally requires you to bind your test case results to a particular test set. You can get this id by clicking on the test set in your Rally iteration status. The last 12 digits in the URL are the test set's object id. In the following example the object id is "288375028016".

```text
https://rally1.rallydev.com/#/134123839256d/iterationstatus?qdp=%2Fdetail%2Ftestset%2F288375028016
```


### Workspace values
You can obtain the workspace values from the following link: [https://rally1.rallydev.com/slm/webservice/v2.0/workspace](https://rally1.rallydev.com/slm/webservice/v2.0/workspace).

### Other values
All the other values are obtained dynamically by the script.

## Usage
Run **Rally_TCRimport.py** with the correct configuration.
