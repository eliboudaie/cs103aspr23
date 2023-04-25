const express = require('express');
const router = express.Router();
const Transaction = require('../models/Transaction');
const User = require('../models/User');
const mongoose = require('mongoose');

// Middleware function to check if the user is logged in.
function isLoggedIn(req, res, next) {
  if (req.locals.loggedIn) {
    next();
  } else {
    res.redirect('/login');
  }
}

// Get all transactions for the current user, sorted by date or amount.
router.get('/transaction/', isLoggedIn, async (req, res) => {
  const sortBy = req.query.sortBy || 'date';
  const sortOrder = req.query.sortOrder || 'desc';

  const transactions = await Transaction.find({ userId: req.user._id })
    .sort({ [sortBy]: sortOrder === 'desc' ? -1 : 1 });

  res.render('transaction/index', { transactions });
});

// Create a new transaction.
router.post('/transaction', isLoggedIn, async (req, res) => {
  const { description, amount, category, date } = req.body;

  const transaction = new Transaction({
    description,
    amount,
    category,
    date,
    userId: req.user._id,
  });

  await transaction.save();

  res.redirect('/transaction');
});

// Delete a transaction with the specified ID.
router.post('/transaction/remove/:transactionId', isLoggedIn, async (req, res) => {
  const transactionId = req.params.transactionId;

  await Transaction.deleteOne({ _id: transactionId });

  res.redirect('/transaction');
});

// Retrieve a transaction with the specified ID for editing.
router.get('/transaction/edit/:transactionId', isLoggedIn, async (req, res) => {
  const transactionId = req.params.transactionId;

  const transaction = await Transaction.findById(transactionId);

  res.render('transaction/edit', { transaction });
});

// Update a transaction with the specified ID.
router.post('/transaction/updateTransaction', isLoggedIn, async (req, res) => {
  const { transactionId, description, amount, category, date } = req.body;

  await Transaction.findOneAndUpdate(
    { _id: transactionId },
    { $set: { description, amount, category, date } },
  );

  res.redirect('/transaction');
});

// Retrieve all transactions for the current user, grouped by category.
router.get('/transaction/byCategory', isLoggedIn, async (req, res) => {
  const userId = req.user._id;

  const transactionsByCategory = await Transaction.aggregate([
    { $match: { userId: new mongoose.Types.ObjectId(userId) } },
    { $group: { _id: "$category", totalAmount: { $sum: "$amount" } } },
    { $sort: { _id: 1 } }
  ]);

  res.render('transaction/byCategory', { transactionsByCategory });
});

module.exports = router;