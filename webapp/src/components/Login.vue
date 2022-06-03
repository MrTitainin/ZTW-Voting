<template>
    <form @submit.prevent="handleSubmit">
        <label>Login </label>
        <input v-model="user.login" type="text" /><br/>
        <label>Hasło </label>
        <input v-model="user.password" type="text" /><br/>
        <input type="submit" value="Zaloguj">
    </form>
</template>

<script>
import config from '@/config';

export default {
    name: 'LoginPanel',
    data() {
        return {
            user: {
                login: '',
                password: '',
            },
        }
    },
    methods: {
        async handleSubmit() {
            try {
                let formData = new FormData();
                formData.append('login', this.user.login);
                formData.append('password', this.user.password);
                
                const response = await fetch(config.SERVICE_URL+"users/login", {
                method: "POST",
                
                body: formData,
                });
                const res = await response.json();
                if (res.success==false)    return 
                this.$emit('user:login', res)
            } catch (error) {
                console.error(error);
            }
        }
    },
    props: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
