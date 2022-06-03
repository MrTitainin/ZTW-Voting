<template>
    <form @submit.prevent="handleSubmit">
        <label>Name </label>
        <input type="text" v-model="election.name" /><br/>
        <label>Multiple choice </label>
        <input type="checkbox" v-model="election.multipleChoice" /><br/>
        <div v-for="option in election.options" :key="option.id">
            <label>Description </label>
            <input type="text" v-model="option.description" />
        </div>
        <input type="button" @click="add()" value="Add"/><br/>
        <input type="submit" value="Create">
    </form>
</template>

<script>
export default {
    name: 'CreateElection',
    data() {
        return {
            election: {
                name: '',
                active: 'false',
                multipleChoice: 'false',
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
        }
    },
    props: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
