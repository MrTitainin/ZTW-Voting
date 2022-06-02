<template>
    <div>
        <table>
            <tbody>
                <tr v-for="election in elections" :key="election.id">
                    <td>{{ election.name }}</td>
                    <!--td>{{ election.date }}</td-->
                    <td>
                        <button class="favorite" @click="vote(election)" :disabled="!election.active">Vote</button>
                        <button class="favorite" @click="results(election)" :disabled="election.active">Results</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
  name: 'ElectionChoice',
  props: {
      elections: Array,
  },
  methods: {
        vote(election) {
            this.$emit('election:vote', election)
        },
        results(election) {
            this.$emit('election:results', election)
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    table{
        margin-left: auto;
        margin-right: auto;
    }
</style>