<template>
    <div>
        <p>{{election.name}}</p>
        <form @submit.prevent="handleSubmit">
            <div v-for="option in options" :key="option.id">
                <input type="radio" v-model="optionSelected" name="optionSelected" :value="option.id" v-if="!election.multipleChoice">
                <input type="checkbox" v-model="option.approved" v-if="election.multipleChoice"/>
                {{ option.description }}
            </div>
            <input type="submit" value="Zagłosuj">
        </form>
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