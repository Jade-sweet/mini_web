var re_username = /^[a-zA-Z\u4e00-\u9fa5]{2,8}$/
var re_tel = /^1[3-9][0-9]{9}$/
var re_password = /^[a-zA-Z0-9\.]{6,16}$/
const app1 = new Vue({
    el: '#app1',
    data: {
        username: '',
        password: '',
        login_img: '',
        loading: false,
        switch_value: true,
    },
    created(){
        this.loading = true
        this.username = localStorage.getItem('login_username')
        this.password = localStorage.getItem('login_password')
        fetch('/common/login_img/')
        .then(resp => resp.json())
        .then(json => {
            if(json.code==10002){
                this.login_img = json.results
                this.loading = false
            }
        })
    },
    methods:{
        Login(){
            // 禁用按钮
            $('#user_sure_click').attr('disabled', 'true')
            // 前端鉴定规则
            if(!re_username.test(this.username) && !re_tel.test(this.username) || !re_password.test(this.password)){
                this.$message({
                    message: '输入数据不符合规范',
                    type: 'warning',
                    center: true,
                });
                // 解除禁用
                $('#user_sure_click').removeAttr('disabled')
                return
            }else{
                if(this.switch_value==true){
                    localStorage.setItem('login_username', this.username)
                    localStorage.setItem('login_password', this.password)
                }else{
                    localStorage.removeItem('login_username')
                    localStorage.removeItem('login_password')
                }
                fetch('/api/token/', {
                    method:'POST',
                    headers:{
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body:`username=${this.username}&password=${this.password}`,
                })
                .then(resp => resp.json())
                .then(json => {
                    // 登录成功
                    // 解除禁用
                    $('#user_sure_click').removeAttr('disabled')
                    if(json.code==20001){
                        localStorage.setItem('token', json.results.token)
                        localStorage.setItem('user_image_path', json.results.user_image_path)
                        this.$message({
                            message: json.message,
                            type: 'success',
                            center: true,
                        });
                        // 延迟1秒跳转到首页
                        setTimeout(function(){
                            location.href = '/static/html/index.html'
                        },1500);

                    }else{
                        this.$message({
                            message: json.message,
                            type: 'warning',
                            center: true,
                        });
                    }
                })
            }
        },
        NewUser(){
            location.href = '/static/html/register.html'
        },
        FindPass(){
            location.href = '/static/html/find_password.html'
        }
    }
})