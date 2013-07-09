*** Settings ***
Suite Setup       Open Browser and login
Suite Teardown    Close Browser
Test Setup        Go To    ${HOST}
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080/
