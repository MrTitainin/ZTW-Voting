<template>
    <LoginPanel/>
    <ElectionChoice :elections=this.elections />
    <ElectionPanel :election=this.elections[0] :options=this.electionOptions />
</template>

<script>
import LoginPanel from './Login.vue'
import ElectionChoice from './ElectionChoice.vue'
import ElectionPanel from './Election.vue'
export default {
    name: 'MainScreen',
    components: {
        LoginPanel,
        ElectionChoice,
        ElectionPanel
    },
    data() {
        return {
            elections: [
                {
                    id: 1,
                    name: 'Wybory test',
                    active: true,
                    multipleChoice: true,
                },
                {
                    id: 2,
                    name: 'Zakończone test',
                    active: false,
                    multipleChoice: true,
                },
            ],
            electionOptions: [
                {
                    id: 1,
                    description: 'Opcja 1',
                },
                {
                    id: 2,
                    description: 'Opcja 2',
                },
            ]
        }
    },
    props: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>