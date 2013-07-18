*** Settings ***
Resource          user_logged_in/manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
Go directly to the add page.
    Go To    ${HOST}/add_shop
    Page Should Contain Element    apply_filter
    Go To    ${HOST}/edit_shop
    Page Should Contain Element    apply_filter
