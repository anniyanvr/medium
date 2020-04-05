//require('custom-env').env(process.argv[2]);
import "reflect-metadata";
import express from "express";
import bodyparser from "body-parser";  
import fetch from "node-fetch";
global["fetch"] = fetch;

const app = express();

app.use(bodyparser.json());
app.use(bodyparser.urlencoded({extended:false}));


module.exports = app;