*** Settings ***
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
Add One Shop
    Add the Shop With Groceries    S-Market    Gotham City    GC    00500
    Shop should exict on main page    S-Market GC
    [Teardown]    Delete Shop    S-Market GC

Add one shop, with one price with comma.
    Add the Shop With Groceries    S-Market    Gotham City    GC    00500    1.4
    Shop should exict on main page    S-Market GC
    [Teardown]    Delete Shop    S-Market GC

Add one shop with scnadic character
    Add the Shop With Groceries    S-Market    Mäntsälä    Mäntsälä    00500
    Shop should exict on main page    S-Market Mäntsälä
    Aplying filter with \ scandic char shoul succeed.
    [Teardown]    Delete Shop    S-Market GC

*** Keywords ***
Aplying filter with \ scandic char shoul succeed.
    Select From List    city    Mäntsälä
    Click Element    name=apply_filter
    Shop should exict on main page    K-Market Mäntsälä
