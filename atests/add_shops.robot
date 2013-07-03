*** Settings ***
Suite Setup       Open Browser    ${HOST}
Suite Teardown    Close Browser
Test Setup        Go To    ${HOST}
Test Teardown
Library           Selenium 2 Library

*** Variables ***
${HOST}           http://localhost:8080/

*** Test Cases ***
Add One Shop
    Add the Shop With Groceries    S-Market GC    Gotham City
    Shop should exict in the list    S-Market GC
    [Teardown]    Delete Shop    S-Market GC

Add six shops. One should not been seen.
    Add the Shop With Groceries    S-Market GC    Gotham City
    Add the Shop With Groceries    S-Market MP    Megapolis    5
    Add the Shop With Groceries    K-Market GC    Gotham City    3
    Add the Shop With Groceries    K-Market MP    Megapolis    6
    Add the Shop With Groceries    Lidl GC    Gotham City    2
    Add the Shop With Groceries    Lidl MP    Megapolis    4
    Check that shop is not on main page    K-Market MP
    [Teardown]    Remove six shops

*** Keywords ***
Enter to the shop adding page
    Click Element    name=add_shop

Add the Shop With Groceries
    [Arguments]    ${name}    ${city}    ${prices}=1
    Enter to the shop adding page
    Add Shop Information    ${name}    ${city}
    Add Grocery    Milk    ${prices}    l    1    rasvaton_maito
    Click Element    name=add_shop

Reload and check if there is a right shop in the list
    [Arguments]    ${shop_name}
    Reload Page
    Page Should Contain    ${shop_name}

Check that shop is not on main page
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

Delete Shop
    [Arguments]    ${shop}
    Click Link    ${shop}
    Click Element    delete_shop
    Check that shop is not on main page    ${shop}

Shop should exict in the list
    [Arguments]    ${shop}
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is a right shop in the list    ${shop}

Remove six shops
    Delete Shop    S-Market GC
    Delete Shop    S-Market MP
    Delete Shop    K-Market GC
    Delete Shop    K-Market MP
    Delete Shop    Lidl GC
    Delete Shop    Lidl MP
