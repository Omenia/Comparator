*** Settings ***
Suite Setup       Login
Suite Teardown    Close Browser
Test Setup        Go To    ${HOST}
Resource          manage_shops.robot

*** Variables ***
