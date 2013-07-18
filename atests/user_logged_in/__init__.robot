*** Settings ***
Suite Setup       Login
Suite Teardown    Close Browser
Test Setup        Go To    ${HOST}
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080/
