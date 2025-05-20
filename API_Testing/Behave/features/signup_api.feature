Feature: Signup API Test

  Scenario: Successful Signup
    Given the API endpoint is "https://www.bootcoding.in/codelab/api/v1/auth/signin"
    When I send a POST request with body
      """
      {
        "email": "wanjarikanak@gmail.com",
        "password": "Kanak@1234"
      }
      """
    Then the response status code should be 201
    And the response JSON should contain key "token"