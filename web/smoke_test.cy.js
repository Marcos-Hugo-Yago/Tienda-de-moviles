describe('Tienda de Móviles - Pruebas E2E', () => {

    beforeEach(() => {
        // Entramos en la raíz antes de cada test
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
        cy.get('.btn-login').first().click(); // Hacemos click en el botón de Iniciar sesión

        // Verificamos que el div de error ahora sea visible
        cy.get('.error').should('be.visible').and('contain', 'Usuario/clave errónea');
    });

    it('Debería loguearse correctamente y redirigir a moviles.html', () => {
        // Usamos las credenciales de tu archivo 'credenciales'
        cy.get('#username').type('root');
        cy.get('#password').type('example');
        cy.get('.btn-login').first().click();

        // Verificamos que la URL ha cambiado a moviles.html
        cy.url().should('include', '/moviles.html');
    });

    it('Debería navegar a la sección de comentarios', () => {
        cy.contains('Ver comentarios').click();
        cy.url().should('include', '/comentarios.html');
    });
});