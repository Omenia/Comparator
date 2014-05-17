*** Settings ***
Test Setup        Go To    ${HOST}
Resource          ../manage_shops.robot
Default Tags  regression


*** Variables ***

*** Test Cases ***
With default setting by five shown shops, one should no been seen
    Shop should not exist on main page    K-Market MP

Filter more than five shops.
    Select From List    no_of_shops    20
    Click Element    name=apply_filter
    Shop should exist on main page    K-Market MP

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

Filter shops by price
    Select From List    order    Kallein
    Click Element    name=apply_filter
    Page Should Contain    K-Market MP
    Select From List    order    Halvin
    Click Element    name=apply_filter
    Page Should Not Contain    K-Market MP

Filter by most expencive, city, area.
    Select From List    order    Kallein
    Select From List    city    Gotham City
    Select From List    area    GC
    Click Element    name=apply_filter
    Page Should Contain    K-Market GC
