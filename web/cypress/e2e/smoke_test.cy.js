describe('Tienda de Móviles - Pruebas E2E', () => {

    beforeEach(() => {
        cy.visit('/');
    });

    it('Debería cargar la página de inicio correctamente', () => {
        cy.contains('Tienda de Móviles').should('be.visible');
        cy.get('#username').should('be.visible');
        cy.get('#password').should('be.visible');
    });

    it('Debería mostrar error con credenciales incorrectas', () => {
        cy.get('#username').type('usuario_falso');
        cy.get('#password').type('clave_falsa');
        cy.get('.btn-login').first().click(); 
        cy.get('.error').should('be.visible').and('contain', 'Usuario/clave errónea');
    });

    it('Debería loguearse correctamente y entrar en la sección de móviles', () => {
    cy.visit(baseUrl, { timeout: 30000 });

    cy.get('input[name="username"]').type('root');
    cy.get('input[name="password"]').type('1234');
    cy.get('button[type="submit"]').click();

    cy.url({ timeout: 10000 }).should('match', /\/moviles/);

    cy.get('body').should('be.visible');
    
    cy.screenshot('login-exitoso');
  });
});
