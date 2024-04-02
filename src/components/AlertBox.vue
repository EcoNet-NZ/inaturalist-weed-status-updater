<template>
    <div class="alert-box" :class="colorClass">
      <strong>{{ headingText }}</strong>
      <br />
      <slot />
    </div>
  </template>
  
  <script>
  export default {
    props: {
      type: {
        type: String,
        default: 'error',
        validator: (value) => ['error', 'success'].includes(value),
      },
    },
    computed: {
      headingText() {
        return this.type === 'error' ? 'Error!' : 'Success!';
      },
      colorClass() {
        return this.type === 'error' ? 'error' : 'success';
      },
    },
  };
  </script>
  
  <style scoped>
  .alert-box {
    border: 1px solid;
    border-radius: 4px;
    padding: 20px;
  }
  
  .error {
    color: #666;
    border-color: #f44336;
    background-color: #f8f8f8;
  }
  
  .error strong {
    color: #f44336;
  }
  
  .success {
    color: #666;
    border-color: #4caf50;
    background-color: #f8f8f8;
  }
  
  .success strong {
    color: #4caf50;
  }
  </style>