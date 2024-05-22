/* En este archivo JS se encuentra la lógica de las páginas secundarias, véase, "Ayuda" y "Acerca de"*/

// Fondo con animación fade-in al cargar la página
window.onload = function(){
  
  // Timeout para que dé tiempo a cargar las imágenes
  setTimeout(() => {document.querySelector('.capa_fade_fondo').classList.add('fade_out')}, "1500");
    
  }