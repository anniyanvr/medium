
'use strict'
import "reflect-metadata";
import { Connection } from "typeorm"; 
import { Database } from './database'  
import { serialize } from "class-transformer";  
import { User } from "./entity/User";

const awsServerlessExpress = require('aws-serverless-express')
const app = require('./app')
const awsServerlessExpressMiddleware = require('aws-serverless-express/middleware')
const server = awsServerlessExpress.createServer(app)

exports.handler = (event, context) => { awsServerlessExpress.proxy(server, event, context) }

app.use(awsServerlessExpressMiddleware.eventContext())

app.get('/getusers', async (req, res) => { 
    const database = new Database() 
    let connection: Connection = await database.getConnection();
    const users = await connection.getRepository(User).findOne(1, {});
    res.json(serialize(users))
}) 
 
