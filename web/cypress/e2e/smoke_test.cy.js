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
        // 1. INTERCEPTAMOS LA LLAMADA: Simulamos que el backend de Python responde "OK"
        cy.intercept('POST', '/api/usuarios/login', {
            statusCode: 200,
            body: { status: 'OK' }
        }).as('loginFalso');

        // 2. Rellenamos el formulario (ahora da igual la clave porque lo vamos a interceptar)
        cy.get('#username').type('root');
        cy.get('#password').type('1234');
        cy.get('.btn-login').first().click();

        // 3. Esperamos a que Cypress cace nuestra petición interceptada
        cy.wait('@loginFalso');

        // 4. Verificamos la redirección (debería ser instantánea)
        cy.url().should('include', '/moviles.html');

        cy.screenshot('evidencia-login-ok');
    });

    it('Debería navegar a la sección de comentarios', () => {
        cy.contains('Ver comentarios').click();
        cy.url().should('include', '/comentarios.html');
    });
});
