const fs = require('fs');
const { isEyeOpen } = require('.');


async function testOpen() {
  const imageBinary = fs.readFileSync('./images/test_image_open.jpg');
  console.log('Testing with an image of open eyes...');
  const result = await isEyeOpen(imageBinary);
  console.log(`Are the eyes open? ${result}`);
}

async function testClosed() {
  const imageBinary = fs.readFileSync('./images/test_image_closed.jpg');
  console.log('Testing with an image of closed eyes...');
  const result = await isEyeOpen(imageBinary);
  console.log(`Are the eyes open? ${result}`);
}

async function test() {
  await testOpen();
  await testClosed();
}

test();
