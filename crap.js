// 9 good reasons why javascript is garbage:

console.log('5'-3); // 2
console.log('5'+3); // '53'
console.log('5' - '4'); // 1
console.log('5' + + '5'); // '55'
console.log('foo' + + 'foo'); // 'fooNaN'
console.log('5' + - '2'); // '5-2'
console.log('5' + - + - - + - - + + - + - + - + - - - '-2'); // '52'

var x = 3;
console.log('5' + x - x); // 50
console.log('5' - x + x); // 5