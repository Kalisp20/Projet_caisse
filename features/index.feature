Feature: Index
    """
        Index feature will test for functionnal links in index page
    """

    Scenario: Success Test for Home page
        Given I navigate to Home page

        When I click on Caisse
        Then I navigate to Caisse page

        When I click on Fournisseur
        Then I navigate to Fournisseur page

        When I click on Dashboard
        Then I navigate to Dashboard page

        When I click on Stock
        Then I navigate to Stock page
        
