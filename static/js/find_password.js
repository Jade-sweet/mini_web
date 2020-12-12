var re_tel = /^1[3-9][0-9]{9}$/
var re_password = /^[a-zA-Z0-9\.]{6,16}$/
var re_tel_code = /^[0-9]{6}$/
const app1 = new Vue({
    el: '#app1',
    data: {
        password: '',
        tel: '',
        tel_code: '',
    },
    methods:{
        Login(){
            // 禁用按钮
            $('#user_sure_click').attr('disabled', 'true')
            // 前端鉴定规则
            if(!re_password.test(this.password) || !re_tel.test(this.tel) || !re_tel_code.test(this.tel_code)){
                this.$message({
                    message: '输入数据不符合规范',
                    type: 'warning',
                    center: true,
                });
                // 解除限制
                $('#user_sure_click').removeAttr('disabled')
                return
            }else{
                fetch('/api/find_password/', {
                    method:'POST',
                    headers:{
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body:`password=${this.password}&tel=${this.tel}&tel_code=${this.tel_code}`,
                })
                .then(resp => resp.json())
                .then(json => {
                    // 解除限制
                    $('#user_sure_click').removeAttr('disabled')
                    // 修改成功
                    if(json.code==50001){
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
        },
        Token(){
            location.href = '/static/html/login.html'
        },
        NewUser(){
            location.href = '/static/html/register.html'
        },
        // 发送验证码
        getCache(){
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
                        // 返回码为200表示发送成功
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