<template>
    <table>
        <tbody>
            <tr v-for="election in elections" :key="election.id">
                <td>{{ election.name }}</td>
                <!--td>{{ election.date }}</td-->
                <td>
                    <button class="favorite" @click="update(book)" :disabled="!election.active">Vote</button>
                    <button class="favorite" @click="remove(book)" :disabled="election.active">Results</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
  name: 'ElectionChoice',
  props: {
      elections: Array,
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>