const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// Endpoint para servir el JSON de productos
app.get('/productos', (req, res) => {
    const jsonPath = path.join(__dirname, 'productos.json');
    fs.readFile(jsonPath, 'utf8', (err, data) => {
        if (err) {
            console.error("Error leyendo el archivo JSON:", err);
            return res.status(500).send('Error interno del servidor');
        }
        res.header("Content-Type", "application/json");
        res.send(data);
    });
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);
});