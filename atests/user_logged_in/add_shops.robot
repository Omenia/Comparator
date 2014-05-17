*** Settings ***
Resource          manage_shops.robot
Default Tags  regression


*** Variables ***

*** Test Cases ***
Add One Shop
    Add the Shop With Groceries    S-Market    Gotham City    GC    00500
    Shop should exist on main page    S-Market GC
    [Teardown]    Delete Shop    S-Market GC

Add one shop, with one price with comma.
    Add the Shop With Groceries    S-Market    Gotham City    GC    00500    1.4
    Shop should exist on main page    S-Market GC
    [Teardown]    Delete Shop    S-Market GC

Add one shop with scandic character
    Add the Shop With Groceries    S-Market    Mäntsälä    Mäntsälä    00500
    ${shop}=    Convert To String    S-Market Mäntsälä
    Shop should exist on main page    ${shop}
    Applying filter with \ scandic char should succeed.
    [Teardown]    Delete Shop    S-Market Mäntsälä

*** Keywords ***
Applying filter with \ scandic char should succeed.
    ${area}=    Convert To String    Mäntsälä
    ${shop}=    Convert To String    S-Market Mäntsälä
    Select From List    city    ${area}
    Click Element    name=apply_filter
    Shop should exist on main page    ${shop}
