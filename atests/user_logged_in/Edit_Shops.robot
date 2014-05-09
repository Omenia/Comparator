*** Settings ***
Test Setup        Create Base Shop
Resource          manage_shops.robot

*** Variables ***

*** Test Cases ***
Modify one shop and one shop information
    Modify Shop Information    name    Citymarket Juva    Tokmanni
    Go To    ${HOST}
    Shop should exist on main page    Tokmanni
    [Teardown]    Delete Shop    Tokmanni Juva

Modify grocery price in one grocery
    Modify Shop Information    Oltermanni_price    Citymarket Juva    42.24
    Check that there are right price and whole basket price is right
    [Teardown]    Delete Shop    Citymarket Juva

Modify grocery manufacturor in one grocery
    Modify Shop Information    Suomalainen naudan jauheliha_manufacturer    Citymarket Juva    Leon Liha
    Go To    ${HOST}
    Modify Shop Information    Suomalainen rasvaton maito_manufacturer    Citymarket Juva    Sonjan Meijeri
    Page Should Contain    Leon Liha
    Page Should Contain    Sonjan Meijeri
    [Teardown]    Delete Shop    Citymarket Juva

Modify area
    Modify Shop Information    area    Citymarket Juva    Rantasalmi
    Go To    ${HOST}
    Shop should exist on main page    Rantasalmi
    [Teardown]    Delete Shop    Citymarket Rantasalmi

*** Keywords ***
Modify Shop Information
    [Arguments]    ${id field}    ${old name}    ${new name}
    Click Link    ${old name}
    Click Element    name=edit_shop
    Input Text    ${id field}    ${new name}
    Click Element    name=edit_shop

Create Base Shop
    Add the Shop With Groceries    Citymarket    Juva    Juva    00100
    Shop should exist on main page    Citymarket Juva

Check that there are right price and whole basket price is right
    Page Should Contain    42.24
    Page Should Contain    57.9
