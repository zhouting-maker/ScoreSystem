const express = require('express');
const router = express.Router();

// 计算字符串长度
router.post('/strlen', (req, res) => {
  const { str } = req.body;

  if (str === undefined || str === null) {
    return res.status(400).json({ error: '请提供 str 参数' });
  }

  const length = String(str).length;
  res.json({ str: String(str), length });
});

module.exports = router;

//计算输入的两个参数之和
router.post('/add', (req, res) => {
  const { a, b } = req.body;

  if (a === undefined || b === undefined) {
    return res.status(400).json({ error: '请提供 a 和 b 参数' });
  }

  const sum = Number(a) + Number(b);
  res.json({ a, b, sum });
});

// 计算数组元素之和
router.post('/sumArray', (req, res) => {
  const { arr } = req.body;

  if (!Array.isArray(arr)) {
    return res.status(400).json({ error: '请提供数组参数 arr' });
  }

  if (arr.length === 0) {
    return res.status(400).json({ error: '数组不能为空' });
  }

  const sum = arr.reduce((acc, val) => acc + Number(val), 0);
  res.json({ arr, sum });
});
