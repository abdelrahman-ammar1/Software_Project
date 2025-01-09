*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BASE_URL}          http://localhost:5000   # Update with your application's URL
${BROWSER}           chrome
${CUSTOMER_NAME}     Test Customer
${CUSTOMER_EMAIL}    test_customer2@example.com
${CUSTOMER_PASSWORD}  password123
${SALESPERSON_EMAIL}  mohamed@gmail.com
${SALESPERSON_PASSWORD}  1234

*** Test Cases ***

Sign Up As Customer
    [Documentation]    Test signing up as a new customer.
    Open Browser    ${BASE_URL}    ${BROWSER}
    Click Link      xpath=//a[contains(text(), 'Sign up here')]   # Navigate to the signup page
    Input Text      name=name      ${CUSTOMER_NAME}
    Input Text      name=email     ${CUSTOMER_EMAIL}
    Input Text      name=password  ${CUSTOMER_PASSWORD}
    Select From List By Value    name=role    Customer
    Click Button    xpath=//button[@type='submit']          # Submit the form
    Wait Until Page Contains    Login                       # Ensure the login page is displayed
    Close Browser

Book A Car
    [Documentation]    Test booking a car as a customer.
    Open Browser    ${BASE_URL}    ${BROWSER}

    # Step 1: Login as Customer
    Input Text      name=email     ${CUSTOMER_EMAIL}
    Input Text      name=password  ${CUSTOMER_PASSWORD}
    Select From List By Value    name=role    Customer
    Click Button    xpath=//button[@type='submit']
    Wait Until Page Contains    Welcome, Customer

    # Step 2: Navigate to "Book a Car" page
    Click Link      xpath=//a[contains(text(), 'Book a Car')]
    Wait Until Page Contains    Available Cars

    # Step 3: Book the first available car
    Click Button    xpath=//form[1]//button[@type='submit']   # Select the first car
    Wait Until Page Contains    Car booked successfully!      # Verify booking success

    # Step 4: Return to Customer Dashboard
    Click Link      xpath=//a[contains(text(), 'Back to Dashboard')]

    # Step 5: Verify dashboard still accessible
    Wait Until Page Contains    Welcome, Customer

    # Close the browser after the test
    Close Browser

Approve A Pending Booking
    [Documentation]    Test approving a pending booking as a salesperson.
    Open Browser    ${BASE_URL}    ${BROWSER}

    # Step 1: Login as Salesperson
    Input Text      name=email     ${SALESPERSON_EMAIL}
    Input Text      name=password  ${SALESPERSON_PASSWORD}
    Select From List By Value    name=role    Salesperson
    Click Button    xpath=//button[@type='submit']
    Wait Until Page Contains    Welcome, Salesperson

    # Step 2: Navigate to "View Bookings" page
    Click Link      xpath=//a[contains(text(), 'View All Bookings')]
    Wait Until Page Contains    Booking ID

    # Step 3: Approve the first pending booking
    Click Button    xpath=//form[1]//button[@type='submit']   # Approve the first pending booking
    Wait Until Page Contains    Approved                      # Wait for the status to update to "Approved"

    # Step 4: Verify the status change in the row
    Element Text Should Be    xpath=//table//tr[1]//td[last()]    Approved

    # Close the browser after the test
    Close Browser