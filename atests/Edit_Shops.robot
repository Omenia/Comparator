*** Settings ***
Suite Setup       Create Base Shop
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
Modify one shop and one shop information
    Modify Shop Information    name    Citymarket Juva    Citymarket Rantasalmi
    Go To    ${HOST}
    Shop should exict in the list    Citymarket Rantasalmi
    [Teardown]    Delete Shop    Citymarket Rantasalmi

Modify gorcery price in one grocery
    Modify Shop Information    Oltermanni_price    Citymarket Juva    42.24
    Page Should Contain    42.24
    [Teardown]    Delete Shop    Juva

*** Keywords ***
Modify Shop Information
    [Arguments]    ${id field}    ${old name}    ${new name}
    Click Link    ${old name}
    Click Element    name=edit_shop
    Input Text    ${id field}    ${new name}
    Click Element    name=edit_shop

Create Base Shop
    Add the Shop With Groceries    Citymarket Juva    Juva
    Shop should exict in the list    Citymarket Juva
