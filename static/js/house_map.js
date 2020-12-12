var default_index = '5'
const app1 = new Vue({
    el: '#app1',
    data: {
        county: [],
        city: '成都市',
        value: '锦江',
        user_image_path: '',
    },
    created(){
        // 加载头像
        this.user_image_path = localStorage.getItem('user_image_path')
        this.GetInfo('锦江')
        let token = localStorage.getItem('token')
        fetch('/common/county_list/?city=' + this.city, {
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
                this.county = json.results
                //this.county.push({'num':20, 'value': '全部'})
            }
        })
    },
    methods: {
        handleSelect(key, keyPath){
            console.log(key, keyPath);
            if(key=='3'){
                document.location.href = '/static/html/spider_page.html';
            }
            if(key=='6'){
                document.location.href = '/static/html/analysis_page.html';
            }
            if(key=='1'){
                document.location.href = '/static/html/index.html';
            }
            if(key=='4'){
                document.location.href = '/static/html/search_houseinfo_page.html';
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
                localStorage.setItem('prv_url', '/static/html/house_map.html')
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
        MapInfo(){
            console.log(this.value)
            this.GetInfo(this.value)
        },
        // 根据市区获取房源数据
        GetInfo(val){
            let token = localStorage.getItem('token')
            fetch('/common/map_info/?county=' + val, {
                headers:{
                'Content-Type': 'application/json',
                'token': token,
                },
            })
            .then(resp => resp.json())
            .then(json => {
            // 登录超时
            if(json.code==401){
                // 移除本地存储的token
                localStorage.removeItem('token')
                this.$message({
                    message: json.message,
                    type: 'warning',
                    center: true,
                });
            }else{
                show_map(json.results.data1, json.results.data2, json.results.local)
            }
            })
        }
    }

})

// 画地图专用
function show_map(data1,data2, local){

    var myChart = echarts.init(document.getElementById('show_map'));

    var data = data1;
    var geoCoordMap = data2;

    var convertData = function (data) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
            var geoCoord = geoCoordMap[data[i].name];
            if (geoCoord) {
                res.push({
                    name: data[i].name,
                    value: geoCoord.concat(data[i].value)
                });
            }
        }
        return res;
    };

    var option = {
        title: {
            text: '所得租房信息分布图',
            left: 'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: function (params) {
                var color = params.color;//图例颜色
                var htmlStr ='<div>';
                htmlStr += params.name + '<br/>';//x轴的名称
                //为了保证和原来的效果一样，这里自己实现了一个点的效果
                htmlStr += '<span ></span>';

                //添加一个汉字，这里你可以格式你的数字或者自定义文本内容
                htmlStr += params.value[2] + '套';

                htmlStr += '</div>';

                return htmlStr;
            }
        },
        bmap: {
            center: local,
            zoom: 13,
            roam: true,
            mapStyle: {
                styleJson: [{
                    'featureType': 'water',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'land',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#f3f3f3'
                    }
                }, {
                    'featureType': 'railway',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'highway',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#fdfdfd'
                    }
                }, {
                    'featureType': 'highway',
                    'elementType': 'labels',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'arterial',
                    'elementType': 'geometry',
                    'stylers': {
                        'color': '#fefefe'
                    }
                }, {
                    'featureType': 'arterial',
                    'elementType': 'geometry.fill',
                    'stylers': {
                        'color': '#fefefe'
                    }
                }, {
                    'featureType': 'poi',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'green',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'subway',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'manmade',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'local',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'arterial',
                    'elementType': 'labels',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'boundary',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#fefefe'
                    }
                }, {
                    'featureType': 'building',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'label',
                    'elementType': 'labels.text.fill',
                    'stylers': {
                        'color': '#999999'
                    }
                }]
            }
        },
        series : [
            {
                name: '待出租套数',
                type: 'scatter',
                coordinateSystem: 'bmap',
                data: convertData(data),
                symbolSize: function (val) {
//                    console.log(val[2])
                    if (val[2] <= 10){
                        return val[2] / 2
                    }
                    return val[2] / 5;
                },
                label: {
                    formatter: '{b}',
                    position: 'right',
                    show: false
                },
                itemStyle: {
                    color: function(val){
                          if(val.value[2]<=10){
                              return '#111111'
                          }else if(10<val.value[2] && val.value[2]<=30){
                              return '#ffd16f'
                          }else if(30<val.value[2] && val.value[2]<=50){
                              return '#ffc647'
                          }else if(50<val.value[2] && val.value[2]<=70){
                              return '#fdbb00'
                          }else if(70<val.value[2] && val.value[2]<=90){
                              return '#ffe241'
                          }else if(90<val.value[2] && val.value[2]<=110){
                              return '#ffa500'
                          }else if(110<val.value[2] && val.value[2]<=130){
                              return '#fd7000'
                          }else if(130<val.value[2] && val.value[2]<=150){
                              return '#ff80b6'
                          }else if(150<val.value[2] && val.value[2]<=170){
                              return '#ff59a4'
                          }else if(170<val.value[2] && val.value[2]<=190){
                              return '#ff38a4'
                          }else if(190<val.value[2] && val.value[2]<=210){
                              return '#e0007a'
                          }else{
                              return '#ff0000'
                          }
                        },
                },
                emphasis: {
                    label: {
                        show: true
                    }
                }
            }
        ]
    };
    myChart.setOption(option);
}
