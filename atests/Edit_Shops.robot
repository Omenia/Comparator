*** Settings ***
Test Setup        Create Base Shop
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
Modify one shop and one shop information
    Modify Shop Information    name    Citymarket Juva    Citymarket Rantasalmi
    Go To    ${HOST}
    Shop should exict on main page    Citymarket Rantasalmi
    [Teardown]    Delete Shop    Citymarket Rantasalmi

Modify gorcery price in one grocery
    Modify Shop Information    Oltermanni_price    Citymarket Juva    42.24
    Check that there are right price and whole basket price is right
    [Teardown]    Delete Shop    Citymarket Juva

Modify gorcery manufacturor in one grocery
    Modify Shop Information    Naudan Jauheliha_manufacturer    Citymarket Juva    Leon Liha
    Page Should Contain    Leon Liha
    [Teardown]    Delete Shop    Citymarket Juva

*** Keywords ***
Modify Shop Information
    [Arguments]    ${id field}    ${old name}    ${new name}
    Click Link    ${old name}
    Click Element    name=edit_shop
    Input Text    ${id field}    ${new name}
    Click Element    name=edit_shop

Create Base Shop
    Add the Shop With Groceries    Citymarket Juva    Juva    00100
    Shop should exict on main page    Citymarket Juva

Check that there are right price and whole basket price is right
    Page Should Contain    42.24
    Page Should Contain    57.9
