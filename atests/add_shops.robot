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
    Create six shops with the different total price.
    Check that shop is not on main page    K-Market MP
    [Teardown]    Remove six shops

*** Keywords ***
