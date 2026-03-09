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

    it('Debería loguearse correctamente y redirigir a moviles.html', () => {
        cy.intercept('POST', '/api/usuarios/login', {
            statusCode: 200,
            body: { status: 'OK' }
        }).as('loginFalso');

        cy.get('#username').type('root');
        cy.get('#password').type('1234');
        cy.get('.btn-login').first().click();

        cy.wait('@loginFalso');
        cy.url().should('include', '/moviles.html');
        
        // EVIDENCIA 1: Captura del login exitoso
        cy.screenshot('evidencia-login-ok');
    });

    it('Debería navegar a la sección de comentarios', () => {
        // CAMBIO: Navegamos primero a la página que contiene el botón.
        // (Si moviles.html te bloquea por no estar logueado, tendrás que 
        // repetir el código de login mockeado del paso anterior aquí).
        cy.visit('/moviles.html'); 
        
        cy.contains('Ver comentarios').click();
        cy.url().should('include', '/comentarios.html');
        
        // CAMBIO: EVIDENCIA 2: Captura de la pantalla de comentarios
        cy.screenshot('evidencia-comentarios'); 
    });
});
