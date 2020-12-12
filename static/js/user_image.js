const app1 = new Vue({
    el: '#app1',
    data: {
        url: '',
        username: '',
        srcList: [],
        dialogImageUrl: '',
        dialogVisible: false,
        upload_status: true,
        headers: '',
        upload_url: '/api/new_image/',
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
                //console.log(json.results)
                // 头像
                this.url = json.results.image_path
                this.srcList.push(json.results.image_path)
                // 用户名
                this.username = json.results.username
                //console.log(this.srcList)
            }
        })
    },
    methods:{
        goBack(){
            // 从本地读取上次菜单
            let prv_url = localStorage.getItem('prv_url')
            if(prv_url != null){
                document.location.href = prv_url
            }else{
                document.location.href = '/static/html/index.html'
            }
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        upload_fail(){
            this.$notify({
                title: '错误',
                message: '上传头像失败',
                type: 'warning',
                duration: 3500
            });
        },
        upload_success(file){
            //console.log(file)
            // 更新本地存放的用户头像信息
            localStorage.setItem('user_image_path', file.results)
            this.$notify({
                title: '成功',
                message: '上传头像成功',
                type: 'success',
                duration: 3500
            });
        },
        change_user_info(){
            document.location.href = '/static/html/change_user_info.html'
        }
    }
})