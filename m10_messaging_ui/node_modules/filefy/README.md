# filefy
[![Build Status](https://travis-ci.org/mbrn/filefy.svg?branch=master)](https://travis-ci.org/mbrn/filefy)
[![npm package](https://img.shields.io/npm/v/filefy/latest.svg)](https://www.npmjs.com/package/filefy)
[![NPM Downloads](https://img.shields.io/npm/dt/filefy.svg?style=flat)](https://npmcharts.com/compare/filefy?minimal=true)
[![Follow on Twitter](https://img.shields.io/twitter/follow/baranmehmet.svg?label=follow+baranmehmet)](https://twitter.com/baranmehmet)


A javascript library to produce downloadable files such as in CSV, PDF, XLSX, DOCX formats

> Only CSV export is available for now!

## Installation

To install filefy with `npm`:

    npm install --save filefy

To install filefy with `yarn`:

    yarn add filefy

## Usage

```js
import { CsvBuilder } from 'filefy';

var csvBuilder = new CsvBuilder("user_list.csv")
  .setColumns(["name", "surname"])
  .addRow(["Eve", "Holt"])
  .addRows([
    ["Charles", "Morris"],
    ["Tracey", "Ramos"]
  ])
  .exportFile();
```

## Licence

This project is licensed under the terms of the [MIT license](/LICENSE).
