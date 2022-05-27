<template>
    <table>
        <p>{{election.name}}</p>
        <form @submit.prevent="handleSubmit">
            <tbody>
                <tr v-for="option in options" :key="option.id">
                    <td>{{ option.description }}</td>
                    <!--td>{{ election.date }}</td-->
                    <td>
                        <button class="favorite" @click="update(book)" :disabled="!election.active">Vote</button>
                        <button class="favorite" @click="remove(book)" :disabled="election.active">Results</button>
                    </td>
                </tr>
            </tbody>
        </form>
    </table>
</template>

<script>
export default {
  name: 'ElectionPanel',
  props: {
      election: Object,
      options: Array,
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>