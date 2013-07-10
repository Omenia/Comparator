*** Settings ***
Resource          ../manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
With default setting by five shown shops, one should no been seen
    Shop should not exict on main page    K-Market MP

Filter more tha five shops.
    Select From List    no_of_shops    20
    Click Element    name=set_no_of_shops
    Shop should exict on main page    K-Market MP

Filter shops by cities
    Select From List    city    Gotham City
    Click Element    name=show_city
    Page Should Contain    S-Market GC
    Page Should Not Contain    S-Market MP
    Page Should Contain    K-Market GC
    Page Should Not Contain    K-Market MP
    Page Should Contain    Lidl GC
    Page Should Not Contain    Lidl MP