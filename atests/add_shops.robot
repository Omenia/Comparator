*** Settings ***
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
Add One Shop
    Add the Shop With Groceries    S-Market GC    Gotham City
    Shop should exict on main page    S-Market GC
    [Teardown]    Delete Shop    S-Market GC

*** Keywords ***
