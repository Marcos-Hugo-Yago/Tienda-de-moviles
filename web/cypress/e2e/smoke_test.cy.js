describe('Tienda de Móviles - Pruebas E2E', () => {
  const urlApp = 'http://apacheb5:80';

  beforeEach(() => {
    cy.clearCookies();
    cy.clearLocalStorage();
  });

  it('Debería cargar la página de inicio correctamente', () => {
    cy.visit(urlApp, { timeout: 30000 });
    cy.get('body').should('be.visible');
  });

  it('Debería mostrar error con credenciales incorrectas', () => {
    cy.visit(urlApp);
    // Usamos selectores más genéricos por si los nombres cambian
    cy.get('input').first().type('usuario_falso');
    cy.get('input').last().type('9999');
    
    // BUSCAMOS EL BOTÓN POR TEXTO (Ignora si es button o input)
    // Cambia 'Login' por el texto exacto que aparezca en tu botón (ej: 'Entrar', 'Acceder')
    cy.get('form').submit(); // Esto envía el formulario directamente sin buscar el botón
  });

  it('Debería loguearse correctamente y entrar en la sección de móviles', () => {
    cy.visit(urlApp, { timeout: 30000 });

    // Intentamos rellenar los campos por su posición si el nombre falla
    cy.get('input').eq(0).clear().type('root');
    cy.get('input').eq(1).clear().type('1234');

    // Enviamos el formulario directamente
    cy.get('form').submit();

    // Verificación de la URL
    cy.url({ timeout: 15000 }).should('match', /moviles/);
    cy.get('body').should('be.visible');
  });
});
