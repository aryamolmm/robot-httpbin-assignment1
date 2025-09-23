*** Settings ***
Library    ../PikaLibrary.py

*** Variables ***
${QUEUE}      ci_cd_test_queue
${MESSAGE}    Hello from Jenkins CI/CD!

*** Test Cases ***
Publish And Consume Message
    [Documentation]    Publishes a message into RabbitMQ and validates it is consumed.
    Connect To Rabbitmq    host=${RABBITMQ_HOST}    port=${RABBITMQ_PORT}    username=guest    password=guest
    Create Queue           ${QUEUE}
    Publish Message        ${QUEUE}    ${MESSAGE}
    ${received}=           Consume Message    ${QUEUE}    timeout=10
    Should Be Equal        ${received}    ${MESSAGE}
    Close Connection
