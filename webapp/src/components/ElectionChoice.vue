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
                        <button class="favorite" @click="stop(election)" :disabled="!election.active" v-if="this.admin">End</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <button class="favorite" @click="create()" v-if="this.admin">New</button>
    </div>
</template>

<script>
export default {
  name: 'ElectionChoice',
  props: {
      elections: Array,
      admin: Boolean,
  },
  methods: {
        vote(election) {
            this.$emit('election:vote', election)
        },
        results(election) {
            this.$emit('election:results', election)
        },
        stop(election) {
            this.$emit('election:stop', election.id)
        },
        create() {
            this.$emit('election:create')
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