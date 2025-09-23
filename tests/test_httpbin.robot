*** Settings ***
Library    ../resources/httpbin_library.py
Resource    ../resources/keywords.robot
Resource    resources/data_generator.robot
Library    ../data_generator.py    WITH NAME    dg
Library    ../httpbin_library.py   WITH NAME    hl
*** Test Cases ***
#Test GET Headers with Retry
#    Create HTTP Session
#    ${resp}=    Get Headers
#    Should Be Equal As Strings    ${resp.status_code}    200

Test GET Headers with Retry
    Create HTTP Session    httpbin
    Get Headers    httpbin

Test GET Headers
    Create Session    httpbin    https://httpbin.org
    ${resp}=    Get Request    httpbin    /headers
#    ${json}=    Evaluate    ${resp.json()}    modules=requests
     ${json}=    Call Method    ${resp}    json

    ${headers}=    Get From Dictionary    ${json}    headers
    Log    ${headers}
    Should Contain    ${headers}    Host

Test POST Random User Data with Retry
    [Documentation]    Test posting random user data with retry logic
#    ${data}=    dg.Generate User Data
#     ${data}=    Create Dictionary    name=TestUser    email=test@example.com
#     Create Session    httpbin    https://httpbin.org

    Create Session    httpbin    https://httpbin.org
    ${data}=    data_generator.Generate User Data
    Log    ${data}
    ${resp}=    Post Request    httpbin    /post    json=${data}
    Should Be Equal As Strings    ${resp.status_code}    200

#Generate User Data
#    ${data}=    Create Dictionary
#    ...    name=TestUser
#    ...    email=testuser@example.com
#    ...    age=25
#    [Return]    ${data}