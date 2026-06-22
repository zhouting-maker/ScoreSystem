const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const pool = require('../db/pool');

const router = express.Router();

router.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const conn = await pool.getConnection();
  try {
    const [users] = await conn.execute('SELECT * FROM users WHERE username = ?', [username]);
    if (!users.length) return res.status(401).json({ error: 'Invalid credentials' });

    const user = users[0];
    const valid = await bcrypt.compare(password, user.password);
    if (!valid) return res.status(401).json({ error: 'Invalid credentials' });

    const token = jwt.sign({ id: user.id, role: user.role }, process.env.JWT_SECRET || 'secret', { expiresIn: '24h' });
    res.json({ token, user: { id: user.id, username: user.username, role: user.role, name: user.name } });
  } finally {
    conn.release();
  }
});

router.post('/register', async (req, res) => {
  const { username, password, name, role } = req.body;
  const conn = await pool.getConnection();
  try {
    const hash = await bcrypt.hash(password, 10);
    await conn.execute('INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
      [username, hash, name, role || 'student']);
    res.json({ success: true });
  } catch (err) {
    res.status(400).json({ error: err.message });
  } finally {
    conn.release();
  }
});

module.exports = router;
