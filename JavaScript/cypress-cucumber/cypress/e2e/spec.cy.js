describe('template spec', () => {
  it('passes', () => {
    cy.visit('https://example.cypress.io')
  })
})

describe('My first test', () => {
  it('does not do much', () => {
    expect(true).to.equal(true);
  })

  it('visits the Kitchen Sink', () => {
    cy.visit('https://example.cypress.io');
    cy.contains('type').click()

    // Should be on a URL containing /commands/action
    cy.url().should('include', '/commands/action');

    // Get an input (given its class) and add text
    cy.get('.action-email').type('fake@email.com');

    // Verify that the value has been updated
    cy.get('.action-email').should('have.value', 'fake@email.com');
  })
})