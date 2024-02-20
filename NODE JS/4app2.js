const names=require('./4app')//. means ik back  or require phr poori fiule chalti hai
const sayHi=require('./4utlis')
const data=require('./4alter')
console.log(names.jhon);
sayHi(names.jhon);
sayHi(names.peter);
console.log(data)
sayHi(data.singlePerson.name);
require('./5add');//isko na export kiya or na yaha call waha call full run file tw khud execute