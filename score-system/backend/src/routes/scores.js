const express = require('express');
const pool = require('../db/pool');
const { authMiddleware, roleMiddleware } = require('../middleware/auth');
const xl = require('excel4node');

const router = express.Router();

// 查询成绩
router.get('/', authMiddleware, async (req, res) => {
  const conn = await pool.getConnection();
  try {
    let query = `
      SELECT s.id, s.score, st.student_no, st.name, c.name as course_name
      FROM scores s
      JOIN students st ON s.student_id = st.id
      JOIN courses c ON s.course_id = c.id
    `;
    const params = [];

    if (req.user.role === 'teacher') {
      query += ' WHERE c.teacher_id = ?';
      params.push(req.user.id);
    } else if (req.user.role === 'student') {
      query += ' WHERE st.id = (SELECT id FROM students LIMIT 1)';
    }

    const [scores] = await conn.execute(query, params);
    res.json(scores);
  } finally {
    conn.release();
  }
});

// 录入成绩
router.post('/', authMiddleware, roleMiddleware('teacher'), async (req, res) => {
  const { student_id, course_id, score } = req.body;
  const conn = await pool.getConnection();
  try {
    await conn.execute(
      'INSERT INTO scores (student_id, course_id, score, created_by) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE score = ?, updated_at = NOW()',
      [student_id, course_id, score, req.user.id, score]
    );
    res.json({ success: true });
  } catch (err) {
    res.status(400).json({ error: err.message });
  } finally {
    conn.release();
  }
});

// 导出 Excel
router.get('/export', authMiddleware, roleMiddleware('teacher', 'admin'), async (req, res) => {
  const conn = await pool.getConnection();
  try {
    let query = `
      SELECT st.student_no, st.name, c.name as course, s.score
      FROM scores s
      JOIN students st ON s.student_id = st.id
      JOIN courses c ON s.course_id = c.id
    `;
    const params = [];

    if (req.user.role === 'teacher') {
      query += ' WHERE c.teacher_id = ?';
      params.push(req.user.id);
    }

    const [scores] = await conn.execute(query, params);

    const wb = new xl.Workbook();
    const ws = wb.addWorksheet('成绩');
    ws.cell(1, 1).string('学号');
    ws.cell(1, 2).string('姓名');
    ws.cell(1, 3).string('课程');
    ws.cell(1, 4).string('成绩');

    scores.forEach((s, i) => {
      ws.cell(i + 2, 1).string(s.student_no);
      ws.cell(i + 2, 2).string(s.name);
      ws.cell(i + 2, 3).string(s.course);
      ws.cell(i + 2, 4).number(s.score);
    });

    res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    res.setHeader('Content-Disposition', 'attachment; filename="scores.xlsx"');
    wb.write('scores.xlsx', res);
  } finally {
    conn.release();
  }
});

// 统计报表
router.get('/report', authMiddleware, async (req, res) => {
  const conn = await pool.getConnection();
  try {
    let query = `
      SELECT c.name, AVG(s.score) as avg_score, MAX(s.score) as max_score,
             MIN(s.score) as min_score, COUNT(*) as total
      FROM scores s
      JOIN courses c ON s.course_id = c.id
    `;
    const params = [];

    if (req.user.role === 'teacher') {
      query += ' WHERE c.teacher_id = ?';
      params.push(req.user.id);
    }

    query += ' GROUP BY c.id';

    const [report] = await conn.execute(query, params);
    res.json(report);
  } finally {
    conn.release();
  }
});

module.exports = router;
