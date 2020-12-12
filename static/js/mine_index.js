function check(){
    let color = localStorage.getItem('bac_color')
    document.body.style.backgroundColor = color;
    let token = localStorage.getItem('token')
    if(token){
        console.log('检查了')
        fetch(`/common/check_login/`, {
            headers:{
			'Content-Type': 'application/json',
			'token': token,
		    },
        })
        .then(resp => resp.json())
        .then(json => {
            console.log(json.results)
            if(json.results=='false'){
                location.href = '/static/html/login.html'
            }
        })
    }else{
        location.href = '/static/html/login.html'
    }
}

check()
