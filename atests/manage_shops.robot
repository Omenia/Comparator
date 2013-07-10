*** Settings ***
Library           Selenium 2 Library

*** Variables ***
${HOST}           http://localhost:8080

*** Keywords ***
Add the Shop With Groceries
    [Arguments]    ${name}    ${city}    ${prices}=1
    Enter to the shop adding page
    Add Shop Information    ${name}    ${city}
    Add Grocery with producer    rasvaton_maito    Valio    ${prices}
    Add Grocery without producer    reissumies    0.79
    Add Grocery without producer    oltermanni    6.95
    Add Grocery without producer    tomaatit    2.19
    Add Grocery with producer    jauheliha    Reilu    3.29
    Add Grocery without producer    jogurtti    2.45
    Add Grocery without producer    tutti-frutti    2.69
    Click Element    name=add_shop

Enter to the shop adding page
    Click Element    name=add_shop

Add Shop Information
    [Arguments]    ${name}    ${city}
    Input Text    name    ${name}
    Input Text    city    ${city}

Add Grocery with producer
    [Arguments]    ${id}    ${name}    ${price}
    Input Text    ${id}_manufacturer    ${name}
    Input Text    ${id}_price    ${price}

Shop should exict on main page
    [Arguments]    ${shop}
    Wait Until Keyword Succeeds    30s    0.2s    Reload and check if there is a right shop in the list    ${shop}

Delete Shop
    [Arguments]    ${shop}
    Go To    ${HOST}
    Click Link    ${shop}
    Click Element    delete_shop
    Shop should not exict on main page    ${shop}

Shop should not exict on main page
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

Add Grocery without producer
    [Arguments]    ${id}    ${price}
    Input Text    ${id}_price    ${price}

Create six shops with the different total price.
    Add the Shop With Groceries    S-Market GC    Gotham City
    Add the Shop With Groceries    S-Market MP    Megapolis    5
    Add the Shop With Groceries    K-Market GC    Gotham City    3
    Add the Shop With Groceries    K-Market MP    Megapolis    6
    Add the Shop With Groceries    Lidl GC    Gotham City    2
    Add the Shop With Groceries    Lidl MP    Megapolis    4

Remove six shops
    Delete Shop    S-Market GC
    Delete Shop    S-Market MP
    Delete Shop    K-Market MP
    Delete Shop    Lidl GC
    Delete Shop    Lidl MP
    Delete Shop    K-Market GC

Open Browser and login
    Open Browser    ${HOST}
    Click Link    Kirjautuminen
    Click Element    id=submit-login
    Go To    ${HOST}
