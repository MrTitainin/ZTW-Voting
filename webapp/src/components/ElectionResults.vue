<template>
    <div class="shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 bg-white sm:p-6  bg-emerald-700 text-emerald-200">
            <p class="font-bold text-emerald-50">{{results.electionName}}</p>
            <div class="mt-2 flex flex-row gap-2 items-center divide-x">
                <div v-for="option in results.options" :key="option.id" class="">
                    <div class="ml-2 flex-1 text-center">{{ option.optionName }}</div>
                    <div class="ml-2 flex-none">{{ option.voteCount }}</div>
                </div>
            </div>
            <button class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-800 bg-emerald-300 hover:bg-indigo-700 hover:text-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" @click="hide()">Close</button>
            <!--{{results}}-->
        </div>
    </div>
</template>

<script>
export default {
    name: 'ElectionResults',
    props: {
        results: Object,
    },
    data() {
        return {
            optionSelected: -1,
        }
    },
    methods: {
        hide() {
            /*if(this.invalidId || this.invalidTitle || this.invalidAuthor || this.invalidPages) return
            if(this.update){
                this.$emit('update:book', this.book)
                this.update = false
            }
            else*/
            this.$emit('results:hide')
            //this.newBook()
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>