const { test } = require("./test");

exports.handler = async function(event, context, callback) {
  console.log("ENVIRONMENT VARIABLES\n" + JSON.stringify(process.env, null, 2))
  console.log("EVENT\n" + JSON.stringify(event, null, 2))
  test()
  return "Hello from consumer1!"
}
