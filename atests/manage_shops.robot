*** Settings ***
Library           Selenium 2 Library

*** Keywords ***
Add the Shop With Groceries
    [Arguments]    ${name}    ${city}    ${prices}=1
    Enter to the shop adding page
    Add Shop Information    ${name}    ${city}
    Add Grocery    rasvaton_maito    Valio    ${prices}
    Click Element    name=add_shop

Enter to the shop adding page
    Click Element    name=add_shop

Add Shop Information
    [Arguments]    ${name}    ${city}
    Input Text    name    ${name}
    Input Text    city    ${city}

Add Grocery
    [Arguments]    ${id}    ${name}    ${price}
    Input Text    ${id}_manufacturer    ${name}
    Input Text    ${id}_price    ${price}

Shop should exict in the list
    [Arguments]    ${shop}
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is a right shop in the list    ${shop}

Delete Shop
    [Arguments]    ${shop}
    Click Link    ${shop}
    Click Element    delete_shop
    Check that shop is not on main page    ${shop}

Check that shop is not on main page
    [Arguments]    ${shop}
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is not a shop in the list    ${shop}

Reload and check if there is a right shop in the list
    [Arguments]    ${shop_name}
    Reload Page
    Page Should Contain    ${shop_name}

Reload and check if there is not a shop in the list
    [Arguments]    ${shop_name}
    Reload Page
    Page Should Not Contain    ${shop_name}
