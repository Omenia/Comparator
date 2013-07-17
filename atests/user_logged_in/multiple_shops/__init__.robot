*** Settings ***
Suite Setup       Create six shops with the different total price.
Suite Teardown    Remove six shops
Resource          ../manage_shops.robot
