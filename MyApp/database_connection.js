const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'victorvega',
  password: 'victorvega',
  database: 'PropertEase'
});

connection.connect();

connection.query('SELECT * FROM PropertyOwner', function (error, results, fields) {
  if (error) throw error;
  console.log('The solution is: ', results);
});

connection.end();
