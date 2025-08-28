<template>
  <div>
    <h1>請求書管理アプリ 🧾</h1>
    <button @click="fetchMessage">バックエンドに接続テスト</button>
    <p v-if="message">バックエンドからの返事 👉 {{ message }}</p>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// バックエンドからのメッセージを保持する場所
const message = ref('')
const error = ref('')

// バックエンドにデータを要求する関数
const fetchMessage = async () => {
  try {
    // バックエンドのAPI (http://localhost:8000/) を呼び出す
    const response = await fetch('http://localhost:8000/')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    message.value = data
    error.value = '' // エラーがなければクリア
  } catch (e) {
    console.error(e)
    error.value = '接続に失敗しました。バックエンドのコンテナは起動していますか？'
    message.value = '' // メッセージをクリア
  }
}
</script>

<style>
/* 簡単なスタイルで見栄えを良くする */
body {
  font-family: sans-serif;
  padding: 2em;
  background-color: #f4f7f6;
}
div {
  max-width: 600px;
  margin: 0 auto;
  padding: 2em;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
button {
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4CAF50; /* Green */
  color: white;
  border: none;
  border-radius: 5px;
}
p {
  margin-top: 20px;
  font-size: 18px;
}
</style>