//http model
const http=require('http');

const server=http.createServer((req,res)=>{//req that user req and response what is send back
    res.write('hello world');//
    res.end();//close the response
    
})

server.listen(5000);//ismai port number btana hota hai jis pht server chale ga