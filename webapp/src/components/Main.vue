<template>
    <div class="justify-center flex bg-emerald-900 items-center h-screen">
        <LoginPanel @user:login="login" v-if="user==0"/>
        <ElectionChoice @election:vote="showVoting" @election:results="showResults" @election:stop="endElection" @election:create="createElection" :elections="this.elections" :admin="this.user.admin" v-if="user!=0 && selectedElection == 0 && !create && !resultsVisible"/>
        <ElectionPanel @vote:submit="submitVote" :election="selectedElection" :options="this.electionOptions" v-if="selectedElection!=0"/>
        <CreateElection @election:submit="startElection" v-if="create"/>
        <ElectionResults @results:hide="hideResults" :results="this.electionResults" v-if="resultsVisible"/>
    </div>
</template>

<script>
import config from '@/config'

import LoginPanel from './Login.vue'
import ElectionChoice from './ElectionChoice.vue'
import ElectionPanel from './Election.vue'
import CreateElection from './CreateElection.vue'
import ElectionResults from './ElectionResults.vue'

export default {
    name: 'MainScreen',
    components: {
    LoginPanel,
    ElectionChoice,
    ElectionPanel,
    CreateElection,
    ElectionResults
},
    data() {
        return {
            elections: [
                {
                    id: 1,
                    name: 'Wybory test',
                    active: true,
                    multipleChoice: false,
                    votable:true,
                },
                {
                    id: 2,
                    name: 'Zakończone test',
                    active: false,
                    multipleChoice: true,
                    votable:false,
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
            resultsVisible:false,
            selectedElection: 0,
            user: 0,
            create: false,
        }
    },
    props: {
    },
    methods: {
        login(usr) {
            this.user = usr
            this.getElectionList()
        },
        async getElectionList(){
            try {
                const response = await fetch(config.SERVICE_URL+"elections/list",{
                    method: "POST",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({sessionKey:this.user.sessionKey}),
                });
                const data = await response.json();
                if (data.success){
                    this.elections=data.electionList
                    for(const election of this.elections){
                        election.id=election.electionId
                        election.name=election.electionName
                        election.active=!election.electionFinished
                        election.votable=election.electionVotable
                        if (election.electionType=='approval')  
                            election.multipleChoice=true
                        else   
                            election.multipleChoice=false
                    }
                }
            } catch (error) {
                console.error(error);
            }
        },
        async showVoting(election) {
            try {
                const response = await fetch(config.SERVICE_URL+"elections/details/"+election.id,{
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
            this.getElectionList()
            //this.selectedElection = election
        },
        async showResults(election) {
            try {
                const response = await fetch(config.SERVICE_URL+"elections/results/"+election.id,{
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
                    this.resultsVisible=true
                }
            } catch (error) {
                console.error(error);
            }
            
            //document.getElementById("tsk").innerHTML = JSON.stringify(this.electionResults)
            //election.name
        },
        async submitVote(options, selected) {
            if (selected==-1){
                selected=[]
                options.forEach(option => {
                    if (option.approved)
                        selected.push(option.id)
                });
            }
            if (!Array.isArray(selected))
                selected=[selected]
            try {
                const response = await fetch(config.SERVICE_URL+"elections/vote",{
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
                if (data.success){
                    this.electionResults=data
                }
            } catch (error) {
                console.error(error);
            }
            this.selectedElection = 0
            this.getElectionList()
        },
        async startElection(election) {
            this.create = false;
            const reqData={
                sessionKey:this.user.sessionKey,
                electionName:election.name,
                options:[]
            }
            if (election.multipleChoice=="true")
                reqData.voteType="approval"
            else
                reqData.voteType="single"
            for(const option of election.options)
                reqData.options.push(option.description)

            try {
                const response = await fetch(config.SERVICE_URL+"elections/start",{
                    method: "POST",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(reqData),
                });
                await response.json();
            } catch (error) {
                console.error(error);
            }
            this.getElectionList()
        },
        async endElection(electionId) {
            try {
                const response = await fetch(config.SERVICE_URL+"elections/end",{
                    method: "PATCH",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        sessionKey:this.user.sessionKey,
                        electionId:electionId
                    }),
                });
                await response.json();
            } catch (error) {
                console.error(error);
            }
            this.getElectionList()
        },
        createElection(){
            this.create = true;
        },
        hideResults(){
            this.resultsVisible = false;
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>