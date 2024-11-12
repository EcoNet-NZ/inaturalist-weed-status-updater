<!--
====================================================================
Copyright 2023 EcoNet.NZ

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
====================================================================
-->
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