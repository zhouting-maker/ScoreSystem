<template>
  <div class="countdown-container">
    <div class="countdown-card">
      <h1 class="title">⏰ 倒计时</h1>

      <!-- 目标时间设置 -->
      <div class="settings">
        <div class="input-group">
          <label>目标日期</label>
          <input
            type="datetime-local"
            v-model="targetDate"
            class="input"
          />
        </div>
        <div class="input-group">
          <label>事件名称（可选）</label>
          <input
            type="text"
            v-model="eventName"
            placeholder="例如：新年倒计时"
            class="input"
          />
        </div>
        <button class="btn-start" @click="startCountdown" :disabled="!targetDate">
          {{ isRunning ? '重新开始' : '开始倒计时' }}
        </button>
      </div>

      <!-- 倒计时显示 -->
      <div v-if="isRunning" class="countdown-display">
        <div class="event-name" v-if="eventName">距离「{{ eventName }}」还有</div>
        <div class="time-units">
          <div class="time-block">
            <span class="time-value">{{ days }}</span>
            <span class="time-label">天</span>
          </div>
          <span class="separator">:</span>
          <div class="time-block">
            <span class="time-value">{{ hours }}</span>
            <span class="time-label">时</span>
          </div>
          <span class="separator">:</span>
          <div class="time-block">
            <span class="time-value">{{ minutes }}</span>
            <span class="time-label">分</span>
          </div>
          <span class="separator">:</span>
          <div class="time-block">
            <span class="time-value">{{ seconds }}</span>
            <span class="time-label">秒</span>
          </div>
        </div>
      </div>

      <!-- 倒计时结束 -->
      <div v-if="isFinished" class="finished">
        <div class="firework">🎉</div>
        <h2>{{ eventName || '倒计时' }}已到！</h2>
        <p class="finish-time">目标时间：{{ formattedTarget }}</p>
        <button class="btn-reset" @click="resetCountdown">重新设置</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CountdownPage',
  data() {
    return {
      targetDate: '',
      eventName: '',
      isRunning: false,
      isFinished: false,
      days: '00',
      hours: '00',
      minutes: '00',
      seconds: '00',
      timer: null,
    }
  },
  computed: {
    formattedTarget() {
      if (!this.targetDate) return ''
      const d = new Date(this.targetDate)
      return d.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      })
    },
  },
  methods: {
    startCountdown() {
      if (this.timer) {
        clearInterval(this.timer)
      }
      this.isRunning = true
      this.isFinished = false
      this.updateCountdown()
      this.timer = setInterval(this.updateCountdown, 1000)
    },
    updateCountdown() {
      const now = new Date()
      const target = new Date(this.targetDate)
      const diff = target - now

      if (diff <= 0) {
        clearInterval(this.timer)
        this.timer = null
        this.isRunning = false
        this.isFinished = true
        this.days = '00'
        this.hours = '00'
        this.minutes = '00'
        this.seconds = '00'
        return
      }

      const totalSeconds = Math.floor(diff / 1000)
      this.days = String(Math.floor(totalSeconds / 86400)).padStart(2, '0')
      this.hours = String(Math.floor((totalSeconds % 86400) / 3600)).padStart(2, '0')
      this.minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0')
      this.seconds = String(totalSeconds % 60).padStart(2, '0')
    },
    resetCountdown() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
      this.isRunning = false
      this.isFinished = false
      this.targetDate = ''
      this.eventName = ''
      this.days = '00'
      this.hours = '00'
      this.minutes = '00'
      this.seconds = '00'
    },
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
}
</script>

<style scoped>
.countdown-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  padding: 20px;
}

.countdown-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 48px 40px;
  width: 100%;
  max-width: 560px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.12);
  text-align: center;
}

.title {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 36px;
  letter-spacing: 2px;
}

.settings {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-align: left;
}

.input-group label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
}

.input {
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.06);
  color: #fff;
  font-size: 16px;
  outline: none;
  transition: all 0.3s;
}

.input:focus {
  border-color: #6c63ff;
  box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.3);
}

.input::placeholder {
  color: rgba(255, 255, 255, 0.35);
}

/* 让 datetime-local 的图标变白 */
.input::-webkit-calendar-picker-indicator {
  filter: invert(1);
  cursor: pointer;
}

.btn-start {
  padding: 14px 32px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #6c63ff, #a855f7);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 8px;
}

.btn-start:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(108, 99, 255, 0.4);
}

.btn-start:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 倒计时显示 */
.countdown-display {
  margin-top: 8px;
}

.event-name {
  color: rgba(255, 255, 255, 0.8);
  font-size: 18px;
  margin-bottom: 24px;
}

.time-units {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.time-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px 16px;
  min-width: 90px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.time-value {
  font-size: 52px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  background: linear-gradient(135deg, #6c63ff, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.time-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.separator {
  font-size: 40px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.3);
  margin-bottom: 24px;
}

/* 结束状态 */
.finished {
  margin-top: 16px;
}

.firework {
  font-size: 64px;
  margin-bottom: 16px;
  animation: bounce 1s ease infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.finished h2 {
  color: #fff;
  font-size: 28px;
  margin-bottom: 12px;
}

.finish-time {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  margin-bottom: 24px;
}

.btn-reset {
  padding: 12px 28px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  background: transparent;
  color: #fff;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-reset:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

/* 响应式 */
@media (max-width: 480px) {
  .countdown-card {
    padding: 32px 20px;
  }

  .time-block {
    min-width: 65px;
    padding: 14px 10px;
  }

  .time-value {
    font-size: 36px;
  }

  .separator {
    font-size: 28px;
  }

  .title {
    font-size: 26px;
  }
}
</style>
