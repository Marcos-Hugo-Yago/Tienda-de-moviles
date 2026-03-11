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

    it('Debería loguearse y navegar a la sección de comentarios', () => {
        // 1. INTERCEPTAMOS LA LLAMADA (Login mockeado)
        cy.intercept('POST', '/api/usuarios/login', {
            statusCode: 200,
            body: { status: 'OK' }
        }).as('loginFalso');

        // 2. HACEMOS LOGIN
        cy.get('#username').type('root');
        cy.get('#password').type('1234');
        cy.get('.btn-login').first().click();

        // 3. ESPERAMOS Y COMPROBAMOS QUE ESTAMOS EN MÓVILES
        cy.wait('@loginFalso');
        cy.url().should('include', '/moviles.html');
        cy.screenshot('evidencia-login-ok'); // Primera foto

        // 4. COMO SEGUIMOS EN LA MISMA SESIÓN, NAVEGAMOS A COMENTARIOS
        cy.contains('Ver comentarios').click();
        cy.url().should('include', '/comentarios.html');
        cy.screenshot('evidencia-comentarios'); // Segunda foto
    });
});
