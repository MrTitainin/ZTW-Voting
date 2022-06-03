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
            electionResults:{},
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
        async showVoting(election) {
            try {
                const response = await fetch("http://localhost:5123/api/elections/details/"+election.id,{
                    method: "POST",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({sessionKey:this.user.sessionKey}),
                });
                const data = await response.json();
                if (data.success){
                    this.electionOptions=data.options
                    for(const option of this.electionOptions){
                        option.id=option.optionId
                        option.description=option.optionName
                    }
                    this.selectedElection = election
                }
            } catch (error) {
                console.error(error);
            }
            //this.selectedElection = election
        },
        async showResults(election) {
            try {
                const response = await fetch("http://localhost:5123/api/elections/results/"+election.id,{
                    method: "POST",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({sessionKey:this.user.sessionKey}),
                });
                const data = await response.json();
                if (data.success){
                    this.electionResults=data
                    document.write(JSON.stringify(this.electionResults))
                }
            } catch (error) {
                console.error(error);
            }
            //election.name
        },
        async submitVote(options, selected) {
            if (!Array.isArray(selected))
                selected=[selected]
            try {
                const response = await fetch("http://localhost:5123/api/elections/vote",{
                    method: "POST",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        sessionKey:this.user.sessionKey,
                        electionId:this.selectedElection.id,
                        optionIds:selected
                    }),
                });
                const data = await response.json();
                document.write(JSON.stringify(data))
                if (data.success){
                    this.electionResults=data
                }
            } catch (error) {
                console.error(error);
            }
            this.selectedElection = 0
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>