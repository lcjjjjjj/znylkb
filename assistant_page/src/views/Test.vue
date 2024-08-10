<script setup>

const saveFile = () => {
  const fileContent = 'This is a sample text file.'
  const blob = new Blob([fileContent], { type: 'text/plain' })
  const link = document.createElement('a')
  const url = window.URL.createObjectURL(blob)
  link.href = url
  link.download = ''
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}

</script>

<template>
  <div>
    <button @click="saveFile">Save File</button>
  </div>
</template>


<style scoped>

</style>
