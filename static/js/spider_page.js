var default_index = '3'
const app1 = new Vue({
    el: '#app1',
    data: {
        city: null,
        citys:[{'num': 0, 'value': '安庆市'}, {'num': 1, 'value': '保定市'}, {'num': 2, 'value': '宝鸡市'}, {'num': 3, 'value': '保亭市'}, {'num': 4, 'value': '北海市'}, {'num': 5, 'value': '长春市'}, {'num': 6, 'value': '常德市'}, {'num': 7, 'value': '长沙市'}, {'num': 8, 'value': '常州市'}, {'num': 9, 'value': '成都市'}, {'num': 10, 'value': '澄迈市'}, {'num': 11, 'value': '重庆市'}, {'num': 12, 'value': '滁州市'}, {'num': 13, 'value': '大连市'}, {'num': 14, 'value': '大理市'}, {'num': 15, 'value': '丹东市'}, {'num': 16, 'value': '儋州市'}, {'num': 17, 'value': '达州市'}, {'num': 18, 'value': '德阳市'}, {'num': 19, 'value': '东莞市'}, {'num': 20, 'value': '鄂州市'}, {'num': 21, 'value': '防城港市'}, {'num': 22, 'value': '佛山市'}, {'num': 23, 'value': '福州市'}, {'num': 24, 'value': '赣州市'}, {'num': 25, 'value': '广州市'}, {'num': 26, 'value': '桂林市'}, {'num': 27, 'value': '贵阳市'}, {'num': 28, 'value': '哈尔滨市'}, {'num': 29, 'value': '海口市'}, {'num': 30, 'value': '海门市'}, {'num': 31, 'value': '杭州市'}, {'num': 32, 'value': '汉中市'}, {'num': 33, 'value': '合肥市'}, {'num': 34, 'value': '淮安市'}, {'num': 35, 'value': '黄石市'}, {'num': 36, 'value': '呼和浩特市'}, {'num': 37, 'value': '惠州市'}, {'num': 38, 'value': '湖州市'}, {'num': 39, 'value': '江门市'}, {'num': 40, 'value': '江阴市'}, {'num': 41, 'value': '吉安市'}, {'num': 42, 'value': '嘉兴市'}, {'num': 43, 'value': '吉林市'}, {'num': 44, 'value': '济南市'}, {'num': 45, 'value': '金华市'}, {'num': 46, 'value': '济宁市'}, {'num': 47, 'value': '晋中市'}, {'num': 48, 'value': '九江市'}, {'num': 49, 'value': '开封市'}, {'num': 50, 'value': '昆明市'}, {'num': 51, 'value': '昆山市'}, {'num': 52, 'value': '廊坊市'}, {'num': 53, 'value': '兰州市'}, {'num': 54, 'value': '乐东市'}, {'num': 55, 'value': '乐山市'}, {'num': 56, 'value': '凉山市'}, {'num': 57, 'value': '临高市'}, {'num': 58, 'value': '陵水市'}, {'num': 59, 'value': '临沂市'}, {'num': 60, 'value': '柳州市'}, {'num': 61, 'value': '洛阳市'}, {'num': 62, 'value': '马鞍山市'}, {'num': 63, 'value': '眉山市'}, {'num': 64, 'value': '绵阳市'}, {'num': 65, 'value': '南昌市'}, {'num': 66, 'value': '南充市'}, {'num': 67, 'value': '南京市'}, {'num': 68, 'value': '南宁市'}, {'num': 69, 'value': '南通市'}, {'num': 70, 'value': '宁波市'}, {'num': 71, 'value': '青岛市'}, {'num': 72, 'value': '清远市'}, {'num': 73, 'value': '秦皇岛市'}, {'num': 74, 'value': '琼海市'}, {'num': 75, 'value': '泉州市'}, {'num': 76, 'value': '三亚市'}, {'num': 77, 'value': '上海市'}, {'num': 78, 'value': '上饶市'}, {'num': 79, 'value': '绍兴市'}, {'num': 80, 'value': '沈阳市'}, {'num': 81, 'value': '深圳市'}, {'num': 82, 'value': '石家庄市'}, {'num': 83, 'value': '苏州市'}, {'num': 84, 'value': '泰安市'}, {'num': 85, 'value': '太原市'}, {'num': 86, 'value': '台州市'}, {'num': 87, 'value': '唐山市'}, {'num': 88, 'value': '天津市'}, {'num': 89, 'value': '万宁市'}, {'num': 90, 'value': '潍坊市'}, {'num': 91, 'value': '威海市'}, {'num': 92, 'value': '文昌市'}, {'num': 93, 'value': '温州市'}, {'num': 94, 'value': '武汉市'}, {'num': 95, 'value': '芜湖市'}, {'num': 96, 'value': '无锡市'}, {'num': 97, 'value': '五指山市'}, {'num': 98, 'value': '厦门市'}, {'num': 99, 'value': '襄阳市'}, {'num': 100, 'value': '西安市'}, {'num': 101, 'value': '咸阳市'}, {'num': 102, 'value': '新乡市'}, {'num': 103, 'value': '西双版纳市'}, {'num': 104, 'value': '许昌市'}, {'num': 105, 'value': '徐州市'}, {'num': 106, 'value': '盐城市'}, {'num': 107, 'value': '烟台市'}, {'num': 108, 'value': '宜昌市'}, {'num': 109, 'value': '银川市'}, {'num': 110, 'value': '义乌市'}, {'num': 111, 'value': '岳阳市'}, {'num': 112, 'value': '张家口市'}, {'num': 113, 'value': '漳州市'}, {'num': 114, 'value': '湛江市'}, {'num': 115, 'value': '郑州市'}, {'num': 116, 'value': '镇江市'}, {'num': 117, 'value': '中山市'}, {'num': 118, 'value': '珠海市'}, {'num': 119, 'value': '株洲市'}, {'num': 120, 'value': '淄博市'}],
        county: null,
        counties: [],
        comm: null,
        comms: [],
        spider_info: [],
        input: null,
        loading: true,
        user_image_path: '',
    },
    created() {
        // 加载头像
        this.user_image_path = localStorage.getItem('user_image_path')
        let token = localStorage.getItem('token')
        fetch('/common/spider_info/',{
            headers:{
                'Content-Type': 'application/json',
                'token': token,
            },
        })
        .then(resp => resp.json())
        .then(json => {
            console.log(json)
            if(json.code==10002){
                this.spider_info = json.results
                this.loading = false
            }else{
                // 移除本地存储的token
                localStorage.removeItem('token')
                console.log(111)
                this.$message({
                    message: json.message,
                    type: 'warning',
                    center: true,
                });
            }
        })
    },
    methods: {
        selectCity() {
            this.county = []
            this.comms = []
            this.county = null
            this.comm = null
            let token = localStorage.getItem('token')
            fetch('/common/county_list/?city=' + this.city,{
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
                    this.counties = json.results
                }
            })
        },
        selectCounty() {
            this.comms = []
            this.comm = null
            let token = localStorage.getItem('token')
            fetch(`/common/street_list/?county=${this.county}&city=${this.city}`,{
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
                    this.comms = json.results
                }
            })
        },
        start_spider(){
            if(this.city == null){
                this.$notify({
                    title: '警告',
                    message: '请先选择城市再开始搜集哦~',
                    type: 'warning',
                    duration: 1500
                });
                return
            }
            if(this.county == null){
                this.$notify({
                    title: '警告',
                    message: '请先选择市区再开始搜集哦~',
                    type: 'warning',
                    duration: 1500
                });
                return
            }
            if(this.comm == null){
                this.$notify({
                    title: '警告',
                    message: '请先选择街道再开始搜集哦~',
                    type: 'warning',
                    duration: 1500
                });
                return
            }
            city = this.city;
            comm = this.comm
            if(this.input != null){
                comm = this.input
            }
            let token = localStorage.getItem('token')
            fetch(`/common/spider/?city=${city}&comm=${comm}`,{
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
                            title: '警告 登录超时',
                            message: json.message,
                            type: 'warning',
                            duration: 3500
                        });
                    }else{
                        this.$notify({
                            title: '成功',
                            message: json.message,
                            type: 'success',
                            duration: 3500
                        });
                    }

                })
        },
        handleSelect(key, keyPath){
            console.log(key, keyPath);
            if(key=='4'){
                document.location.href = '/static/html/search_houseinfo_page.html';
            }
            if(key=='6'){
                document.location.href = '/static/html/analysis_page.html';
            }
            if(key=='1'){
                document.location.href = '/static/html/index.html';
            }
            if(key=='5'){
                document.location.href = '/static/html/house_map.html';
            }
            if(key=='2-1'){
                localStorage.setItem('prv_url', '/static/html/spider_page.html')
                document.location.href = '/static/html/change_password.html';
            }
            if(key=='2-2'){
                localStorage.setItem('prv_url', '/static/html/spider_page.html')
                document.location.href = '/static/html/user_image.html';
            }
            if(key=='2-3'){
                localStorage.setItem('prv_url', '/static/html/spider_page.html')
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