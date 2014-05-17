*** Test Cases ***
Most cheapest shop should have one euro sign
    #When Multiple Shops have created with different price classes (already done by suite setup)
    Then Most cheapest one have "€" sign

Average priced shop should have two euro sign
    #When Multiple Shops have created with different price classes (already done by suite setup)
    Then Most cheapest one have "€€" sign

Average priced shop should have three euro sign
    #When Multiple Shops have created with different price classes (already done by suite setup)
    Then Most cheapest one have "€€€" sign