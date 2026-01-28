        const express = require("express")
        const app = express()
        const fs = require("fs/promises")
        
        app.use(express.json());
        app.use(express.text());
        app.use(express.urlencoded({ extended: true }));
        
        app.get("/",async(req,res)=>{
            try {
                const data = await fs.readFile("data.txt", "utf-8");
                res.type("text/plain").send(data);
            } catch (err) {
                res.status(500).send("Error");
            }
        })
        
        app.post("/",async(req,res)=>{
            try {
                await fs.writeFile("res.txt", req.body);
                res.send("Success")
            } catch (error) {
                console.log("Error",error)
                res.send("ERRRRRRRRRRRRRRRRRRR")
            }
        })
        
        app.listen(1111,()=>{
            console.log("Server created")
        })
