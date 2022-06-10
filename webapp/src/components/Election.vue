<template>
    <div class="shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 bg-white sm:p-6  bg-emerald-700 text-emerald-200">
            <p class="font-bold text-emerald-50">{{election.name}}</p>
            <form @submit.prevent="handleSubmit" class="mt-3 flex flex-col items-start place-content-start">
                <div v-for="option in options" :key="option.id" class="mt-2">
                    <input type="radio" v-model="optionSelected" name="optionSelected" :value="option.id" v-if="!election.multipleChoice" class="object-left">
                    <input type="checkbox" v-model="option.approved" v-if="election.multipleChoice" class="object-left"/>
                    {{ option.description }}
                </div>
                <input class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-50 bg-emerald-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200" type="submit" value="Vote">
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ElectionPanel',
    props: {
        election: Object,
        options: Array,
    },
    data() {
        return {
            optionSelected: -1,
        }
    },
    methods: {
        handleSubmit() {
            /*if(this.invalidId || this.invalidTitle || this.invalidAuthor || this.invalidPages) return
            if(this.update){
                this.$emit('update:book', this.book)
                this.update = false
            }
            else*/
            this.$emit('vote:submit', this.options, this.optionSelected)
            //this.newBook()
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>