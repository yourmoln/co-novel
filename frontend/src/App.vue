<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <h1>co-novel AI小说助手</h1>
      </el-header>
      <el-main class="main">
        <router-view/>
      </el-main>
      <el-footer class="footer">
        <p>&copy; 2025 co-novel AI小说助手</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

.main {
  min-height: calc(100vh - 120px);
}

.footer {
  background-color: #f5f5f5;
  text-align: center;
  line-height: 60px;
}
</style>
