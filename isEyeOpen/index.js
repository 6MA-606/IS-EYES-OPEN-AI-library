const fs = require("fs");
const { spawn } = require("child_process");
const path = require("path");

function isEyeOpen(imageBinary, earThreshold = 0.23) {
  return new Promise((resolve, reject) => {
    // Define the Python script path
    const pythonScript = path.join(__dirname, "eye_detection.py");

    // Spawn a Python process to execute the script
    const pythonProcess = spawn("python", [pythonScript, earThreshold]);

    let result = "";
    let error = "";

    // Handle errors in the stdin stream
    pythonProcess.stdin.on('error', (err) => {
      console.error('Error with stdin stream:', err);
      reject(err);
    });

    // Write the binary image data to the Python script's stdin
    pythonProcess.stdin.write(imageBinary, (err) => {
      if (err) {
        console.error("Error writing to stdin:", err);
        reject(err);
        return;
      }
      // Ensure the stream is closed after the data is written
      pythonProcess.stdin.end();
    });

    // Capture the Python script output
    pythonProcess.stdout.on("data", (data) => {
      result += data.toString();
    });

    // Capture errors from the Python script
    pythonProcess.stderr.on("data", (data) => {
      error += data.toString();
    });

    // Handle the closing of the process
    pythonProcess.on("close", (code) => {
      if (code !== 0) {
        console.error("Python process exited with error code:", code);
        reject(new Error(error || "Python process failed"));
        return;
      }

      // Clean up the result and return it as a boolean
      const cleanedResult = result.trim();

      if (cleanedResult === "true") {
        resolve(true);
      } else if (cleanedResult === "false") {
        resolve(false);
      } else {
        reject(new Error("Unexpected result: " + cleanedResult));
      }
    });

    // Handle any errors with the Python process itself
    pythonProcess.on('error', (err) => {
      console.error("Error with Python process:", err);
      reject(err);
    });
  });
}

module.exports = { isEyeOpen };
