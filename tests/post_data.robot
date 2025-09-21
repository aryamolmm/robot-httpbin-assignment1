*** Settings ***
Resource    ../resources/keywords.robot

*** Test Cases ***
Test POST Random Data
    Create HTTP Session    httpbin
    Post Random User Data    httpbin
