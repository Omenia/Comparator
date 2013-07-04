*** Settings ***
Resource          manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
Modify one shop and one shop information
    Add the Shop With Groceries    Citymarket Juva    Juva
    Shop should exict in the list    Citymarket Juva
    Modify Shop Information    name    Citymarket Juva    Citymarket Rantasalmi
    Shop should exict in the list    Citymarket Rantasalmi
    [Teardown]    Delete Shop    Citymarket Rantasalmi

*** Keywords ***
Modify Shop Information
    [Arguments]    ${id field}    ${old name}    ${new name}
    Click Link    ${old name}
    Click Element    name=edit_shop
    Input Text    ${id field}    ${new name}
    Click Element    name=edit_shop
    Go To    ${HOST}
