<template>
  <el-table :data="tableData">
    <el-table-column v-for="property in tableProperty" :prop="property.prop" :label="property.label" :width="columnWidth" :key="property.prop"></el-table-column>
  </el-table>
</template>

<script>
export default {
  props: {
    tableProperty: Array,
    tableData: Array,
    columnWidth: Number
  }
}
</script>