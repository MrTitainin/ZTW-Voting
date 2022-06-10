<template>
    <form @submit.prevent="handleSubmit">
        <div class="shadow overflow-hidden sm:rounded-md">
          <div class="px-4 py-5 bg-white sm:p-6 bg-emerald-700">
            <div class="grid grid-cols-4 gap-6 items-center">
                <label class="text-emerald-200 sm:col-span-1 align-middle">Login </label>
                <input v-model="user.login" type="text" class="sm:col-span-3 text-violet-600 mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"/>
                <label class="text-emerald-200 sm:col-span-1 align-middle">Hasło </label>
                <input v-model="user.password" type="text" class="sm:col-span-3 text-violet-600 mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"/>
            </div>
            <input type="submit" value="Zaloguj" class ="content-center text-emerald-100 mt-5 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md bg-emerald-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-600 disabled:text-slate-200">
          </div>
        </div>
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
