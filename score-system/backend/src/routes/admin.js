const express = require('express');
const pool = require('../db/pool');
const { authMiddleware, roleMiddleware } = require('../middleware/auth');

const router = express.Router();

// 获取所有用户
router.get('/users', authMiddleware, roleMiddleware('admin'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const [users] = await conn.execute('SELECT id, username, name, role FROM users');
    res.json(users);
  } finally {
    conn.release();
  }
});

// 删除用户
router.delete('/users/:id', authMiddleware, roleMiddleware('admin'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    await conn.execute('DELETE FROM users WHERE id = ?', [req.params.id]);
    res.json({ success: true });
  } finally {
    conn.release();
  }
});

// 上报教育部 - JSON 格式
router.post('/publish-edu', authMiddleware, roleMiddleware('admin'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const [scores] = await conn.execute(`
      SELECT st.student_no, st.name, c.name as course, s.score, s.created_at
      FROM scores s
      JOIN students st ON s.student_id = st.id
      JOIN courses c ON s.course_id = c.id
    `);

    // 构造上报数据
    const reportData = {
      timestamp: new Date().toISOString(),
      institution: 'School Name',
      totalRecords: scores.length,
      records: scores.map(s => ({
        studentNo: s.student_no,
        studentName: s.name,
        courseName: s.course,
        score: s.score,
        reportDate: s.created_at
      }))
    };

    // 这里可以调用教育部 API
    console.log('Sending to EDU API:', JSON.stringify(reportData, null, 2));

    res.json({ success: true, message: 'Published to EDU system', recordCount: scores.length });
  } catch (err) {
    res.status(400).json({ error: err.message });
  } finally {
    conn.release();
  }
});

// 学生管理
router.get('/students', authMiddleware, roleMiddleware('admin', 'teacher'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const [students] = await conn.execute('SELECT * FROM students');
    res.json(students);
  } finally {
    conn.release();
  }
});

router.post('/students', authMiddleware, roleMiddleware('admin'), async (req, res) => {
  const { student_no, name, class_name } = req.body;
  const conn = await pool.getConnection();
  try {
    await conn.execute('INSERT INTO students (student_no, name, class_name) VALUES (?, ?, ?)',
      [student_no, name, class_name]);
    res.json({ success: true });
  } catch (err) {
    res.status(400).json({ error: err.message });
  } finally {
    conn.release();
  }
});

// 课程管理
router.get('/courses', authMiddleware, async (req, res) => {
  const conn = await pool.getConnection();
  try {
    const [courses] = await conn.execute('SELECT * FROM courses');
    res.json(courses);
  } finally {
    conn.release();
  }
});

router.post('/courses', authMiddleware, roleMiddleware('admin', 'teacher'), async (req, res) => {
  const { name, semester } = req.body;
  const conn = await pool.getConnection();
  try {
    await conn.execute('INSERT INTO courses (name, teacher_id, semester) VALUES (?, ?, ?)',
      [name, req.user.id, semester]);
    res.json({ success: true });
  } catch (err) {
    res.status(400).json({ error: err.message });
  } finally {
    conn.release();
  }
});

module.exports = router;
