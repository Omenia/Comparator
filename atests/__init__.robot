*** Variables ***

*** Settings ***
Suite Setup       Open Browser    ${HOST}   ${BROWSER}    alias=sut
Resource          user_logged_in/manage_shops.robot
