Feature: Caisse
    """
        Stock feature will test for successful and failed functionnallity attempts
    """

    Scenario: Success test for search product
        Given I navigate to caisse page
        And I click on search button
        When I put a product name in modal dialog 
        Then I can add to the cart among the results in the modal dialog a product and a quantity