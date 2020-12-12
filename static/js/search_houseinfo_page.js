var default_index = '4'
const app1 = new Vue({
    el: '#app1',
    data: {
        input: null,
        tableData: [],
        gridData_detail: [
                    {
                        "houseid": '',
                        "city": "",
                        "county": "",
                        "street": "",
                        "comm_name": "",
                        "price": '',
                        "longitude": "",
                        "latitude": "",
                        "area": '',
                        "orientation": "",
                        "priceunit": "",
                        "check_in_time": "",
                        "floor": "",
                        "lift": "",
                        "car_station": "",
                        "water": "",
                        "power": "",
                        "gas": "",
                        "lease_term": "",
                        "rent_share": "",
                        "house_style": "",
                        "furniture": "",
                        "fur_num": '',
                        "metro": '',
                        "detail_link": ""
                    }
                ],
        minmetro: '',
        maxmetro: '',
        minarea: '',
        maxarea: '',
        minprice: '',
        maxprice: '',
        area: '',
        count: 0,
        nextPage: '',
        prevPage: '',
        f_url: '',
        radio: '-price',
        button_status: false,
        loading: false,
        user_image_path: '',
        area_options: [
            {value: '0-20', label: '20平米以下'},
            {value: '20-40', label: '20-40平米'},
            {value: '40-60', label: '40-60平米'},
            {value: '60-80', label: '60-80平米'},
            {value: '80-100', label: '80-100平米'},
            {value: '100-120', label: '100-120平米'},
            {value: '120-300', label: '120平米以上'},
            {value: '0-300', label: '房屋面积不限'},
        ],
        area_value: '房屋面积不限',
        price_options: [
            {value: '0-500', label: '500元/月以下'},
            {value: '500-1000', label: '500-1000元/月'},
            {value: '1000-1500', label: '1000-1500元/月'},
            {value: '1500-2000', label: '1500-2000元/月'},
            {value: '2000-2500', label: '2000-2500元/月'},
            {value: '2500-3000', label: '2500-3000元/月'},
            {value: '3000-9999', label: '3000元/月以上'},
            {value: '0-9999', label: '租房价格不限'},
        ],
        price_value: '月租价格不限',
        metro_options: [
            {value: '0-300', label: '300米以下'},
            {value: '300-500', label: '300-500米'},
            {value: '500-700', label: '500-700米'},
            {value: '700-900', label: '700-900米'},
            {value: '900-1100', label: '900-1100米'},
            {value: '1100-1300', label: '1100-1300米'},
            {value: '1300-1500', label: '1300-1500米'},
            {value: '1500-1700', label: '1500-1700米'},
            {value: '1700-999999', label: '1700米以上'},
            {value: '0-999999', label: '地铁距离不限'},
        ],
        metro_value: '地铁距离不限',
    },
    created(){
        // 加载头像
        this.user_image_path = localStorage.getItem('user_image_path')
    },
    methods: {
        handleSelect(key, keyPath){
            console.log(key, keyPath);
            if(key=='3'){
                document.location.href = '/static/html/spider_page.html';
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
            if(key=='6'){
                document.location.href = '/static/html/analysis_page.html';
            }
            if(key=='2-2'){
                localStorage.setItem('prv_url', '/static/html/spider_page.html')
                document.location.href = '/static/html/user_image.html';
            }
            if(key=='2-3'){
                localStorage.setItem('prv_url', '/static/html/search_houseinfo_page.html')
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
        },
        // 点击按钮查找元素
        start_search(){
            // 显示加载
            this.loading = true
            // 用于是否点击排序方式发送请求
            this.button_status = true
            this.f_url = `/api/houseinfos/?minmetro=${this.minmetro}&maxmetro=${this.maxmetro}&minprice=${this.minprice}&maxprice=${this.maxprice}&minarea=${this.minarea}&maxarea=${this.maxarea}&area=${this.area}&ordering=${this.radio}`
            let token = localStorage.getItem('token')
            fetch(this.f_url, {
                headers:{
                    'Content-Type': 'application/json',
                    'token': token,
                },
            })
                .then(resp => resp.json())
                .then(json => {
                if(json.code==401){
                    localStorage.removeItem('token')
                    document.location.href = '/static/html/login.html';
                }else{
                    this.tableData = json.results
                    this.count = json.count
                    this.prevPage = json.previous
                    this.nextPage = json.next
                    this.$message({
                        message: `搜索完成，发现${this.count}条记录`,
                        type: 'success',
                        center: true,
                    });
                    // 关闭加载
                    this.loading = false
                }
                })
        },
        handleCurrentChange(currentPage) {
              this.loadData(this.f_url + '&page=' + currentPage)
        },
        // 分页加载
        loadData(url){
            if (url) {
                // 显示加载
                this.loading = true
                let token = localStorage.getItem('token')
                fetch(url, {
                    headers:{
                        'Content-Type': 'application/json',
                        'token': token,
                    },
                })
                .then(resp => resp.json())
                .then(json => {
                    // 401错误，未提供正确的token
                    if(json.code==401){
                        localStorage.removeItem('token')
                        document.location.href = '/static/html/login.html';
                    }else{
                        this.tableData = json.results
                        this.count = json.count
                        this.nextPage = json.next
                        this.prevPage = json.previous
                        // 关闭加载
                        this.loading = false
                    }

                })
            }
        },
        // 构建排序方式
        filter(){
            area_s = this.area_value
            price_s = this.price_value
            metro_s = this.metro_value
            if(area_s == '房屋面积不限'){
                area_s = '0-300'
            }
            if(price_s == '月租价格不限'){
                price_s = '0-9999'
            }
            if(metro_s == '地铁距离不限'){
                metro_s = '0-999999'
            }
            this.minprice = price_s.split('-')[0]
            this.maxprice = price_s.split('-')[1]
            this.minarea = area_s.split('-')[0]
            this.maxarea= area_s.split('-')[1]
            this.minmetro = metro_s.split('-')[0]
            this.maxmetro = metro_s.split('-')[1]
        },
        // 点击排序方式自动请求
        reverse(){
            if(this.button_status == true){
                this.f_url = `/api/houseinfos/?minmetro=${this.minmetro}&maxmetro=${this.maxmetro}&minprice=${this.minprice}&maxprice=${this.maxprice}&minarea=${this.minarea}&maxarea=${this.maxarea}&area=${this.area}&ordering=${this.radio}`
                this.loadData(this.f_url)
                this.$message({
                    message: `调整排序方式完成`,
                    type: 'success',
                    center: true,
                });
            }
        },
        // 查看单个详情
        handleClick(a){
            let token = localStorage.getItem('token')
            let url = `/api/houseinfos/${a.houseid}/`
            fetch(url, {
                headers:{
                    'Content-Type': 'application/json',
                    'token': token,
                },
            })
            .then(resp => resp.json())
            .then(json => {
                if(json.code==401){
                    localStorage.removeItem('token')
                    document.location.href = '/static/html/login.html';
                }else{
                    this.gridData_detail = json.results
//                    console.log(json.results)
                }

            })
        }
    }

})