describe('Tienda de Móviles - Pruebas E2E', () => {
  // Definimos la URL aquí arriba para que todos los tests la vean
  const urlApp = 'http://apacheb5:80';

  beforeEach(() => {
    // Limpieza antes de cada test
    cy.clearCookies();
    cy.clearLocalStorage();
  });

  it('Debería cargar la página de inicio correctamente', () => {
    cy.visit(urlApp, { timeout: 30000 });
    cy.get('body').should('be.visible');
  });

  it('Debería mostrar error con credenciales incorrectas', () => {
    cy.visit(urlApp);
    cy.get('input[name="username"]').type('usuario_falso');
    cy.get('input[name="password"]').type('9999');
    cy.get('button[type="submit"]').click();
    
    // Ajusta este texto según el mensaje de error real de tu app
    cy.contains(/incorrecto|error|fallido/i).should('be.visible');
  });

  it('Debería loguearse correctamente y entrar en la sección de móviles', () => {
    cy.visit(urlApp, { timeout: 30000 });

    // Login con credenciales conocidas
    cy.get('input[name="username"]').type('root');
    cy.get('input[name="password"]').type('1234');
    cy.get('button[type="submit"]').click();

    // Verificación flexible de la URL (que contenga 'moviles')
    cy.url({ timeout: 15000 }).should('match', /moviles/);
    
    // Verificación de que hay contenido
    cy.get('body').should('not.be.empty');
  });
});
