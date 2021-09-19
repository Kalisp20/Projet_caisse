Feature: Fournisseur
    """
        Login feature will test for successful and failed login attempts
    """

    Scenario: Success search attempts
        Given I navigate to supplier page
        When I click on search button
        Then Dialog modal open
        When I search a supplier ARMOR FRUIT
        Then I click to submit button
        Then Result view

    Scenario: Failed search attempts
        Given I navigate to supplier page
        When I click on search button
        Then Dialog modal open
        When I search a supplier '<<<<'
        Then I click to submit button 
        Then No result view   

    Scenario: Give up search supplier functionnallity
        Given I navigate to Supplier page
        When I click on search button
        Then Dialog modal open
        When I search a supplier ARMOR FRUIT
        Then I click to Close button
        Then Dialog modal close
    
    Scenario: Success consult attempts
        Given I navigate to supplier page
        When I click on consult button
        Then Success modal open
        Then Click to consult supplier
        Then View table Fournisseur
    
    Scenario: Success update consult result
        Given I navigate to consult supplier page
        When I input email and tel
        Then I update table fournisseur
    
    Scenario: Success delete a supplier
        Given I navigate to consult supplier page
        When I click to garbage button
        Then I confirm how to delete
       
    

