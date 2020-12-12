var re_password = /^[a-zA-Z0-9\.]{6,16}$/
const app1 = new Vue({
    el: '#app1',
    data: {
        password: '',
        password1: '',
    },
    methods:{
        Login(){
            // 禁用按钮
            $('#user_sure_click').attr('disabled', 'true')
            // 前端鉴定规则
            if(!re_password.test(this.password1) || !re_password.test(this.password)){
                this.$message({
                    message: '输入数据不符合规范',
                    type: 'warning',
                    center: true,
                });
                // 解除禁用
                $('#user_sure_click').removeAttr('disabled')
                return
            }else{
                fetch('/api/new_password/', {
                    method:'POST',
                    headers:{
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'token': localStorage.getItem('token')
                    },
                    body:`password1=${this.password1}&password=${this.password}`,
                })
                .then(resp => resp.json())
                .then(json => {
                    // 登录成功
                    // 解除禁用
                    $('#user_sure_click').removeAttr('disabled')
                    if(json.code==40001){
                        this.$message({
                            message: json.message,
                            type: 'success',
                            center: true,
                        });
                    }else{
                        this.$message({
                            message: json.message,
                            type: 'error',
                            center: true,
                        });
                    }
                })
            }
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