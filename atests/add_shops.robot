*** Settings ***
Suite Setup       Open Browser    ${HOST}
Suite Teardown    Close Browser
Test Setup        Go To    ${HOST}
Test Teardown
Library           Selenium 2 Library

*** Variables ***
${HOST}           http://localhost:8080/

*** Test Cases ***
Add and Remove One Shop
    Add the Shop With Groceries    S-Market GC    Gotham City
    Got to page where are shop information
    Remove shop
    Check that shop is removed    S-Market GC

Add six shops. One should not been seen.
    Add the Shop With Groceries    S-Market GC    Gotham City
    Add the Shop With Groceries    S-Market MP    Megaplolis    5
    Add the Shop With Groceries    K-Market GC    Gotham City    3
    Add the Shop With Groceries    K-Market MP    Megaplois    6
    Add the Shop With Groceries    Lidl GC    Gotham City    2
    Add the Shop With Groceries    Lidl MP    Megapolis    4
    Check that shop is removed    K-Market MP

*** Keywords ***
Enter to the shop adding page
    Click Element    name=add_shop

Add the Shop With Groceries
    [Arguments]    ${name}    ${city}    ${prices}=1
    Enter to the shop adding page
    Add Shop Information    ${name}    ${city}
    Add Grocery    Milk    ${prices}    l    1    rasvaton_maito
    Click Element    name=add_shop
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is a right shop in the list    S-Market GC

Got to page where are shop information
    Click Link    S-Market GC

Reload and check if there is a right shop in the list
    [Arguments]    ${shop_name}
    Reload Page
    Page Should Contain    ${shop_name}

Remove Shop
    Click Element    delete_shop

Check that shop is removed
    [Arguments]    ${shop}
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is not a shop in the list    ${shop}

Reload and check if there is not a shop in the list
    [Arguments]    ${shop_name}
    Reload Page
    Page Should Not Contain    ${shop_name}

Add Shop Information
    [Arguments]    ${name}    ${city}
    Input Text    name    ${name}
    Input Text    city    ${city}

Add Grocery
    [Arguments]    ${name}    ${price}    ${quantity}    ${amount}    ${id}
    Input Text    ${id}_manufacturer    ${name}
    Input Text    ${id}_price    ${price}
    Input Text    ${id}_quantity    ${quantity}
    Input Text    ${id}_amount    ${amount}
