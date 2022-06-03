<template>
    <div>
        <LoginPanel @user:login="login" v-if="user==0"/>
        <ElectionChoice @election:vote="showVoting" @election:results="showResults" :elections=this.elections v-if="user!=0 && selectedElection == 0"/>
        <ElectionPanel @vote:submit="submitVote" :election=this.elections[0] :options=this.electionOptions v-if="selectedElection!=0"/>
    </div>
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
                    multipleChoice: false,
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
            ],
            selectedElection: 0,
            user: 0
        }
    },
    props: {
    },
    methods: {
        login(usr) {
            this.user = usr
            this.elections=usr.electionList
            for(const election of this.elections){
                election.id=election.electionId
                election.name=election.electionName
                election.active=election.electionActive
                if (election.electionType=='approval')  
                    election.multipleChoice=true
                else   
                    election.multipleChoice=false
            }
        },
        showVoting(election) {
            // TODO options request
            this.selectedElection = election
        },
        showResults(election) {
            // TODO
            election.name
        },
        submitVote(options, selected) {
            this.selectedElection = 0
            options[0].description
            selected
            // TODO do it
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>