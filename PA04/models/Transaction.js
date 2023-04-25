
'use strict';
const mongoose = require( 'mongoose' );
const Schema = mongoose.Schema;
const ObjectId = mongoose.Schema.Types.ObjectId;

var transactionSchema = Schema( {
  description: { type: String },
  amount: { type: Number, required: true} ,
  category: {type: String, required: true},
  date: {type: Date, required: true},
  userId: {type:ObjectId, ref:'user' },
} );

module.exports = mongoose.model( 'Transaction', transactionSchema );