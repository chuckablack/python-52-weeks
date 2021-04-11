"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    }
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var BaseBuilder_1 = __importDefault(require("../core/BaseBuilder"));
var CsvBuilder = /** @class */ (function (_super) {
    __extends(CsvBuilder, _super);
    function CsvBuilder(fileName) {
        var _this = _super.call(this) || this;
        _this._FileName = '';
        _this._Delimeter = ',';
        _this._Columns = [];
        _this._RowData = [];
        _this._FileName = fileName;
        return _this;
    }
    CsvBuilder.prototype.setColumns = function (columns) {
        this._Columns = columns;
        return this;
    };
    CsvBuilder.prototype.setDelimeter = function (delimeter) {
        this._Delimeter = delimeter;
        return this;
    };
    CsvBuilder.prototype.addRow = function (row) {
        this._RowData.push(row);
        return this;
    };
    CsvBuilder.prototype.addRows = function (rows) {
        this._RowData = this._RowData.concat(rows);
        return this;
    };
    CsvBuilder.prototype.escapeCell = function (cellData) {
        if (typeof cellData === 'string') {
            return '"' + cellData.replace(/\"/g, '""') + '"';
        }
        return cellData;
    };
    CsvBuilder.prototype.getRowData = function (row) {
        return row.map(this.escapeCell).join(this._Delimeter);
    };
    CsvBuilder.prototype.exportFile = function () {
        var _this = this;
        var dataArray = [];
        if (this._Columns && this._Columns.length > 0) {
            dataArray.push(this.getRowData(this._Columns));
        }
        this._RowData.forEach(function (row) {
            dataArray.push(_this.getRowData(row));
        });
        var csvContent = dataArray.join("\r\n");
        _super.prototype.exportFile.call(this, 'csv', this._FileName, csvContent);
    };
    return CsvBuilder;
}(BaseBuilder_1.default));
exports.default = CsvBuilder;
