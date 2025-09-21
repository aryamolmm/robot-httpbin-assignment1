#*** Settings ***
#Library    RequestsLibrary
#Library    Collections
#
#*** Variables ***
#${BASE_URL}    https://httpbin.org
#&{HEADERS}     X-Test=RobotFramework
#
#*** Test Cases ***
#Check Headers Endpoint
#    Create Session    httpbin    ${BASE_URL}
#    ${resp}=    Get On Session    httpbin    /headers    headers=${HEADERS}
#    Should Be Equal As Integers    ${resp.status_code}    200
#    ${json}=    To Json    ${resp.content}
#    Dictionary Should Contain Key    ${json}    headers
#    Should Be Equal    ${json['headers']['X-Test']}    RobotFramework
*** Settings ***
Resource    ../resources/keywords.robot
Library    ../resources/httpbin_library.py


*** Test Cases ***
Test GET Headers
    Create HTTP Session    httpbin
    Get Headers    httpbin
