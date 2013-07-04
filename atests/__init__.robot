*** Settings ***
Suite Setup       Open Browser    ${HOST}
Suite Teardown    Close Browser
Test Setup        Go To    ${HOST}
Library           Selenium 2 Library

*** Variables ***
${HOST}           http://localhost:8080/
