<template>
    <div>
        <LoginPanel @user:login="login" v-if="user==0"/>
        <ElectionChoice @election:vote="showVoting" @election:results="showResults" @election:stop="endElection" @election:create="createElection" :elections="this.elections" :admin="this.user.admin" v-if="user!=0 && selectedElection == 0 && !create"/>
        <ElectionPanel @vote:submit="submitVote" :election="this.elections[0]" :options="this.electionOptions" v-if="selectedElection!=0"/>
        <CreateElection @election:submit="startElection" v-if="create"/>
    </div>
</template>

<script>
import config from '@/config'

import LoginPanel from './Login.vue'
import ElectionChoice from './ElectionChoice.vue'
import ElectionPanel from './Election.vue'
import CreateElection from './CreateElection.vue'

export default {
    name: 'MainScreen',
    components: {
    LoginPanel,
    ElectionChoice,
    ElectionPanel,
    CreateElection
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
            user: 0,
            create: false,
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
        },
        createElection(){
            this.create = true;
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>