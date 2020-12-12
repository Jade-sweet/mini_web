const app1 = new Vue({
    el: '#app1',
    data: {
        red: 80,
        green: 101,
        blue: 123,
        color1: 'rgba(36, 181, 187, 0.8)',
        color2: 'rgba(74, 157, 216, 0.8)',
        color3: 'rgba(140, 224, 176, 1)',
        color4: 'rgba(140, 224, 176, 1)',
        show2: false,
    },
    created(){
        let color = localStorage.getItem('bac_color')
        if(color!=null){
            document.body.style.backgroundColor = color;
            document.getElementsByClassName('bac')[0].style.backgroundColor = color
        }else{
            localStorage.setItem('bac_color', this.color2)
            document.body.style.backgroundColor = this.color2;
            document.getElementsByClassName('bac')[0].style.backgroundColor = this.color2
        }
    },
    methods:{
        ToPage(){
            document.location.href = '/static/html/search_houseinfo_page.html'
        },
        A1(){
            localStorage.setItem('bac_color', this.color1)
            document.body.style.backgroundColor = this.color1;
            document.getElementsByClassName('bac')[0].style.backgroundColor = this.color1
        },
        A2(){
            localStorage.setItem('bac_color', this.color2)
            document.body.style.backgroundColor = this.color2;
            document.getElementsByClassName('bac')[0].style.backgroundColor = this.color2
        },
        A3(){
            localStorage.setItem('bac_color', this.color3)
            document.body.style.backgroundColor = this.color3;
            document.getElementsByClassName('bac')[0].style.backgroundColor = this.color3
        },
        UserChange(){
            localStorage.setItem('bac_color', this.color4)
            document.body.style.backgroundColor = this.color4;
            document.getElementsByClassName('bac')[0].style.backgroundColor = this.color4
        }
    }
})