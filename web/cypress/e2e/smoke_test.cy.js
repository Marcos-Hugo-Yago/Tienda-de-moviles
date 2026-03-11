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
        // 1. Ir explícitamente a la página de inicio o de login
        cy.visit('/'); // Cámbialo a '/login.html' si tu login está en otra URL

        // 2. Hacer un login REAL (Asegúrate de poner credenciales que existan en tu BD)
        cy.get('#username').clear().type('root');
        cy.get('#password').clear().type('1234'); // <-- Usa la contraseña correcta de tu BD
        cy.get('.btn-login').first().click();

        // 3. Comprobar que hemos entrado a la tienda
        cy.url().should('include', '/moviles.html');
        cy.screenshot('evidencia-login-ok');

        // 4. Esperar a que el botón sea visible y hacer click
        // Usamos should('be.visible') para asegurarnos de que no esté oculto
        cy.contains('Ver comentarios').should('be.visible').click();
        
        // 5. Comprobar la navegación final
        cy.url().should('include', '/comentarios.html');
        cy.screenshot('evidencia-comentarios');
    });
});
