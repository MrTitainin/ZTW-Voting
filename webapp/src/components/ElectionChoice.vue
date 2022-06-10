<template>
    <div class="shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 bg-white sm:p-6  bg-emerald-700">
            <div class="grid grid-cols-4 gap-x-2 gap-y-10 items-center" v-for="election in elections" :key="election.id">
                <div class="mt-5 col-start-auto text-emerald-200 sm:col-span-1 align-middle">{{ election.name }}</div>
                <button class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-50 bg-emerald-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200" @click="vote(election)" :disabled="!election.votable">Vote</button>
                <button class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-50 bg-emerald-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200" @click="results(election)" :disabled="election.active">Results</button>
                <button class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-50 bg-emerald-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200" @click="stop(election)" :disabled="!election.active" v-if="this.admin">End</button>
            </div>
            <button class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-800 bg-emerald-300 hover:bg-indigo-700 hover:text-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" @click="create()" v-if="this.admin">New</button>
        </div>
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