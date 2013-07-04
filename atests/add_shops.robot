*** Settings ***
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

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
Remove six shops
    Delete Shop    S-Market GC
    Delete Shop    S-Market MP
    Delete Shop    K-Market GC
    Delete Shop    K-Market MP
    Delete Shop    Lidl GC
    Delete Shop    Lidl MP
