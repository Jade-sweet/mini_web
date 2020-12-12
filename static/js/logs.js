const app1 = new Vue({
    el: '#app1',
    data: {
        logs_options: [],
        loading: false,
    },
    created(){
        this.loading = true
        let token = localStorage.getItem('token')
        fetch('/api/logs/',{
            headers:{
			'Content-Type': 'application/json',
			'token': token,
		    },
        })
        .then(resp => resp.json())
        .then(json => {
            if(json.code==401){
                // 移除本地存储的token
                localStorage.removeItem('token')
                this.$message({
                    message: json.message,
                    type: 'warning',
                    center: true,
                });
            }else{
                this.loading = false
                this.logs_options = json.results
            }
        })
    },
    methods:{
        load(){
            this.logs_options = this.logs_options.push(0)
        },
        goBack(){
            // 从本地读取上次菜单
            let prv_url = localStorage.getItem('prv_url')
            if(prv_url != null){
                document.location.href = prv_url
            }else{
                document.location.href = '/static/html/index.html'
            }
        }
    }
})