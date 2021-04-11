"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var BaseBuilder = /** @class */ (function () {
    function BaseBuilder() {
    }
    BaseBuilder.prototype.exportFile = function (dataType, fileName, data) {
        if (window.navigator.msSaveOrOpenBlob) {
            var blob = new Blob([data]);
            window.navigator.msSaveOrOpenBlob(blob, fileName);
        }
        else {
            var charBom = "\uFEFF";
            var encodedData = encodeURIComponent(data);
            var content = "data:text/" + dataType + ";charset=utf-8," + charBom + encodedData;
            var link = document.createElement("a");
            link.setAttribute("href", content);
            link.setAttribute("download", fileName);
            document.body.appendChild(link);
            link.click();
        }
    };
    return BaseBuilder;
}());
exports.default = BaseBuilder;
