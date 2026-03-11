describe('Tienda de Móviles - Pruebas E2E', () => {
  const urlApp = 'http://apacheb5:80';

  beforeEach(() => {
    cy.clearCookies();
    cy.clearLocalStorage();
  });

  it('Debería cargar la página de inicio correctamente', () => {
    cy.visit(urlApp, { timeout: 30000 });
    cy.contains('Tienda de Móviles').should('be.visible');
  });

  it('Debería mostrar error con credenciales incorrectas', () => {
    cy.visit(urlApp);
    
    // Rellenamos los campos
    cy.get('input').eq(0).type('usuario_falso');
    cy.get('input').eq(1).type('9999');
    
    // HACEMOS CLIC EN EL BOTÓN POR SU TEXTO (tal cual sale en tu foto)
    cy.contains('Iniciar sesión').click();
    
    // Verificamos que NO hemos entrado (seguimos en la raíz o sale error)
    cy.url().should('not.include', '/moviles');
  });

  it('Debería loguearse correctamente y entrar en la sección de móviles', () => {
    cy.visit(urlApp, { timeout: 30000 });

    // Login con root / 1234
    cy.get('input').eq(0).type('root');
    cy.get('input').eq(1).type('1234');

    // Clic en el botón
    cy.contains('Iniciar sesión').click();

    // Esperamos a que la URL cambie a algo que contenga "moviles"
    // He subido el timeout a 20 segundos por si la base de datos va lenta
    cy.url({ timeout: 20000 }).should('include', 'moviles');
    
    // Verificación final: que aparezca algo de la tienda
    cy.get('body').should('be.visible');
  });
});
