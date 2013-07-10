*** Settings ***
Resource          ../manage_shops.robot

*** Variables ***
${HOST}           http://localhost:8080

*** Test Cases ***
With default setting by five shown shops, one should no been seen
    Check that shop is not on main page    K-Market MP

Filter shops by cities
    Select From List    city    Gotham City
    Click Element    name=show_city
    Page Should Contain    S-Market GC
    Page Should Not Contain    S-Market MP
    Page Should Contain    K-Market GC
    Page Should Not Contain    K-Market MP
    Page Should Contain    Lidl GC
    Page Should Not Contain    Lidl MP
