*** Variables ***
${BROWSER}     ff

*** Settings ***
Suite Setup       Open Browser    ${HOST}   ${BROWSER}
Resource          user_logged_in/manage_shops.robot
