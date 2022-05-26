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
        handleSubmit() {
            if(this.user.login != "root" || this.user.password != "toor") return
            this.user.login = "success!"
            this.$emit('user:login', this.user)
        }
    },
    props: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
