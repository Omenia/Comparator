*** Settings ***
Test Setup        Go To    ${HOST}
Resource          ../manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
With default setting by five shown shops, one should no been seen
    Shop should not exict on main page    K-Market MP

Filter more tha five shops.
    Select From List    no_of_shops    20
    Click Element    name=apply_filter
    Shop should exict on main page    K-Market MP

Filter shops by cities
    Select From List    city    Gotham City
    Click Element    name=apply_filter
    Page Should Contain    S-Market GC
    Page Should Not Contain    S-Market MP
    Page Should Contain    K-Market GC
    Page Should Not Contain    K-Market MP
    Page Should Contain    Lidl GC
    Page Should Not Contain    Lidl MP

Filter shops by postal code
    Select From List    postal_code    00500
    Click Element    name=apply_filter
    Page Should Contain    S-Market GC
    Page Should Not Contain    S-Market MP
    Page Should Contain    K-Market GC
    Page Should Not Contain    K-Market MP
    Page Should Contain    Lidl GC
    Page Should Not Contain    Lidl MP

Filter shops by areas
    Select From List    area    GC
    Click Element    name=apply_filter
    Page Should Contain    S-Market GC
    Page Should Not Contain    S-Market MP
    Page Should Contain    K-Market GC
    Page Should Not Contain    K-Market MP
    Page Should Contain    Lidl GC
    Page Should Not Contain    Lidl MP
