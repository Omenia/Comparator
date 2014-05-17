*** Settings ***
Resource          ../manage_shops.robot

*** Test Cases ***
Most cheapest shop should have one euro sign
    #When Multiple Shops have created with different price classes (already done by suite setup)
    Then Most cheapest one have € sign

Average priced shop should have two euro sign
    #When Multiple Shops have created with different price classes (already done by suite setup)
    Then Avergage one have €€ sign

Average priced shop should have three euro sign
    #When Multiple Shops have created with different price classes (already done by suite setup)
    Then Most expencive one have €€€ sign

*** Keywords ***
Most Cheapest one have € sign
    Table Row Should Contain   shops    1    €

Avergage one have €€ sign
    Table Row Should Contain   shops    3    €€

Most expencive one have €€€ sign
    Table Row Should Contain   shops    5    €€€
