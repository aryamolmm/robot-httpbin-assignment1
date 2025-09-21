*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    ../utils/data_generator.py
Library    ../utils/retry_decorator.py


*** Variables ***
${BASE_URL}    https://httpbin.org

*** Keywords ***
Create HTTP Session
    [Arguments]    ${session_name}=httpbin
    Create Session    ${session_name}    https://httpbin.org

Get Headers
    [Arguments]    ${session_name}=httpbin
    ${resp}=    Get Request    ${session_name}    /headers
    ${json}=    To Json    ${resp.content}
    ${headers}=    Get From Dictionary    ${json}    headers
    Log    ${headers}
    Should Contain    ${headers}    Host

Post Random User Data
    [Arguments]    ${session_name}
    ${data}=    Generate User Data
    ${resp}=    Post Request    ${session_name}    /post    json=${data}
    Log    ${resp.json()}
    Should Be Equal As Strings    ${resp.status_code}    200
