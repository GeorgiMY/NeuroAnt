import express from "express";
import dotenv from 'dotenv';

dotenv.config();
const app = express();

// set the view engine to ejs
app.set('view engine', 'ejs');
app.use(express.static('public'));


// Set up routes
app.get('/', (req: express.Request, res: express.Response) => {
    res.render('index');
});

// Set up routes
app.get('/ant', (req: express.Request, res: express.Response) => {
    res.render('ant');
});

// Start the server
const PORT = process.env.PORT;

if (!process.env.PORT) throw new Error("No PORT value in .env");

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
    console.log(`||| http://localhost:${PORT} |||`)
});
