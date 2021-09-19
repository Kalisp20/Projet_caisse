Feature: Stock
    """
        Stock feature will test for successful and failed functionnallity attempts
    """

    Scenario: Success test for bills download
        Given I navigate to stock page
        And I click on bills button 
        When I select a supplier and date, taxe, marge, and bills in modal dialog
        Then Success dialog open

    Scenario: Failure test for bills download
        Given I navigate to stock page
        And I click on bills button 
        When I miss select a supplier or date, taxe, marge, and bills in modal dialog
        Then Input is failed and modal dialog don't disappear
    
    Scenario: Success test to add a product in stock 
        Given I navigate to stock page
        And I click on add product button 
        When I select a supplier and date, taxe, marge, and info product
        Then Success dialog open
    
    Scenario: Failure test to add a product in stock 
        Given I navigate to stock page
        And I click on add product button 
        When I miss select a supplier or date, taxe, marge, or info product
        Then Input is failed and modal dialog don't disappear

    Scenario: Success test to consult stock
        Given I navigate to stock page
        And I click on consult button 
        Then I navigate to stock view

    Scenario: I modify info to stock table
        Given I navigate to stock page
        And I click on consult button
        When I select day conservation
        
      