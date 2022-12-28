import mysql from "mysql2/promise";

export default async function handler(req, res) {
    const connection = mysql.createConnection({
        host: "localhost",
        user: "root",
        password: "elai",
        socketPath: "/var/lib/mysql/mysql.sock"
    });
}

