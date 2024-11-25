const express = require("express"); 
const mysql = require("mysql2");
const app = express();
app.use(express.static('public'));
const session = require("express-session");

app.use(
    session({
        secret: "OrionPax-16", 
        resave: false,
        saveUninitialized: true,
    })
);
let conexion = mysql.createConnection({
    host: "localhost",
    database: "Molino",
    user: "root",
    password: "root"
});

app.set("view engine", "ejs");
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static("public"));

// Ruta para la página principal
app.get("/", function(req, res) {
    res.render("Inicio");
});

app.get("/registro", function(req, res) {
    res.render("Registro");
});

// Ruta para la página de lobby después de iniciar sesión
app.get("/lobby", function(req, res) {
    res.render("Inicio");
});

app.get("/Sesion", function(req,res){
    res.render("LobbyI");
});

// Ruta para la página de inicio de sesión
app.get("/inicio", function(req, res) {
    res.render("index", { error: false });
});

// Registro de usuarios
app.post("/registrar", function(req, res) {
    const datos = req.body;
    let usuario = datos.usuario; 
    let nombre = datos.nombre;    
    let direccion = datos.direccion;  
    let telefono = datos.telefono;    
    let contraseña = datos.contrasena; 
    let registre = "INSERT INTO Tortilleria (Usuario, Nombre_Dueño, Dirección, Telefono, contraseña) VALUES (?, ?, ?, ?, ?)";
    conexion.query(registre, [usuario, nombre, direccion, telefono, contraseña], function(error) {
        if (error) {
            throw error;
        } else {
            console.log("Datos almacenados correctamente");
            res.redirect("/inicio");
        }
    });
});

// Validación de inicio de sesión
app.post("/validar", (req, res) => {
    const { usuario, contrasena } = req.body;
    let consulta = "SELECT * FROM Tortilleria WHERE usuario = ? AND contraseña = ?";
    conexion.query(consulta, [usuario, contrasena], (error, results) => {
        if (error) throw error;

        if (results.length > 0) {
            req.session.usuario = usuario;
            res.redirect("/Sesion"); 
        } else {
            res.render("index", { error: true });
        }
    });
});

app.listen(3000, function() {
    console.log("Servidor creado en http://localhost:3000");
});
