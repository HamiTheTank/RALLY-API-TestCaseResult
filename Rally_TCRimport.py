import requests
import json

#---------------------------------------------------------------------------------------------------
#------------- VARIABLES ---------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

#obtain it from Rally Application manager: https://rally1.rallydev.com/login/accounts/index.html#/keys
API_KEY = ""

#Click on a test set in Rally iteration status.
#The last 12 digits in the URL are the test set's object id.
testSet_objectID = ""
#mandatory fields for test case results
import_date = "2020-02-29" #YYYY-MM-DD" format
import_build = "v1.0" #any string value is accepted
import_verdict = "Pass" #valid values: Inconclusive, Pass, Blocked, Error, Fail

#Workspace related info. Obtain here: https://rally1.rallydev.com/slm/webservice/v2.0/workspace
rallyAPIMajor = "2"
rallyAPIMinor = "0"
workspace_ref = ""
workspace_refObjectUUID = ""
workspace_refObjectName = ""
workspace_type = "Workspace"

#API addresses and request header
Rally_headers = {'ZSESSIONID' : API_KEY, 'Content-Type' : 'application/json', "Accept": "application/json"}
testcases_url = "https://rally1.rallydev.com/slm/webservice/v2.0/testcase"
testset_url = "https://rally1.rallydev.com/slm/webservice/v2.0/testset"
testcaseresult_url = "https://rally1.rallydev.com/slm/webservice/v2.0/testcaseresult/create"


#PAYLOAD TEMPLATE for importing test case results

myrequest= {
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

#---------------------------------------------------------------------------------------------------
#------------- FUNCTION DEFINITIONS ----------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


def get_testcaseIDs(testSetID):

    print('getting test case id\'s')
    params = {}
    params["query"] = '(TestSet.ObjectID = "' + testSetID + '")'
    params["workspace"] = workspace_ref
    params["pagesize"] = 200
    params["fetch"] = 'ObjectID'
    
    r = requests.get(url = testcases_url, params = params, headers = Rally_headers)
    print('Done. STATUS: ' + str(r.status_code))
    return r.text


    
def set_testcaseResults(testSetID, testCasesJSON, verdict):
    
    print('setting test case results...')    
    
    i = 1
    total = str(len(testCasesJSON["QueryResult"]["Results"]))
    
    for item in testCasesJSON["QueryResult"]["Results"]:        
        
        print('Progress: ' + str(i) + '/' + total)
        
        myrequest["TestCaseResult"]["Build"] = import_build
        myrequest["TestCaseResult"]["Date"] = import_date
        myrequest["TestCaseResult"]["TestCase"]["_ref"] = testcases_url + "/" + str(item["ObjectID"])
        myrequest["TestCaseResult"]["TestSet"]["_ref"] = testset_url + "/" + str(testSetID)
        myrequest["TestCaseResult"]["Verdict"] = verdict
        myrequest["TestCaseResult"]["Workspace"]["_rallyAPIMajor"] = rallyAPIMajor
        myrequest["TestCaseResult"]["Workspace"]["_rallyAPIMinor"] = rallyAPIMinor
        myrequest["TestCaseResult"]["Workspace"]["_ref"] = workspace_ref
        myrequest["TestCaseResult"]["Workspace"]["_refObjectUUID"] = workspace_refObjectUUID
        myrequest["TestCaseResult"]["Workspace"]["_refObjectName"] = workspace_refObjectName
        myrequest["TestCaseResult"]["Workspace"]["_type"] = workspace_type
        
        print('IMPORTING TEST CASE: ' + str(item["_ref"]))        
        r = requests.post(url = testcaseresult_url, data = json.dumps(myrequest), headers = Rally_headers)
        
        print('STATUS: ' + str(r.status_code))
        print(r.text)
        i += 1        
    
    print ('DONE')



#---------------------------------------------------------------------------------------------------
#------------- MAIN --------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


testcasesJSON = json.loads( get_testcaseIDs(testSet_objectID) )
set_testcaseResults( testSet_objectID, testcasesJSON, import_verdict )




