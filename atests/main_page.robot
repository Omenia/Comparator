*** Settings ***
Resource          user_logged_in/manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
Go directly to the add page.
    Open Browser    ${HOST}/add_shop
    Page Should Contain Element    apply_filter
    [Teardown]    Close Browser
