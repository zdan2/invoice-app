<template>
  <div>
    <h1>請求書管理アプリ 🧾</h1>
    
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>提出者名</th>
          <th>ファイル名</th>
          <th>提出日時</th>
          <th>ステータス</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="invoice in invoices" :key="invoice.id">
          <td>{{ invoice.id }}</td>
          <td>{{ invoice.client_name }}</td>
          <td>{{ invoice.file_name }}</td>
          <td>{{ invoice.uploaded_at }}</td>
          <td>
            <span :class="`status-${invoice.status}`">{{ invoice.status }}</span>
          </td>
        </tr>
      </tbody>
    </table>
    
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup>
// ... <script>部分は変更なし ...
import { ref, onMounted } from 'vue'

const invoices = ref([])
const error = ref('')

const fetchInvoices = async () => {
  try {
    const response = await fetch('http://localhost:8000/invoices')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    invoices.value = await response.json()
  } catch (e) {
    console.error(e)
    error.value = 'データの取得に失敗しました。'
  }
}

onMounted(() => {
  fetchInvoices()
})
</script>

<style>
/* ... <style>部分は変更なし ... */
</style>