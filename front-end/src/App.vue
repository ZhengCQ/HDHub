<template>
  <div id="app">
    <navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Base/Navbar.vue'

export default {
  name: 'App',
  components: {
    navbar: Navbar
  }
}
</script>
