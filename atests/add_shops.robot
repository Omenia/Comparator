*** Settings ***
Library    Selenium 2 Library
Test Setup    Open Browser    http://localhost:8080/
Test Teardown    Close Browser

*** Test Cases ***
Add and Remove One Shop
    Enter to the shop adding page
    Add the Shop With Groceries    S-Market GC    Gotham City
    Got to page where are shop information
    Remove shop
    Check that shop is removed

*** Keywords ***
Enter to the shop adding page
    Click Element    name=add_shop

Add the Shop With Groceries
    [Arguments]    ${name}   ${city}
    Add Shop Information    ${name}    ${city}
    Add Grocery   Milk   1   l   1   rasvaton_maito
    Click Element    name=add_shop

Got to page where are shop information
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is a right shop in the list    S-Market GC
    Click Link    S-Market GC

Reload and check if there is a right shop in the list
    [Arguments]   ${shop_name}
    Reload Page
    Page Should Contain    ${shop_name}

Remove Shop
    Click Element    delete_shop

Check that shop is removed
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is not a shop in the list    S-Market GC

Reload and check if there is not a shop in the list
    [Arguments]   ${shop_name}
    Reload Page
    Page Should Not Contain    ${shop_name}

Add Shop Information
    [Arguments]   ${name}   ${city}
    Input Text    name    ${name}
    Input Text    city    ${city}

Add Grocery
    [Arguments]   ${name}    ${price}    ${quantity}    ${amount}   ${id}
    Input Text    ${id}_manufacturer    ${name}
    Input Text    ${id}_price    ${price}
    Input Text    ${id}_quantity    ${quantity}
    Input Text    ${id}_amount   ${amount}

