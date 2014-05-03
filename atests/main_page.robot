*** Settings ***
Resource          user_logged_in/manage_shops.robot

*** Variables ***
#
*** Test Cases ***
Go directly to the add page.
    Go To    ${HOST}/add_shop
    Page Should Contain Element    recaptcha_challenge_field