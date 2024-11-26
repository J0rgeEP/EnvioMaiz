const ejs = require('ejs');
const fs = require('fs');
const path = require('path');

// Ruta al archivo EJS
const inputFile = path.join(__dirname, 'views/index.ejs');
const outputFile = path.join(__dirname, 'dist/index.html');

ejs.renderFile(inputFile, {}, (err, str) => {
  if (err) {
    console.error(err);
    return;
  }
  // Guarda el archivo HTML renderizado
  fs.writeFileSync(outputFile, str);
  console.log('Archivo HTML generado: ' + outputFile);
});
