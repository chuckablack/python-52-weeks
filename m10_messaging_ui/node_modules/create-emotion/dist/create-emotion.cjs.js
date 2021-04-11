'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./create-emotion.cjs.prod.js");
} else {
  module.exports = require("./create-emotion.cjs.dev.js");
}
