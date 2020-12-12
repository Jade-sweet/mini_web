var re_username = /^[a-zA-Z\u4e00-\u9fa5]{2,8}$/
var re_tel = /^1[3-9][0-9]{9}$/
var re_tel_code = /^[0-9]{6}$/
const app1 = new Vue({
    el: '#app1',
    data: {
        username: '',
        tel: '',
        tel_code: '',
        old_username:'',
        old_tel: '',
    },
    created(){
        let token = localStorage.getItem('token')
        this.headers = {
            'token': token,
            }
        fetch('/api/get_user_info/',{
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
                this.$notify({
                    title: '警告',
                    message: json.results,
                    type: 'warning',
                    duration: 3500
                });
            }else{
                // 用户名
                this.username = json.results.username
                this.tel = json.results.tel
                this.old_tel = json.results.tel
                this.old_name = json.results.username
                //console.log(this.srcList)
            }
        })
    },

    methods:{
        exit(){
            document.location.href = '/static/html/user_image.html'
        },
        Login(){
            // 禁用按钮
            $('#user_sure_click').attr('disabled', 'true')
            if(this.old_name==this.username && this.old_tel==this.tel){
                document.location.href = '/static/html/user_image.html'
            }else{
                // 前端鉴定规则
                if(!re_username.test(this.username) || !re_tel.test(this.tel) || !re_tel_code.test(this.tel_code)){
                    this.$message({
                        message: '输入数据不符合规范',
                        type: 'warning',
                        center: true,
                    });
                    // 解除禁用按钮 change_user_tel
                    $('#user_sure_click').removeAttr('disabled')
                    return
                }else{
                    let token = localStorage.getItem('token')
                    fetch('/api/change_user_tel/', {
                    method:'POST',
                    headers:{
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'token': token,
                    },
                    body:`username=${this.username}&tel=${this.tel}&tel_code=${this.tel_code}`,
                })
                .then(resp => resp.json())
                .then(json => {
                    // 解除禁用按钮
                    $('#user_sure_click').removeAttr('disabled')
                    // 修改成功
                    if(json.code==90001){
                        this.$message({
                            message: json.message,
                            type: 'success',
                            center: true,
                        });
                        setTimeout(function(){document.location.href = '/static/html/user_image.html'},1000)
                    }else{
                        this.$message({
                            message: json.message,
                            type: 'warning',
                            center: true,
                        });
                    }
                    })
                }
            }
        },
        // 点击发送短信
        getCache(event){
            if(!re_tel.test(this.tel)){
                this.$message({
                    message: '请输入正确的手机号',
                    type: 'warning',
                    center: true,
                });
                return
            }else{
                // 禁用按钮
                $('#cache').attr('disabled',"false");
                var time= 120
                time1 = setTimeout(function(){
                    // 清除禁用
                    clearInterval(time2)
                    // 恢复初态
                    $('#cache').removeAttr('disabled');
                    $('#cache').text(`获取验证码`)
                }, 121000)
                // 定时减少时间
                time2 = setInterval(function(){
                    $('#cache').text(`${time}s后可用`);
                    time = time - 1
                },1000)
                fetch(`/common/tel_code/?tel=${this.tel}`)
                    .then(resp => resp.json())
                    .then(json => {
                        if(json.code==200){
                            this.$message({
                                message: json.message,
                                type: 'success',
                                center: true,
                            });
                        }else{
                            this.$message({
                                message: json.message,
                                type: 'warning',
                                center: true,
                            });
                        }

                    })
            }
        }
    }
})