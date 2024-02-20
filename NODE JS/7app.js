// sync method synchronous
const {readFileSync,writeFileSync}=require('fs');//const fs=require('fs') fs.readFileSync
console.log('STARTING..............')
const first =readFileSync('./content/first.txt','utf-8');
const second=readFileSync('./content/second.txt','utf-8');

console.log(first,second);

writeFileSync('./content/third.txt',`here is the result of sync : ${first} ,${second}`);//if there is no file it will create first same as python
writeFileSync('./content/second.txt',`the result of append is`,{flag:'a'});//to append
console.log('DONE.........')
console.log('NEW TASK STARING.............')