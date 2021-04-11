'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./emotion.cjs.prod.js");
} else {
  module.exports = require("./emotion.cjs.dev.js");
}
