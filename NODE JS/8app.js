//asynchronous
const {readFile,writeFile}=require('fs')
console.log('STARTING..............')
readFile('./content/first.txt','utf8',(err,result)=>{
    if(err){
        console.log(err);
        return
    }
    const first=result;
    readFile('./content/second.txt','utf8',(err,result)=>{
        if(err){
            console.log(err);
            return
        }
        const second=result;
        writeFile('./content/third.txt',`here is the result : ${first} ,${second}`,(err,result)=>{
            if(err){
                console.log(err);
                return
            }
            console.log('DONE.........');
        })
    })
})
console.log('NEW TASK STARING.............')//phale synchronous code chale ga full or arrow function asynchronous hoty 