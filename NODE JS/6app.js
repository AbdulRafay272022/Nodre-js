const path=require('path');
console.log(path.sep)//computer const salash use krta change folder ky liyh
const filepath=path.join('/content','text','text.txt');//kuch extra laga do hatta dega
console.log(filepath);
console.log(path.basename(filepath));
const absolutepath=path.resolve(__dirname,'content','text','text.txt');//it give absolute path and dirname points towards the directory that have node js in it
console.log(absolutepath);