<template>
    <div class="shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 bg-white sm:p-6 text-emerald-200  bg-emerald-700 items-start">
            <form @submit.prevent="handleSubmit">
                <div class="md:grid md:grid-cols-3 md:gap-6">
                    <div class="flex justify-start">
                        <label>Election name</label>
                    </div>
                    <input class="mt-5 md:mt-0 md:col-span-2 flex justify-start text-violet-600 font-bold focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" type="text" v-model="election.name" />
                    <div class="flex justify-start">
                        <label>Is multiple choice allowed?</label>
                    </div>
                    <div class="mt-5 md:mt-0 md:col-span-2 flex justify-start">
                        <input type="checkbox" v-model="election.multipleChoice" />
                        <label v-if="election.multipleChoice" class="ml-3">Yes</label>
                        <label v-else class="ml-3">No</label>
                    </div>
                </div>
                <hr class="mt-5"/>
                <div class="flex justify-start mt-5">
                    <label>Options: </label>
                </div>
                <div class="md:grid md:grid-cols-3 md:gap-6 mt-5" v-for="option in election.options" :key="option.id">
                    <div class="flex justify-start">
                        <label>Description </label>
                    </div>
                    <input class="mt-5 md:mt-0 md:col-span-2 text-violet-600 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" type="text" v-model="option.description" />
                </div>
                <input class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-50 bg-emerald-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200" type="button" @click="add()" value="Add new option"/><br/>
                <hr class="mt-5"/>
                <input class="mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-50 bg-emerald-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200" type="submit" :disabled="unready" value="Create and start election">
                <input class="mt-5 ml-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-emerald-200 bg-emerald-800 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200" type="button" @click="cancel()" value="Cancel">
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CreateElection',
    data() {
        return {
            election: {
                name: '',
                active: 'false',
                multipleChoice: 'true',
                options:[
                    {
                        id:0,
                        description:''
                    }
                ]
            },
            currentId:1,
        }
    },
    methods: {
        handleSubmit() {
            this.$emit('election:submit', this.election)
        },
        add() {
            this.election.options.push({
                id:this.currentId,
                description:''
            });
            this.currentId = this.currentId+1;
        },
        cancel() {
            this.$emit('election:cancel')
        }
    },
    computed: {
        unready() {
            function checkEmpty(field) {
                return field.description === ''
            }

            return this.election.name === '' || this.election.options.findIndex(checkEmpty)!=-1
        }
    },
    props: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
