*** Settings ***
Library    ../PikaLibrary.py    WITH NAME    Pika



*** Test Cases ***
Publish And Consume Single Message
    Connect To RabbitMQ    host=rabbitmq    username=guest    password=guest
    Publish Message        test-queue    {"msg":"hello world"}
    ${msg}=    Consume Message    test-queue    timeout=5
    Should Be Equal As Strings    ${msg}    {"msg":"hello world"}
    Close Connection

Publish Five Messages And Consume
    Connect To RabbitMQ    host=rabbitmq    username=guest    password=guest
    FOR    ${i}    IN RANGE    5
        Publish Message    my-batch-queue    {"n": ${i}}
    END
    # consume all (example)
    :FOR    ${i}    IN RANGE    5
    \    ${m}=    Consume Message    my-batch-queue    timeout=3
    \    Log    Consumed: ${m}
    Close Connection
