*** Settings ***
Suite Setup       Create six shops with the different total price.
Suite Teardown    Erase database
Resource          ../manage_shops.robot
