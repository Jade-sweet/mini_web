var default_index = '6'
const app1 = new Vue({
    el: '#app1',
    data: {
        user_image_path: '',
        head_word: [
            '首先感谢您使用本网站作为您的辅助找房工具',
            '下面的内容是简单对成都最近二手房价的大概分析',
            '初次涉及此领域，如有错误，请指正'
        ]
    },
    created(){
        // 加载头像
        this.user_image_path = localStorage.getItem('user_image_path')
    },
    // 负责页面跳转
    methods: {
       handleSelect(key, keyPath){
            console.log(key, keyPath);
            if(key=='4'){
                document.location.href = '/static/html/search_houseinfo_page.html';
            }
            if(key=='1'){
                document.location.href = '/static/html/index.html';
            }
            if(key=='3'){
                document.location.href = '/static/html/spider_page.html';
            }
            if(key=='5'){
                document.location.href = '/static/html/house_map.html';
            }
            if(key=='2-1'){
                localStorage.setItem('prv_url', '/static/html/analysis_page.html')
                document.location.href = '/static/html/change_password.html';
            }
            if(key=='2-2'){
                localStorage.setItem('prv_url', '/static/html/analysis_page.html')
                document.location.href = '/static/html/user_image.html';
            }
            if(key=='2-3'){
                localStorage.setItem('prv_url', '/static/html/analysis_page.html')
                document.location.href = '/static/html/logs.html';
            }
            if(key=='2-4'){
                let token = localStorage.getItem('token')
                fetch('/api/invalid_token/', {
                    headers:{
                    'Content-Type': 'application/json',
                    'token': token,
                    },
                })
                .then(resp => resp.json())
                .then(json => {
                    localStorage.removeItem('token')
                    document.location.href = '/static/html/login.html';
                })
            }
        }
    }

})

