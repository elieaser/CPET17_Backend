const express = require("express");
const mysql = require("mysql2");
const app = express();
const port = 3001;
const bodyParser = require('body-parser')
const cors = require('cors');
app.use(cors());
app.use(bodyParser.urlencoded({ limit: "50mb", extended: false }))

const connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "elai",
    database: "captured",
});

app.get("/", (req, res) => {
    console.log(req.query);
    res.send("hello");
});

app.get("/view", (req, res) => { 
    // querry display database
    connection.query(
        "SELECT * FROM `tbl_dt`",
            function (err, results) {
            console.log(results);
            res.json(results);})
});

app.post("/motion_detector", (req, res) => {
    const { Time_Captured, image } = req.body;
    // query insert to database
    connection.query(
        "INSERT INTO tbl_dt (Time_Captured, image) VALUES (?,?)  ",
        [Time_Captured, image]),
        function (err, results) {
            console.log(results);
            res.json(results);}
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
    